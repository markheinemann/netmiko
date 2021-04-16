# script will ssh to a device and parse through " show interfaces command " printing out
# some parameters to a csv file
# uses genie parsers



from __future__ import absolute_import, division, print_function
import netmiko
from netmiko import ConnectHandler
import json
from pprint import pprint
import csv
from getpass import getpass

# simple netmiko script
#device ip address
device ='1.2.3.4'

##working  path - jumping  transparently thru ssh  jump server ##
device_type = 'cisco_nxos'
username = 'xxxxxxxxx'
print("username : " + username )
password = getpass ('password ?: ')
ssh_config_file = '/etc/ssh/ssh_config'


print('-'*79)
print('connecting to device', device)
connection = netmiko.ConnectHandler(ip=device, device_type=device_type,
                                        username=username, password=password, ssh_config_file=ssh_config_file)
print(connection)

#convert output to structured python dictionary
data = connection.send_command('show interface',use_genie=True )


# then convert to json format and display
#print(json.dumps(data, indent=2))


#  writing to an xls
interface_file = "my_interfaces.csv"
report_fields=["INTERFACE", "IN_PKTS", "LOAD_INTERVAL"]


with open(interface_file, "w") as f:
	writer=csv.DictWriter(f, report_fields)
	writer.writeheader()
	for interface,details in data.items():
		if interface.startswith("Ethernet"):
			writer.writerow(
				{"INTERFACE" : interface,
			 	"IN_PKTS" : details["counters"]["in_pkts"],
			 	"LOAD_INTERVAL" : details["counters"]["rate"]["load_interval"]}
			 	) 
		


connection.disconnect()
