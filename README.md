-some cisco netmiko scripts that are useful for networking tasks <br /><br />

 1) send-commands.py <br /><br />

-this netmiko script will call devices.txt and commands.txt <br />
-devices.txt is a list of ip addresses.one address on each line <br />
-commands.txt is a list of config commands. One command on each line <br />
-all the commands will be sent to every ip address in enable mode/ conf t <br />
-tested on python3.7
