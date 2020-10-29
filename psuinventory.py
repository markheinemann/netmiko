from __future__ import unicode_literals, print_function
import time
from netmiko import ConnectHandler, redispatch
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import pprint
import textfsm


#
#this script wil call devices.txt 
#it will ssh through the corporate jumpbox and establish ssh connection with the switch address in devices.txt
#it will convert the output of 'show invent' to structured data using textfsm
#the script will parse the data and return all the psus and their serials
# will write output to a .txt
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



#iplist = open('iplist.txt', 'r')
#iplist = iplist.read()
#iplist = iplist.strip().splitlines()



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
        hostname = net_connect.send_command('show run | inc hostname')
        hostname.split(" ")
        col1, col2 = hostname.split(" ")
        filename = col2 + '.txt'
        filename = (filename.replace("\n", " "))
        
        print(filename)


 # get output from show ip arp and convert to structured data       
        output = net_connect.send_command("show inventory", use_textfsm=True)
        #output = net_connect.send_config_set(commands)
        l2 = len(output)
        #l = len(iplist)
        #print("total entries in user list ( iplist.txt ) =  " + str(l))
        print("total entries output from device =  " + str(l2))
        #print("for each entry in iplist.txt, search for matching entry in device arp ip arp table...")
        #pprint.pprint(output) 
        print("******************************")


        #print (output)

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
                    #hostname = net_connect.send_command('show run | inc hostname')
                    #hostname.split(" ")
                    #col1, col2 = hostname.split(" ")
                    #filename = col2 + '.txt'
       
        #filename = (filename.replace("\n", " "))
        
        #print(filename)

        #showrun = net_connect.send_command('show run')

        #log_file = open(filename, "a")   # in append mode
        #log_file.write(psu)



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



