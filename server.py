from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import requests

# Import files
from constants import *
from socket_manager import SocketManager
from weather_manager import WeatherManager

# Initialize fastapi app
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {'code': 200, 'res': 'server is running and reachable!'}


@app.get("/update-device")
async def update_client(deviceID: str, clientID: str, operation: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID or operation):
        return {'code': 400, 'res': 'not enough arguments supplied'}

    # Check if device is connected
    if not socketManager.connected(deviceID):
        return {'code': 400, 'res': 'device could not be found'}

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return {'code': 405, 'res': 'no permission to update'}

    try:
        # Send update data to device
        await socketManager.send(deviceID, operation)
    except Exception as e:
        print(e)
        # Return error code
        return {'code': 500, 'res': 'error while sending data to device'}

    # Return success code
    return {'code': 200, 'res': 'successfully updated device'}


@app.get("/get-device")
async def get_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return {'code': 400, 'res': 'not enough arguments supplied'}

    # Check if device is connected
    if not socketManager.connected(deviceID):
        return {'code': 400, 'res': 'device could not be found'}

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return {'code': 405, 'res': 'no permission to update'}

    data = {
        'op': 'get-settings'
    }

    try:
        # Send data request to the device
        await socketManager.send(deviceID, json.dumps(data))

        # Receive data from device
        data = await socketManager.receive(deviceID)
    except Exception as e:
        print(e)
        # Return error code
        return {'code': 500, 'res': 'error while sending data to device'}

    # Return data to client
    return {'code': 200, 'res': 'successfully returned device settings', 'settings': json.loads(data)}


@app.get("/add-client")
async def add_client(deviceID: str, clientID: str):
    # Check if all arguments are supplied
    if not (deviceID or clientID):
        return {'code': 400, 'res': 'not enough arguments supplied'}

    # Check if device is connected
    if not socketManager.connected(deviceID):
        return {'code': 400, 'res': 'device could not be found'}

    # Check if client has permission
    if clientID not in devicePermissions[deviceID]:
        return {'code': 405, 'res': 'no permission to update'}

    # Add clientID to the permissions for deviceID
    devicePermissions[deviceID].append(clientID)

    # Return success code
    return {'code': 200, 'res': 'successfully added client to device'}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept connection
    await websocket.accept()
    # Start handler for the socket
    await socketManager.handler(websocket)


@app.get("/get-weather-data")
async def get_weather_data():
    result = weatherManager.getWeather()

    forecast_list = []

    # add location, sunrise and sunset data
    timezone = result['city']['timezone']
    forecast_list.append([result['city']['name'], result['city']
                         ['sunrise'] + timezone, result['city']['sunset'] + timezone])

    for i in result['list']:
        forecast = []
        forecast.append(i['dt_txt'])
        forecast.append(i['main']['temp'])
        forecast.append(i['clouds']['all'])
        forecast_list.append(forecast)

    return {'code': 200, 'res': 'successfully returned weather data', 'forecast': forecast_list}

# Permissions of the client identifiers and their devices
devicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

# Start socket connection
socketManager = SocketManager()
weatherManager = WeatherManager()

# # Run uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
