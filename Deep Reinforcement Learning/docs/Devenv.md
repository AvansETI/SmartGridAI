1. Generate SSH-keys on each development client device (student laptops) (password is strongly advised)
```
	ssh-keygen -t rsa -b 4096
```
2. Enable ssh-agent (see note at bottom) and add key
```
	ssh-add
```
3. Install ssh keys on $UNAME@sendlab.avansti.nl:10022 -> ~/.ssh/authorized_keys
4. Create a devenv user and a user account for each dev on SmartGrid server
5. Install ssh keys of each user on their respective account and allow devenv to read -> ~/.ssh/authorized_keys
6. On client device (student laptops) edit in user folder -> .ssh/config
```
	Host sendlab_jumphost
		HostName sendlab.avansti.nl
		Port 10022
		User smartgridai

	Host smartgrid_$UNAME
		HostName 192.168.5.22
		Port 22
		User $UNAME
		ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe sendlab_jumphost netcat -w 120 %h %p

	Host smartgrid_$DEV_ENV
		HostName 172.22.0.1
		Port $PORT
		User $UNAME
		ForwardAgent yes
		RequestTTY force
		RemoteCommand exec bash
		ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe smartgrid_$UNAME netcat -w 120 %h %p
```
7. Connect
```
	ssh smartgrid_$DEV_ENV
```

Use devenv script to manage development environments.

Add SSH key to github. 

	1. Windows + r > .ssh > Edit id_rsa.pub and copy the key. 
	2. Profile settings on github > SSH & GPG Keys > Add new key > Paste key.

Fix Windows' outdated SSH-Agent:

	1. Install Chocolatey: https://chocolatey.org/install
	2. CMD: SC STOP ssh-agent & SC DELETE ssh-agent
	3. PS/CMD: choco install -y openssh -params '"/SSHAgentFeature"'