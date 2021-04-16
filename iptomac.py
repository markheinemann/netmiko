#someone asked me for the mac addresses for a selected list of ip addresses on a switch.
#I could have just entered  the simple cli command "show ip arp ", copied the output into excel and pulled out the requested data
#instead this python script will perform the filter and output ONLY the requested data, saving  very little time;)
#this script will return a list of mac addresses against a selected list of ip addresses as defined in iplist.txt
#this script will call devices.txt and iplist.txt. These are simple .txt files with entry on each line
#it will then establish an ssh connection with the switch address in devices.txt
#it will convert the output of 'show ip arp' to structured data using textfsm
#the script will search through iplist.txt and find matches against the switch structured data output


from __future__ import unicode_literals, print_function
import time
import netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import pprint
import textfsm

devices = open('devices.txt', 'r')
devices = devices.read()
devices = devices.strip().splitlines()



iplist = open('iplist.txt', 'r')
iplist = iplist.read()
iplist = iplist.strip().splitlines()


device_type = 'cisco_nxos'
username = 'xxxxxxxxxx'
password = 'yyyyyyyyyy'
ssh_config_file = '/etc/ssh/ssh_config'


for device in devices:
	try:
# connect to terminal server
		print('-'*79)
		print('connecting to device', device)
		connection = netmiko.ConnectHandler(ip=device, device_type=device_type,
		                                username=username, password=password, ssh_config_file=ssh_config_file)
		print(connection)

		# get output from show ip arp and convert to structured data       
		output = connection.send_command("show ip arp", use_textfsm=True)
		#output = net_connect.send_config_set(commands)
		l2 = len(output)
		l = len(iplist)
		print("total entries in user list ( iplist.txt ) =  " + str(l))
		print("total entries output from device =  " + str(l2))
		print("for each entry in iplist.txt, search for matching entry in device arp ip arp table...")
        #print complete structured output of 'show ip arp'
		pprint.pprint(output) 
		print("******************************")

		# search for matches and print when there is a match
		for ipaddress in iplist:
		    for count in range (l2):
		        ip = output[count] ['address']
		        mac = output[count] ['mac']
		        interface = output[count]['interface']
		        if ip == ipaddress:
                    #print output if there is a match
		            print(ip, end="   ")
		            print(mac, end="  ")
		            print(interface,)

		connection.disconnect()

	#error control
	except ValueError:
	    print('authentication failed to ', device)
	    continue
	except NetMikoTimeoutException:
	    print('device not reachable', device)
	    continue
	except NetMikoAuthenticationException:
	    print('auth failure', device)
	    continue



