# import socket
from _thread import *
from flask import Flask, request
import asyncio
import websockets

# Import constants files
from constants import *

# Initialize flask server
app = Flask(__name__)

@app.route("/")
def server_running():
    return 'Server running!', 200

@app.route("/update-device", methods=['GET'])
async def update_client():
    # Get the request data
    DeviceID = request.args.get('DeviceID')
    ClientID = request.args.get('ClientID')
    Data = request.args.get('Data')

    # Check if all arguments are supplied
    if not (DeviceID or ClientID or Data):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if DeviceID not in Devices:
        return 'device could not be found', 400

    # Check if client has permission
    if ClientID not in DevicePermissions[DeviceID]:
        return 'no permission to update', 405
    
    # Send update data to device
    await socket_send(Devices[DeviceID], str.encode(Data))

    # Return success code
    return '', 204

@app.route("/get-device", methods=['GET'])
async def get_client():
    # Get the request data
    DeviceID = request.args.get('DeviceID')
    ClientID = request.args.get('ClientID')

    # Check if all arguments are supplied
    if not (DeviceID or ClientID):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if DeviceID not in Devices:
        return 'device could not be found', 400

    # Check if client has permission
    if ClientID not in DevicePermissions[DeviceID]:
        return 'no permission to update', 405
    
    # Send data request to the device 
    await socket_send(Devices[DeviceID], str.encode('get-settings'))

    # Receive data from device
    data = await socket_receive(Devices[DeviceID])
    
    # Return data to client
    return data

async def socket_send(websocket, data):
    # Send server connection conformation to device
    await websocket.send(data)

async def socket_receive(websocket):
    # Send server connection conformation to device
    data = (await websocket.recv()).decode("utf-8")

    return data

async def socket_handler(websocket):
    # Send server connection conformation to device
    await socket_send(websocket, str.encode('Server is working!'))

    # Receive device identifier from device
    DeviceID = await socket_receive(websocket)
    if DeviceID:
        # Store device identifier in currently connected dict
        Devices[DeviceID] = websocket
        print(f'new device connection: {DeviceID}')

    # Keep websocket connection open
    while True:
        await asyncio.sleep(1)

async def socket_connection():
    # Serve websocket on all network interfaces at selected port
    async with websockets.serve(socket_handler, "", SERVER_SOCKET_PORT):
        await asyncio.Future()  # run socket forever

# Permissions of the client identifiers and their devices
DevicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Currently connected devices
Devices = {}

if __name__ == "__main__":
    # Start websocket in new thread
    start_new_thread(asyncio.run, (socket_connection(),))

    # Start Flask app
    app.run(host=SERVER_IP, port=SERVER_FLASK_PORT)
