from _thread import *
import asyncio
import websockets

# Currently connected devices
class SocketConnection:
    def __init__(self, port):
        self.devices = {}
        
        start_new_thread(asyncio.run, (self.socket_connection(port),))

    def from_id(self, deviceID):
        return self.devices[deviceID]

    def connected(self, deviceID):
        return deviceID in self.devices

    async def send(self, deviceID, data):
        # Send server connection conformation to device
        await self.devices[deviceID].send(data)

    async def receive(self, deviceID):
        # Send server connection conformation to device
        data = (await self.devices[deviceID].recv()).decode("utf-8")

        return data

    async def socket_handler(self, websocket):
        # Send server connection conformation to device
        await websocket.send(str.encode('Server is working!'))

        # Receive device identifier from device
        deviceID = (await websocket.recv()).decode("utf-8")
        if deviceID:
            # Store device identifier in currently connected dict
            self.devices[deviceID] = websocket
            print(f'new device connection: {websocket.remote_address}, {deviceID}')

        # Keep websocket connection open
        while True:
            await asyncio.sleep(1)

    async def socket_connection(self, port):
        # Serve websocket on all network interfaces at selected port
        async with websockets.serve(self.socket_handler, "", port):
            await asyncio.Future()  # run socket forever
