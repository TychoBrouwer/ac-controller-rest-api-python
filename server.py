# from flask import Flask, request
from fastapi import FastAPI, WebSocket

# Import files
from constants import *
from socket_connection import SocketConnection

# Initialize flask server
# app = Flask(__name__)
app = FastAPI()

# @app.route("/update-device", methods=['GET'])
@app.get("/update-device")
async def update_client(deviceID: str, clientID: str, data: str):
    # # Get the request data
    # deviceID = request.args.get('deviceID')
    # clientID = request.args.get('clientID')
    # data = request.args.get('data')

    # Check if all arguments are supplied
    if not (deviceID or clientID or data):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return 'device could not be found', 400

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return 'no permission to update', 405
    
    # Send update data to device
    await socketConnection.send(deviceID, data)

    # Return success code
    return '', 204

@app.get("/get-device")
# @app.route("/get-device", methods=['GET'])
async def get_client(deviceID: str, clientID: str):
    # # Get the request data
    # deviceID = request.args.get('deviceID')
    # clientID = request.args.get('clientID')

    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return 'not enough arguments supplied', 400

    # Check if device is connected
    if not socketConnection.connected(deviceID):
        return 'device could not be found', 400

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return 'no permission to update', 405

    # Send data request to the device 
    await socketConnection.send(deviceID, str.encode('get-settings'))

    # Receive data from device
    data = await socketConnection.receive(deviceID)

    # Return data to client
    return data

# @app.route("/add-client", methods=['GET'])
@app.get("/add-client")
async def add_client(deviceID: str, clientID: str):
    # # Get the request data
    # deviceID = request.args.get('deviceID')
    # clientID = request.args.get('clientID')

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
    await socketConnection.socket_handler(websocket)

# Permissions of the client identifiers and their devices
devicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Start socket connection
socketConnection = SocketConnection();

# if __name__ == "__main__":
#     # Start Flask app
#     app.run(host=SERVER_IP, port=SERVER_FLASK_PORT)
