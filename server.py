import socket
from _thread import *
from flask import Flask, request

# Import constants files
from constants import *

# Initialize flask server
app = Flask(__name__)

@app.route("/")
def server_running():
    return 'Server running!', 200

@app.route("/api/update-device", methods=['POST', 'GET'])
def update_client():
    # Get the request data
    RequestData = request.get_json()
    DeviceID = RequestData['DeviceID']
    ClientID = RequestData['ClientID']
    Data = RequestData['Data']

    # Check if device is connected
    if DeviceID not in Devices:
        return 'device could not be found', 404

    # Check if client has permission
    if ClientID not in DevicePermissions[DeviceID]:
        return 'no permission to update', 403
    
    # Send update data to device
    Devices[DeviceID].sendall(str.encode(Data))

    # Return success code
    return '', 204

@app.route("/api/get-device", methods=['POST', 'GET'])
def get_client():
    # Get the request data
    RequestData = request.get_json()
    DeviceID = RequestData['DeviceID']
    ClientID = RequestData['ClientID']

    # Check if device is connected
    if DeviceID not in Devices:
        return 'device could not be found', 404

    # Check if client has permission
    if ClientID not in DevicePermissions[DeviceID]:
        return 'no permission to update', 403
    
    # Send data request to the device 
    Devices[DeviceID].sendall(str.encode('get-settings'))

    # Receive data from device
    data = Devices[DeviceID].recv(2048)
    # Return data to client
    return data

def initiate_device(connection):
    # Send server conformation to device
    connection.send(str.encode('Server is working!'))

    # Receive device indentifier from device
    data = connection.recv(2048)
    if data:
        # Store device identifier in currently connected dict
        Devices[data.decode('utf-8')] = connection

def socket_connection_loop():
    # Loop for eccepting new device connections
    while True:
        # Accept new device connection
        connection, address = ServerSideSocket.accept()
        print(f'Connected to {address[0]}:{address[1]}')

        # Initiate device connection
        initiate_device(connection)

    ServerSideSocket.close()
    
# Permissions of the client identifiers and their devices
DevicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Currenly connected devices
Devices = {}

# Initialize socket
ServerSideSocket = socket.socket()

if __name__ == "__main__":
    try:
        ServerSideSocket.bind((SERVER_IP, SERVER_SOCKET_PORT))
    except socket.error as e:
        print(str(e))

    print('Socket is listening...')
    ServerSideSocket.listen(5)

    # Start listening to new device connections 
    start_new_thread(socket_connection_loop, ())

    # Start Flask app
    app.run(host=SERVER_IP, port=SERVER_FLASK_PORT)
