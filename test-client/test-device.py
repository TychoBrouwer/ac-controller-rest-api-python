# import socket
import asyncio
import websockets

# Import constants files
from constants import *

async def socket_connection():
    # Connect to websocket
    async with websockets.connect(f'wss://{SERVER_SOCKET_ADDRESS}') as websocket:
        # Receive server conformation
        res = (await websocket.recv()).decode("utf-8")
        print(res)

        # Send device identifier to server
        await websocket.send(str.encode('DEVICE IDENTIFIER'))

        while True:
            # Receive data from server
            res = (await websocket.recv()).decode("utf-8")
            print(res)

            # If get settings request is received send settings to server  
            if res == 'get-settings':
                # ClientSocket.send(str.encode('DEVICE IDENTIFIER'))
                await websocket.send(str.encode('DEVICE IDENTIFIER'))

# Start socket connection function
asyncio.run(socket_connection())
