import socket

# Import constants files
from constants import *

# Initiate socket
ClientSocket = socket.socket()

# Connect to server socket
print('Waiting for connection response')
try:
    # ClientSocket.connect((SERVER_ADDRESS, SERVER_SOCKET_PORT))
    ClientSocket.connect((SERVER_IP, SERVER_SOCKET_PORT))
except socket.error as e:
    print(str(e))

# Send unique device identifier
ClientSocket.send(str.encode('DEVICE IDENTIFIER'))

while True:
    # Receive data from server
    res = ClientSocket.recv(2048).decode('utf-8')
    print(res)

    # If get settings request is received send settings to server  
    if res == 'get-settings':
        ClientSocket.send(str.encode('DEVICE IDENTIFIER'))

ClientSocket.close()
