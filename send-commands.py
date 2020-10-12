#this netmiko script will call devices.txt and commands.txt
#devices.txt is a list of ip addresses.one address on each line
#commands.txt is a list of config commands. One command on each line
#all the commands will be sent to every ip address in enable mode/ conf t
#tested on python3.7

from __future__ import absolute_import, division, print_function

from netmiko import ConnectHandler
from getpass import getpass

import netmiko

devices = open('devices.txt','r')
devices = devices.read()
devices = devices.strip().splitlines()

with open('commands.txt') as f:
    commands = f.read().splitlines()

device_type = 'cisco_ios'
username = input ("username: ")
password = getpass('exec password: ')
secret = getpass('enable password: ')

for device in devices:
        try:
                print('-'*79)
                print('connecting to device', device)
                net_connect = ConnectHandler(ip=device, device_type=device_type,
                                        username=username, password=password, secret=secret)
                net_connect.enable()
                output = net_connect.send_config_set(commands)
                print (output)
                print(net_connect.find_prompt())
                net_connect.disconnect()

        except  netmiko.ssh_exception.NetMikoTimeoutException:
            print('authentication failed to ', device)
