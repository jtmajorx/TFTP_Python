from sys import argv
import csv
import getpass
import netmiko
from netmiko import ConnectHandler
from netmiko import Netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
# Creditials
username = input('Username: ')
password = getpass.getpass('Password: ')
# enablepw = getpass.getpass("Enable Password? ")

# File parameters
tftpsrv = input('TFTP Server: ')
filename = input('File to load into running-config: ')

# Format csv
script, csv_file = argv
reader = csv.DictReader(open(csv_file, 'rt'))

# Import nodes
all_nodes = []
for line in reader:
    all_nodes.append(line)

# Download tftp file, save config
for devices in all_nodes:
    devices['username'] = username
    devices['password'] = password
    hostname = devices['host']
    try:
        net_connect = Netmiko(
            **devices,
            device_type = 'cisco_ios_ssh',
            port = '22',
            global_delay_factor=2
            )
        output = net_connect.send_command('copy tftp://%s/%s running-config' %(tftpsrv,filename),expect_string=r'running-config' )
        output += ('\n\n')
        output += net_connect.send_command('\n', expect_string=r'OK|Error')
        print(f"\n\n--------- TFTP cmd sent to %s ---------" %hostname)
        print(output)
        net_connect.disconnect()
    except:
        try:
            net_connect = Netmiko(
                **devices,
                device_type = 'cisco_ios_telnet',
                port = '23',
                global_delay_factor=10
                )
            output = net_connect.send_command('copy tftp://%s/%s running-config' %(tftpsrv,filename),expect_string=r'running-config' )
            output += ('\n\n')
            output += net_connect.send_command('\n', expect_string=r'OK|Error')
            print(f"\n\n--------- TFTP cmd sent to %s ---------" %hostname)
            print(output)
            net_connect.disconnect()
        except:
            print('***ERROR***Cannot connect to %s.' %hostname)
