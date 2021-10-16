import subprocess, sys, os, datetime, pathlib, threading, logging, time, pexpect
from pexpect import pxssh
# setting: 
FileToRun = pathlib.PurePath("DistributedTest2.py")# set 'main' file that needs to run on the nano
folderToPushTo = pathlib.PurePath("~/Algorithm") # folder @ working computer too push the code to be run too
folderToPullFrom = pathlib.PurePath("NanoExecute/Example/distributedTest/") # relative to working directory contains fileToo run and dependencies  

#setting: om console output te controleren
#options: none: om alles te laten zien, 'nano6' ...: om specifiek alles van die remote te laten zien
remoteOutputToShow = None

#setting: om alle remotes/workers opnieuw te laten opstarten
rebootAll = False

#setting: selectie voor alle workers in de cluster
remoteIpDict = {
    #'nano1' : '192.168.4.2',
    # 'nano2' : '192.168.4.3',
    # 'nano3' : '192.168.4.4',
    # 'nano4' : '192.168.4.5',
    'nano5' : '192.168.4.6',
    'nano6' : '192.168.4.7'
    #'nano7' : '192.168.4.8',
    #'nano8' : '192.168.4.9',
    #'nano10': '192.168.4.10',
    #'nano11': '192.168.4.11'
}

# einde settings
#____________________________________________________________________________________________________

#setup logging
#init logging location
workDir = pathlib.Path.cwd() # get working directory for saving log files and 
datetime = datetime.datetime.now()
def timeToString(modifier): return str(datetime.strftime(modifier))
logFolderName = "log_%s-%s-%s_%s-%s-%s" % (timeToString(r"%y"), timeToString(r"%m"), timeToString(r"%d"), timeToString(r"%H"), timeToString(r"%M"), timeToString(r"%S"))
logFileFolder = workDir / "log" / logFolderName
logFileFolder.mkdir(parents=True, exist_ok=True)
print("logging to folder: " + str(logFileFolder))

loggingFormat = '%(levelname)s\t%(name)s: \t%(message)s'# format voor logging om te gebruiken 
logging.basicConfig(format=loggingFormat, level=logging.DEBUG)
logging.getLogger().addHandler(logging.FileHandler(str(logFileFolder / 'run.py.log'), mode='w+',delay=False))

def getRemoteLogging(remoteName):
    return logging.getLogger("remote."+remoteName)

#setting up how to handle remote logging locally
remoteLogger = logging.getLogger('remote')
remoteLogger.setLevel(logging.INFO)
if remoteOutputToShow is not None: 
    logging.warning("only showing output from remote."+remoteOutputToShow)
    remoteFilter = logging.Filter(getRemoteLogging(remoteOutputToShow).name)
    remoteLogger.addFilter(remoteFilter)
else:
    #filter everything but error from remotes
    nanoLoggerHandeler = logging.StreamHandler(sys.stdout)
    nanoLoggerHandeler.setLevel(logging.ERROR)
    nanoLoggerHandeler.setFormatter(logging.Formatter(loggingFormat))
    remoteLogger.addHandler(nanoLoggerHandeler)
    remoteLogger.propagate = False

# setup remote selection
remotes = list(remoteIpDict.keys())
remoteSelection = remotes
logging.info("using remotes: " + str(remoteIpDict))

