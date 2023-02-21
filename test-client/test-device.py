# import socket
import asyncio
import websockets

# Import constants files
from constants import *

# # Initiate TCP socket
# ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# # Connect to server socket
# print('Waiting for connection response')
# try:
#     ClientSocket.connect((SERVER_ADDRESS, SERVER_SOCKET_PORT))
#     # ClientSocket.connect((SERVER_IP, SERVER_SOCKET_PORT))
# except socket.error as e:
#     print(str(e))

# # Send unique device identifier
# ClientSocket.send(str.encode('DEVICE IDENTIFIER'))

async def socket_connection():
    async with websockets.connect(f'ws://localhost:{SERVER_SOCKET_PORT}') as websocket:
        res = await websocket.recv()
        print(res)

        await websocket.send(str.encode('DEVICE IDENTIFIER'))

        while True:
            # Receive data from server
            res = await websocket.recv()
            print(res)

            # If get settings request is received send settings to server  
            if res == 'get-settings':
                # ClientSocket.send(str.encode('DEVICE IDENTIFIER'))
                await websocket.send(str.encode('DEVICE IDENTIFIER'))

asyncio.run(socket_connection())

# while True:
#     # Receive data from server
#     # res = ClientSocket.recv(2048).decode('utf-8')
#     print(res)

#     # If get settings request is received send settings to server  
#     if res == 'get-settings':
#         # ClientSocket.send(str.encode('DEVICE IDENTIFIER'))

# ClientSocket.close()
