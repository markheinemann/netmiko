# simple netmiko script to log inbto a nexus and print out the running code version

from __future__ import absolute_import, division, print_function
import netmiko
from netmiko import ConnectHandler
import json
from getpass import getpass


#device ip address
device ='x.x.x.x'


device_type = 'cisco_nxos'
username = 'xxxxxxxxx'
print( " username : " + username )
password = getpass ('enter password: ')
ssh_config_file = '/etc/ssh/ssh_config'


print('-'*79)
print('connecting to device', device)
connection = netmiko.ConnectHandler(ip=device, device_type=device_type,
                                        username=username, password=password, ssh_config_file=ssh_config_file)
print(connection)

#convert output to structured python dictionary
data = connection.send_command('show ver',use_textfsm=True )


# then convert to json format and display
print(json.dumps(data, indent=2))


for k in data:
	print (k['os'])
	print(f"{k['hostname']} running code is {k['os']}")

	print( " the running code on " + k['hostname'] + " is "+ k['os'])


connection.disconnect()