# setup remote loggers
class LogPipe(threading.Thread):
    def __init__(self, level, logger):
        """Setup the object with a logger and a loglevel
        and start the thread"""
        threading.Thread.__init__(self, daemon=True)
        self.stop= False
        self.logger = logger
        self.level = level
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe"""
        return self.fdWrite

    def run(self):
        """Run the thread, logging everything."""
        while(not self.stop):
            for line in iter(self.pipeReader.readline, ''):
                self.logger.log(self.level, line.strip('\n'))
        self.pipeReader.close()

    def end(self):
        self.stop = True
        self.close()

    def close(self):
        """Close the write end of the pipe."""
        if (self.stop):
            try:os.close(self.fdWrite)
            except Exception:pass
        self.pipeReader.close()


successfullyFinished = False
runProcesses = []
try:
    logResources = {}
    def killLogResources(name):
        _ , fh,logPipeInfo, logPipeError = logResources[name]
        fh.close()
        logPipeInfo.end()
        logPipeError.end()
        logResources.pop(name)
    
    for name in remoteSelection:
        #setup logging
        log = getRemoteLogging(name)
        # log.setLevel(logging.INFO)
        logFileFolderFile = logFileFolder / (name + ".log")
        fh = logging.FileHandler(logFileFolderFile)
        fh.setLevel(logging.INFO)
        log.handlers.clear()
        [log.removeHandler(lH) for lH in log.handlers]
        log.addHandler(fh)

        logPipeInfo = LogPipe(level = logging.INFO, logger = log)
        logPipeError = LogPipe(level = logging.ERROR, logger = log)
    
        logResources[name] = (log, fh, logPipeInfo, logPipeError)

    logging.info("testing ssh connection")
    def testSSh(name):
        remote = pexpect.spawn("ssh {name}@{ip}".format(name= name, ip= remoteIpDict[name]))
        remoteTerminalIdentifier = ".*{name}@.*$".format(name= name)
        expectedResponces = ["password", "Are you sure you want to continue connecting (yes/no)", "Warning: Permanently added", remoteTerminalIdentifier]
        index = remote.expect(expectedResponces)
        while(index != expectedResponces.index(remoteTerminalIdentifier)):
            if (index == expectedResponces.index("password:")):
                remote.sendline(name)
            elif(index == expectedResponces.index("Are you sure you want to continue connecting (yes/no)")):
                remote.sendline("yes")
        logging.info("ssh login possible on: "+ name)
        logResources[name][0].info("test login success")
        remote.terminate()
            
    [testSSh(name) for name in remoteSelection]
    
    # reboot all devices 
    if(rebootAll):
        logging.info("start rebooting devices")
        [subprocess.call("ssh {name}@{ip} echo {name} | sudo -S reboot".format(name= name, ip= remoteIpDict[name]), shell=True) for name in remoteSelection]
        print("rebooting all remotes")
        time.sleep(60*3)# wait three minutes for devices to reboot

    # setup for copy to remote
    folderToPush = workDir / folderToPullFrom
    if not (folderToPush / FileToRun).exists():
        logging.fatal("Error: specified file to run cannot be found\n two possible variables could be miss specified: FileToRun & FolderToPullFrom\naborting")
        exit()

    print("starting copy process. coping: " + str(folderToPush))

    #Placing our Model / Algorithm.
    for remoteName  in remoteSelection:
        log, fh, logPipeInfo, logPipeError = logResources[name]
        # logging.info("making new dir on {name}".format(name = name))
        # subprocess.call("ssh %s@%s mkdir -p %s" % (remoteName, remoteIpDict[remoteName ], folderToPushTo), stdout= logPipeInfo, stderr= logPipeError, shell=True)
        logging.info("starting to copy on {name}".format(name = name))
        scpProcess = subprocess.Popen("scp -r %s %s@%s:%s" %(folderToPush, remoteName , remoteIpDict[remoteName ], folderToPushTo), stdout= logPipeInfo, stderr= logPipeError, shell=True)
        runProcesses.append((scpProcess, remoteName ))

    #Wait till every process is done
    for processes, remoteName  in runProcesses:
        out, err = processes.communicate()
        if out is not None: logging.info(str(remoteName ) +" output: " + str(out))
        if err is not None: logging.error(str(remoteName ) +" error: " + str(err))
        processes.terminate()
        logging.info(str(remoteName  + " copy ended"))


    logging.info("copy process completed")
    #Calling the copied script.
    runProcesses.clear()

    ipArgument = "--worker_ips "
    for remoteName in remoteSelection: ipArgument += remoteIpDict[remoteName ] + " "
    for name in remoteSelection:
        log, fh, logPipeInfo, logPipeError = logResources[name]
        
        #vb: ssh 192.168.1.1@nano1 python3 ~/Algorithm/test.py --worker_ips 192.168.1.1 192.168.1.2
        sshCommand = "%s@%s" % (name, remoteIpDict[name])
        logging.debug("folder to push to: "+ str(folderToPushTo))
        homeDir = pathlib.PurePath("/home") / name
        processCommandArray  = ["ssh",sshCommand, "python3.6", str(folderToPushTo / folderToPullFrom.parts[-1] / FileToRun), ipArgument]
        logging.info(name + " running: "+ str(processCommandArray))
        
        # free up memory
        # log.info("run.py: start running sudo systemctl isolate multi-user.target")
        # returnCode = subprocess.call(args=[sshCommand,"echo %s | sudo systemctl isolate multi-user.target" % name], stdout= logPipeInfo, stderr= logPipeError, shell=True)
        # log.debug("run.py: sudo systemctl isolate multi-user.target finished with returncode:  %s"%returnCode)
        
        runProcesses.append((subprocess.Popen( processCommandArray, stdout= logPipeInfo, stderr=logPipeError), name))
        logging.info(name + " process started")

    idx = 0

    while any(runProcesses):
        for stoppedProcess in filter(lambda paramList: paramList[0].poll() is not None, runProcesses):
            process, name = stoppedProcess
            # assert (), name + " has crashed"
            if process.returncode  is not 0: logging.critical(name + " does not have a return code 0")
            logging.debug(name +" started to stop")
            runProcesses.remove(stoppedProcess)
            try:
                process.wait()
            except KeyboardInterrupt:
                try:
                    process.terminate()
                except OSError:
                    pass
                process.wait()
            killLogResources(name)
            logging.info(name +" Stopped")
            
        # animation
        bar = list("-----------")
        bar[idx % len(bar)] = '|'
        print('\t['+"".join(bar)+ ']', end="\r")
        idx+=1
        time.sleep(0.1)

    successfullyFinished = True
    logging.debug("active thread Count: " + str(threading.active_count()))
    print("run.py successfully finished")
    time.sleep(0)
    exit()
except KeyboardInterrupt as identifier:
    print("program interpupted by using ctrl+c")
    logging.fatal("process is being terminated because keyboardInterrupt")
    exit()
except AssertionError as identifeir:
    logging.fatal("a remote has crashed")
    exit()
finally:
    if not successfullyFinished:
        logging.fatal("ending all life of initiated program")
        for process, name in runProcesses:
            logging.fatal("killing program at a remote: "+ name)
            getRemoteLogging(name).fatal("process is being terminated by run.py")
            process.kill()
    
        for process, name in runProcesses:
            process.wait()
            logging.fatal("program terminated at remote: "+ name)
        
        print("run.py abruptly ended")
    toTerminate = [key for key in logResources]
    for content in toTerminate:
        # log, fh, logPipeInfo, logPipeError = logResources[content]
        killLogResources(content)
        logging.info("ended log process for {name}".format(name = content))
    logging.info("all logging process ended")
    
    
