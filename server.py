from typing import Union
from fastapi import FastAPI, WebSocket
import uvicorn
import json

# Import files
from constants import *
from socket_connection import SocketConnection

# Initialize fastapi app
app = FastAPI()

@app.get("/")
def root():
    return 'server is running and reachable!'

@app.get("/update-device")
async def update_client(deviceID: str, clientID: str, settings: str):    
    # Check if all arguments are supplied
    if not (deviceID or clientID or settings):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return 'device could not be found', 400

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return 'no permission to update', 405
    
    print(settings)

    # Send update data to device
    await socketConnection.send(deviceID, settings)

    # Return success code
    return '', 204

@app.get("/get-device")
async def get_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return 'device could not be found', 400

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return 'no permission to update', 405

    data = {
        'op': 'get-settings'
    }

    # Send data request to the device 
    await socketConnection.send(deviceID, json.dumps(data))

    # Receive data from device
    data = await socketConnection.receive(deviceID)

    # Return data to client
    return data

@app.get("/add-client")
async def add_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return 'device could not be found', 400

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return 'no permission to update', 405

    # Add clientID to the permissions for deviceID
    devicePermissions[deviceID].append(clientID)

    # Return success code
    return '', 204

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await socketConnection.handler(websocket)

# Permissions of the client identifiers and their devices
devicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Start socket connection
socketConnection = SocketConnection();

# Run uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
