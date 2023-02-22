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
    return { 'code': 200, 'res': 'server is running and reachable!' }

@app.get("/update-device")
async def update_client(deviceID: str, clientID: str, operation):    
    # Check if all arguments are supplied
    if not (deviceID or clientID or operation):
        return { 'code': 400, 'res': 'not enough arguments supplied' }

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return { 'code': 400, 'res': 'device could not be found' }

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return { 'code': 405, 'res': 'no permission to update' }
    
    print(operation)

    # Send update data to device
    await socketConnection.send(deviceID, operation)

    # Return success code
    return { 'code': 200, 'res': 'successfully updated device' }

@app.get("/get-device")
async def get_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return { 'code': 400, 'res': 'not enough arguments supplied' }

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return { 'code': 400, 'res': 'device could not be found' }

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return { 'code': 405, 'res': 'no permission to update' }

    data = {
        'op': 'get-settings'
    }

    # Send data request to the device 
    await socketConnection.send(deviceID, json.dumps(data))

    # Receive data from device
    data = await socketConnection.receive(deviceID)

    # Return data to client
    return { 'code': 200, 'res': 'successfully returned device', 'settings': data }

@app.get("/add-client")
async def add_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return { 'code': 400, 'res': 'not enough arguments supplied' }

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return { 'code': 400, 'res': 'device could not be found' }

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return { 'code': 405, 'res': 'no permission to update' }

    # Add clientID to the permissions for deviceID
    devicePermissions[deviceID].append(clientID)

    # Return success code
    return { 'code': 200, 'res': 'successfully added client to device' }

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
