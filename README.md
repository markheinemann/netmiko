-some cisco netmiko scripts that are useful for networking tasks <br /><br />

 1) send-commands.py <br /><br />

-this netmiko script will call devices.txt and commands.txt <br />
-devices.txt is a list of ip addresses.one address on each line <br />
-commands.txt is a list of config commands. One command on each line <br />
-all the commands will be sent to every ip address in enable mode/ conf t <br />
-tested on python3.7

2)  ciscobackup.py


-this netmiko script will call devices.txt and commands.txt <br />
-devices.txt is a list of ip addresses.one address on each line <br />
- script will log into each device in devices.tx via an intermediate unix terminal server ( Bastion host )
-the terminal server address can be chnaged within the script



if you get a keygen error, then  remove the host from the 'known_hosts' file  in the terminal server
#[u3212308@plgsasse123401 .ssh]$ pwd
#/home/u3212308/.ssh
#eg   [u3212308@plgsasse123401 .ssh]$ ssh-keygen -R x.x.x.x   where x.x.x.x is the ip address of the destination device


-script will prompt the user for creds:

Terminal Server Username: r3-core\ 
Terminal Server Exec Password:
PRV  password:
