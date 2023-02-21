from flask import Flask, request

# Import files
from constants import *
from socket_connection import *

# Initialize flask server
app = Flask(__name__)

@app.route("/update-device", methods=['GET'])
async def update_client():
    # Get the request data
    deviceID = request.args.get('deviceID')
    clientID = request.args.get('clientID')
    data = request.args.get('data')

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
    await socketConnection.send(deviceID, str.encode(data))

    # Return success code
    return '', 204

@app.route("/get-device", methods=['GET'])
async def get_client():
    # Get the request data
    deviceID = request.args.get('deviceID')
    clientID = request.args.get('clientID')

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

@app.route("/add-client", methods=['GET'])
async def add_client():
    # Get the request data
    deviceID = request.args.get('deviceID')
    clientID = request.args.get('clientID')

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

# Permissions of the client identifiers and their devices
devicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Start socket connection
socketConnection = SocketConnection(SERVER_SOCKET_PORT);

if __name__ == "__main__":
    # Start Flask app
    app.run(host=SERVER_IP, port=SERVER_FLASK_PORT)
