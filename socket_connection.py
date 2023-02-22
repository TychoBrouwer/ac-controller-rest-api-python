import asyncio

# Currently connected devices
class SocketConnection:
    def __init__(self):
        self.devices = {}
        
    def connected(self, deviceID):
        return deviceID in self.devices

    async def send(self, deviceID, data):
        # Send server connection conformation to device
        await self.devices[deviceID].send_text(data)

    async def receive(self, deviceID):
        # Send server connection conformation to device
        data = await self.devices[deviceID].recv()

        return data

    async def socket_handler(self, websocket):
        # Send server connection conformation to device
        await websocket.send_text('Server is working!')

        # Receive device identifier from device
        deviceID = await websocket.receive_text()
        if deviceID:
            # Store device identifier in currently connected dict
            self.devices[deviceID] = websocket
            print(f'new device connection: {websocket.client}, {deviceID}')

        # Keep websocket connection open
        while True:
            await asyncio.sleep(1)
            
