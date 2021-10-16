## NanoSetup

Nano's can be setup by running a few scripts found in the `NanoSetup` branch
Before running the scripts the Nano OS needs to be installed by using the getting started link from nvidea ([Found Here](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) we used version `r32.2.1`

***

1. First get the latest version of the `SmartGridSetup` branch found [here](https://github.com/RDAxRoadkill/SmartGridSetup) 
2. Move the `nanoInstall` folder to the wanted nano via ssh or pulling the github file. 
3. Run the `install.py` script from the nanoInstall folder by using `sudo -H python3 install.py` it's important to use python3 here since we need that version for various packages, and since both python 2.7 & 3.6 are standard installed on a Jetson Nano.
4. After a successful run the check.py script by using the same command `sudo -H python3 check.py`. A few notes about the check.py script:
* The script contains the hello world script for tensorflow, openaigym & logs into Weights&Biases
* OpenAIGym could end in an error if no Monitor is connected
* Weights&Biases pushes an empty run to our login, I recommend making your own and saving your API key somewhere. 
5. Both scripts should end successfully, it's been tested on version `r32.2.1`
6. For easy access in the future, you could also run the `SSH.py` script and change the public key's that are in that file to something you use.


***
voorbeeld ssh config met alle nano's

verander smartgrid_jacco naar persoonlijke jump

> Host nano1
> 	HostName 192.168.4.2
> 	User nano1
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano2
> 	HostName 192.168.4.3
> 	User nano2
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano3
> 	HostName 192.168.4.4
> 	User nano3
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano4
> 	HostName 192.168.4.5
> 	User nano4
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano5
> 	HostName 192.168.4.6
> 	User nano5
> 	ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano6
> 	HostName 192.168.4.7
> 	User nano6
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano7
> 	HostName 192.168.4.8
> 	User nano7
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano8
> 	HostName 192.168.4.9
> 	User nano8
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano10
> 	HostName 192.168.4.10
> 	User nano10
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

> Host nano11
> 	HostName 192.168.4.11
> 	User nano11
>   ForwardAgent yes
> 	RequestTTY force
> 	RemoteCommand exec bash
> 	ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_jacco netcat -w 120 %h %p

