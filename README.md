-some cisco netmiko scripts that are useful for networking tasks <br /><br />

 <b>1) send-commands.py <br /><br /> </b>

-this netmiko script will call devices.txt and commands.txt <br />
-devices.txt is a list of ip addresses.one address on each line <br />
-commands.txt is a list of config commands. One command on each line <br />
-all the commands will be sent to every ip address in enable mode/ conf t <br />
-tested on python3.7

<b>2)  ciscobackup.py</b>


-this netmiko script will call devices.txt and commands.txt <br />
-devices.txt is a list of ip addresses.one address on each line <br />
- script will log into each device in devices.tx via an intermediate unix terminal server ( Bastion host )<br />
-the terminal server address can be chnaged within the script<br /><br />



if you get a keygen error, then  remove the host from the 'known_hosts' file  in the terminal server<br />
#[u3212308@plgsasse123401 .ssh]$ pwd<br />
#/home/u3212308/.ssh<br />
#eg   [u3212308@plgsasse123401 .ssh]$ ssh-keygen -R x.x.x.x   where x.x.x.x is the ip address of the destination device<br /><br />


-script will prompt the user for creds - These are necessary and particular to my company's security standards<br /><br />

Terminal Server Username: r3-core\ <br />
Terminal Server Exec Password:<br />
PRV  password:<br />  ( this is the enable password


<b>3) iptomac.py</b></br>

-someone asked me for the mac addresses for a selected list of ip addresses on a cisco switch.</br>
-I could have just entered  the simple cli command "show ip arp ", copied the output into excel and pulled out the requested data</br>
-instead this python script will perform the filter and output ONLY the requested data, saving  very little time;)</br>
-this script will return a list of mac addresses against a selected list of ip addresses as defined in iplist.txt</br>
-this script wil call devices.txt and iplist.txt</br>
-it will ssh through the corporate jumpbox( bastion host security measure ) and establish ssh connection with each  switch address in devices.txt</br>
-it will convert the output of 'show ip arp' to structured data using the python library textfsm</br>
-the script will then search through iplist.txt and find matches against the switch structured data output</br>

-if you get a keygen error, then  remove the host from the 'known_hosts' file  in the terminal server<br />
-[u3212308@plgsasse123401 .ssh]$ pwd<br />
-/home/u3212308/.ssh<br />-
-eg   [u3212308@plgsasse123401 .ssh]$ ssh-keygen -R x.x.x.x   where x.x.x.x is the ip address of the destination device<br /><br />

-script will prompt the user for creds - These are necessary and particular to my company's security standards<br /><br />

-Terminal Server Username: <br />
-Terminal Server Exec Password:<br />
-r1-core PRV account name:<br />
-PRV  password:<br />

