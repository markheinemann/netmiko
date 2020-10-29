from __future__ import unicode_literals, print_function
import time
from netmiko import ConnectHandler, redispatch
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import pprint
import textfsm


#someone asked me for the mac addresses for a selected list of ip addresses on a switch.
#I could have just entered  the simple cli command "show ip arp ", copied the output into excel and pulled out the requested data
#instead this python script will perform the filter and output ONLY the requested data, saving  very little time;)
#this script will return a list of mac addresses against a selected list of ip addresses as defined in iplist.txt
#this script wil call devices.txt and iplist.txt
#it will ssh through the corporate jumpbox and establish ssh connection with the switch address in devices.txt
#it will convert the output of 'show ip arp' to structured data using textfsm
#the script will search through iplist.txt and find matches against the switch structured data output

# if you get a keygen error, then  remove the host from the 'known_hosts' file  in the JumppBox
#[u3238123@plgsassec12301 .ssh]$ pwd
#/home/u3238123/.ssh
#eg   [u3238123@plgsassec12301 .ssh]$ ssh-keygen -R x.x.x.x

username = input("Terminal Server Username: r3-core\\")
password = getpass('Terminal Server Exec Password: ')
prvaccount = input("r1-core PRV account name: ")
secret = getpass('PRV  password:  ')

var1 = "r3-core\\"
var2 = username
var3 = var1 + var2
print (var3)
username = var3

prvaccount = "r1-core\\\\" + prvaccount


# terminal server creds
ssh_device = {

    'device_type': 'terminal_server',
    'ip': '10.116.15.125',
    'username': username,
    'password': password,
    'secret': secret,
    'port': 22,
}


devices = open('devices.txt', 'r')
devices = devices.read()
devices = devices.strip().splitlines()



iplist = open('iplist.txt', 'r')
iplist = iplist.read()
iplist = iplist.strip().splitlines()



for device in devices:
    try:
# connect to terminal server
        print('-' * 79)
        print('connecting to device', device)

        net_connect = ConnectHandler(**ssh_device)
        print ("SSH prompt: {}".format(net_connect.find_prompt()))


# now ssh to the end device using prv account creds
        #net_connect.write_channel("ssh -o StrictHostKeyChecking=no -l r1-core\\\prvmhein " + device + '\n')
        net_connect.write_channel("ssh -o StrictHostKeyChecking=no -l " + prvaccount + " " + device + '\n')
        time.sleep(2)
        output = net_connect.read_channel()

        print(output)
    

        if 'ssword' in output:
            net_connect.write_channel(secret + '\r\n')

            time.sleep(2)
            output = net_connect.read_channel()
# Did we successfully login

        net_connect.write_channel('\r\n')

        time.sleep(2)

        redispatch(net_connect, device_type='cisco_nxos')

        net_connect.enable()
 # get output from show ip arp and convert to structured data       
        output = net_connect.send_command("show ip arp", use_textfsm=True)
        #output = net_connect.send_config_set(commands)
        l2 = len(output)
        l = len(iplist)
        print("total entries in user list ( iplist.txt ) =  " + str(l))
        print("total entries output from device =  " + str(l2))
        print("for each entry in iplist.txt, search for matching entry in device arp ip arp table...")
        pprint.pprint(output) 
        print("******************************")

# search for matches and print when there is a match
        for ipaddress in iplist:
            for count in range (l2):
                ip = output[count] ['address']
                mac = output[count] ['mac']
                if ip == ipaddress:
                    print(ip, end="   ")
                    print(mac)

        net_connect.disconnect()

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



