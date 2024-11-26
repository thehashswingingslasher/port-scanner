import socket
from termcolor import colored

def scan(ipaddress, port):
  try:
    sock = socket.socket()
    sock.connect((ipaddress, port))
    serviceversion = sock.recv(1024)
    serviceversion = serviceversion.decode('utf-8')
    serviceversion = serviceversion.strip('\n')
    portstate = f'Port {str(port)} is open'
    print(colored(portstate, 'green'), end= '    ')
    print(serviceversion)
    print(f'Port {str(port)} is open')
  except ConnectionRefusedError:
    print(colored(f'Port {str(port)} is closed', 'red'))
  except UnicodeDecodeError:
    print(colored(f'Port {str(port)} is open', 'green'))

target = input('Target: ')
ports = input('Port: ')

if ',' in ports:
  portlist = ports.split(',')
  for port in portlist:
    scan(target, int(port))
elif '-' in ports:
  portrange = ports.split('-')
  start = int(portrange[0])
  end = int(portrange[1])
  for port in range(start, end+1):
    scan(target,port)
else:
  scan(target, int(ports))
