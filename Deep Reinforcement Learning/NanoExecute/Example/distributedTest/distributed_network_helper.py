import socket, json, os, argparse, logging, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' #1 = suppress tf info messages, 2 = supres warnings, 3 = supress all
loggingFormat = '%(levelname)s\t %(name)s %(filename)s %(funcName)s() [%(lineno)d]: \t%(message)s'
logging.basicConfig(format=loggingFormat, level=logging.DEBUG, stream= sys.stdout)
import tensorflow as tf

def getIpsFromArgs():
  """helpFunctie om ip's als een option van de command line te halen
  vb: DistributedTest2.py worker_ips 192.168.1.1 192.168.1.2
  vb: DistributedTest2.py --chief_ips 192.168.1.12 worker_ips 192.168.1.1 192.168.1.2"""
  workerIps = None
  chiefIps = None
  paramServerIps = None

  parser = argparse.ArgumentParser(description='run distributed training script on this computer')
  parser.add_argument('-w', '--worker_ips', nargs='+', required=True,
    help='all the workers in the training pool. first ip is chief if not otherwise specified')
  parser.add_argument('-c', '--chief_ips', nargs='+',
    help='chief workers are special')
  parser.add_argument('-p', '--parameter_server', nargs='+',
    help='the server that distributes and accumulates all the weights')
  
  args = parser.parse_args()
  workerIps = args.worker_ips
  chiefIps = args.chief_ips
  paramServerIps = args.parameter_server
  print("commands received on w:" + str(workerIps) + " c:" + str(chiefIps) + " p:" + str(paramServerIps))

  return (workerIps, chiefIps, paramServerIps)

def initDistributedNetwork(workerIps, chiefIps = None, paramServIp = None, port = 39202):
  logging.debug("network received w:" + str(workerIps) + " c:" + str(chiefIps) + " p:" + str(paramServIp))

  #make list of ip:port from ip list
  def makeIpPortArray(ips):
    ipPortArray = []
    if ips is None: return ipPortArray
    for ip in ips:
      ipPort = "%s:%d" % (ip,port) 
      ipPortArray.append(ipPort)
    return ipPortArray

  #assing to all the variables
  workerArray = makeIpPortArray(workerIps)
  chiefArray = makeIpPortArray(chiefIps)
  paramServArray = makeIpPortArray(paramServIp)

  #find current computr ip adrs
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
  IPAddr = s.getsockname()[0]
  
  currentWorkerId = 0
  ipPort = "%s:%d" % (IPAddr, port)
  try:
    allMachines = []
    allMachines.extend(chiefArray)
    allMachines.extend(paramServArray)
    allMachines.extend(workerArray) 

    currentWorkerId = allMachines.index(ipPort)
  except(ValueError):
    print("current ip address + port ('%s') is not in worker or chief array " % ipPort)
    exit()

  isMainChief = currentWorkerId is 0
  isChief = chiefIps is not None and IPAddr in chiefIps
  isWorker = workerIps is not None and IPAddr in workerIps
  isParamWorker = paramServIp is not None and IPAddr in paramServIp

  taskWorkerType = 'worker'
  if isChief: taskWorkerType = 'chief'
  if isParamWorker: taskWorkerType = 'ps'

  clusterArg = {'worker': workerArray}
  if chiefArray is not None and len(chiefArray) > 0:
    clusterArg['chief'] = chiefArray
  if paramServArray is not None and len(paramServArray) > 0:
    clusterArg['ps'] = paramServArray

  os.environ['TF_CONFIG'] = json.dumps({
    'cluster': clusterArg,
    'task': {'type': taskWorkerType, 'index': currentWorkerId}
  })
  logging.debug("TF_CONFIG = "+str(os.environ['TF_CONFIG']))

  #%% defineer strategie en initialiseer
  strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(device="/gpu:0") 

  return (strategy, isMainChief, isChief , isWorker, isParamWorker)
