from __future__ import unicode_literals, print_function
import time
from netmiko import ConnectHandler, redispatch
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass


# this sceript wil call devices.txt and take a .txt config snapshot of each device in the list
# if you get a keygen error, then  remove the host from the 'known_hosts' file  in the JumppBox
#[u3238608@plgsassecste01 .ssh]$ pwd
#/home/u3238608/.ssh
#eg   [u3238608@plgsassecste01 .ssh]$ ssh-keygen -R 10.127.242.1



username = input("Terminal Server Username: r3-core\\")
password = getpass('Terminal Server Exec Password: ')
prvaccount = input("r1-core PRV account name: ")
secret = getpass('PRV  password:  ')

var1 = "r3-core\\"
var2 = username
var3 = var1 + var2
print (var3)
username = var3





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





for device in devices:
    try:

        print('-' * 79)
        print('connecting to device', device)

        net_connect = ConnectHandler(**ssh_device)
        print ("SSH prompt: {}".format(net_connect.find_prompt()))



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

        print(output)
       

        redispatch(net_connect, device_type='cisco_ios')

        net_connect.enable()
        hostname = net_connect.send_command('show run | inc hostname')
        hostname.split(" ")
        col1, col2 = hostname.split(" ")
        filename = col2 + '.txt'
       
        filename = (filename.replace("\n", " "))
        
        print(filename)

        showrun = net_connect.send_command('show run')

        log_file = open(filename, "a")   # in append mode
        log_file.write(showrun)
      
        net_connect.disconnect()

    except ValueError:
        print('authentication failed to ', device)
        continue
    except NetMikoTimeoutException:
        print('device not reachable', device)
        continue
    except NetMikoAuthenticationException:
        print('auth failure', device)
        continue

