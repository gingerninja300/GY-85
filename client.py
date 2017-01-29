import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

#where to send data
SERVER_IP = '192.168.43.217'
PORT_NUMBER = 80

#defining socket to commmunicate through
server_socket = socket(AF_INET, SOCK_STREAM)
#testing connection
server_socket.connect(SERVER_IP, PORT_NUMBER)

while True:
  server_socket.sentto('data', (SERVER_IP, PORT_NUMBER))
  time.sleep(.5)
sys.exit()
