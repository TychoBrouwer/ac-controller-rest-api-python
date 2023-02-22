# import socket
import asyncio
import websockets
import json

# Import constants files
from constants import SERVER_ADDRESS

settings = {
    'deviceID': 'DEVICE IDENTIFIER',
}

async def socket_connection():
    # Connect to websocket
    async with websockets.connect(f'wss://{SERVER_ADDRESS}/ws') as websocket:
        # Receive server conformation
        conf = await websocket.recv()
        print(conf)

        # Send device identifier to server
        await websocket.send(settings['deviceID'])

        while True:
            # Receive operation from server
            operation = json.loads(await websocket.recv())
            
            print(operation)
            print(operation['op'])
            print(type(operation))

            # If get settings request is received send settings to server  
            if operation['op'] == 'get-settings':
                await websocket.send(json.dumps(settings))

            if operation['op'] == 'update-settings':
                # settings = res['settings']
                print(operation['settings'])

# Start socket connection function
asyncio.run(socket_connection())
