# l2 to l3 switchport mapper
# this script will query' show ip arp' on L3 switch, with ' show mac address-table' on connected L2 switch
# and write matching data to xls
# omitting any macs that are coming from upstream


from __future__ import absolute_import, division, print_function
import netmiko
from netmiko import ConnectHandler
import json
import xlsxwriter
from getpass import getpass



#L3 switch ip address
l3device ='1.2.3.4'
#l2 switch ip address
l2device = '5.6.7.8'


hostname = input(" for filename - l2 switch hostname ?  :")
# omitting any macs that are coming from upstream. They are not required to be in output file
po = input("ommit uplink port-channel number ?  :")



device_type = 'cisco_nxos'
username = 'xxxxxxxxx'
password = getpass ('password ? :')
ssh_config_file = '/etc/ssh/ssh_config'


print('-'*79)
print('connecting to device', l3device)
connection = netmiko.ConnectHandler(ip=l3device, device_type=device_type,
                                        username=username, password=password, ssh_config_file=ssh_config_file)
print(connection)

#convert output to structured python dictionary
l3data = connection.send_command('show ip arp',use_textfsm=True )


print('connecting to device', l2device)
connection = netmiko.ConnectHandler(ip=l2device, device_type=device_type,
                                        username=username, password=password, ssh_config_file=ssh_config_file)
print(connection)

#convert output to structured python dictionary
l2data = connection.send_command('show mac address-table',use_textfsm=True )


workbook = xlsxwriter.Workbook(hostname + ".xlsx")
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})

row = 0
col=0	

#headers for xls
worksheet.write(row,col,	"HOST", bold)
worksheet.write(row,col+1, "MAC", bold)
worksheet.write(row,col+2, "IP ADDRESS", bold)
worksheet.write(row,col+3, "PORT", bold)	
row += 1	


# captute macs from Eth ports

for macl3 in l3data:
	for macl2 in l2data:
		if macl3['mac']==macl2['mac']:
			if macl2['ports'].startswith("Eth"):
			
				print(macl3['mac'], end="  ")
				print(macl3['address'], end="  ")
				print(macl2['mac'], end="  ")
				print(macl2['ports'])
				print("***********************")
				xlsmac=macl2['mac']
				xlsaddress=macl3['address']
				xlsport=macl2['ports']
				worksheet.write(row,col,	hostname + " : "  + l2device)
				worksheet.write(row,col+1,	xlsmac)
				worksheet.write(row,col+2,	xlsaddress)
				worksheet.write(row,col+3,	xlsport)
				row += 1
				

# capture macs from port channels

uplink = "Po"+po

for macl3 in l3data:
	for macl2 in l2data:
		if macl3['mac']==macl2['mac']:
			if macl2['ports'].startswith(uplink):
				pass
			elif macl2['ports'].startswith("vPC"):
				pass
			elif macl2['ports'].startswith("Eth"):
				pass
			else:	
				print(macl3['mac'], end="  ")
				print(macl3['address'], end="  ")
				print(macl2['mac'], end="  ")
				print(macl2['ports'])
				print("***********************")
				xlsmac=macl2['mac']
				xlsaddress=macl3['address']
				xlsport=macl2['ports']
				worksheet.write(row,col,	hostname + " : "  + l2device)
				worksheet.write(row,col+1,	xlsmac)
				worksheet.write(row,col+2,	xlsaddress)
				worksheet.write(row,col+3,	xlsport)
				row += 1




workbook.close()


connection.disconnect()
