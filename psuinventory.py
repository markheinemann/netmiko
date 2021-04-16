#this script wil call devices.txt 
#it will establish ssh connections with the switch addresses in devices.txt
#it will convert the output of 'show invent' to structured data using textfsm
#the script will parse the data and return all the psus and their serials
# will write output to a .txt


from __future__ import unicode_literals, print_function
import time
import netmiko
from netmiko import ConnectHandler, redispatch
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import pprint
import textfsm


device_type = 'cisco_nxos'
username = 'r1-core\\prvmhein'
password = 'lmJKQ$NhrZ%3p4'
ssh_config_file = '/etc/ssh/ssh_config'


devices = open('devices.txt', 'r')
devices = devices.read()
devices = devices.strip().splitlines()



for device in devices:
    try:
        print('connecting to device', device)
        connection = netmiko.ConnectHandler(ip=device, device_type=device_type,
                    username=username, password=password, ssh_config_file=ssh_config_file)
        print(connection)
        hostname = connection.send_command('show run | inc hostname')
        hostname.split(" ")
        col1, col2 = hostname.split(" ")
        filename = col2 + '.txt'
        filename = (filename.replace("\n", " "))       
        print(filename)


 # get output from show inventory and convert to structured data 
        output = connection.send_command("show inventory", use_textfsm=True)      
        l2 = len(output)

        print("******************************")


# search for matches and print when there is a match
        p = "Power"
        for count in range (l2):
                psu = output[count] ['name']
                serial = output[count] ['sn']
                
                if p in psu:
                    print(device, end="   ")
                    print(psu, end="   ")
                    print(serial)
                    

                    log_file = open(filename, "a")   # in append mode
                    log_file.write(device)
                    log_file.write("\n")
                    log_file.write(psu)
                    log_file.write("\n")
                    log_file.write(serial)
                    log_file.write("\n")
                    log_file.write("\n")

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

