import asyncio


class SocketManager:
    def __init__(self):
        # Currently connected devices
        self.devices = {}

    def connected(self, deviceID):
        return deviceID in self.devices

    async def send(self, deviceID, data):
        # Send server connection conformation to device
        await self.devices[deviceID].send_text(data)

    async def receive(self, deviceID):
        # Send server connection conformation to device
        data = await self.devices[deviceID].receive_text()

        return data

    async def add(self, deviceID, websocket):
        if deviceID:
            # Store device identifier in currently connected dict
            self.devices[deviceID] = websocket
            print(
                f'new device connection: {websocket.client.host}:{websocket.client.port}, {deviceID}')

    async def handler(self, websocket):
        # Send server connection conformation to device
        await websocket.send_text('Server is working!')

        # Receive device identifier from device
        deviceID = await websocket.receive_text()

        try:
            while True:
                if deviceID:
                    asyncio.create_task(self.add(deviceID, websocket))
                await asyncio.sleep(1)
        except websocket.WebSocketDisconnect:
            # Remove device from currently connected dict
            del self.devices[deviceID]
            print(
                f'device disconnected: {websocket.client.host}:{websocket.client.port}, {deviceID}')
