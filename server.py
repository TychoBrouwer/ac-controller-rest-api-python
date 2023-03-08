from fastapi import FastAPI, WebSocket
import uvicorn
import json
import asyncio
import httpx

# Import files
from constants import *
from socket_manager import SocketManager

# Initialize fastapi app
app = FastAPI()


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
    return {'code': 200, 'res': 'successfully returned device settings', 'settings': data}


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

# Permissions of the client identifiers and their devices
devicePermissions = {
    'DEVICE IDENTIFIER': ['CLIENT IDENTIFIER']
}

@app.get("/get-weather-data")
async def get_weather_data():
    client = httpx.AsyncClient()
    task = api_request(client)
    result = await task
    result = json.loads(result)

    '''Forecasts are formatted as follows:
    [
    ['CITY_NAME (String)', 
    SUNRISE_TIME (Unix, current timezone), 
    SUNSET_TIME (Unix, current timezone)
    ]

    ['TIMESTAMP (String) (YYYY-MM-DD HH:MM:SS)', 
    TEMPERATURE (Celcius), 
    CLOUD_COVERAGE (%), 
    ],
    'next observation'
    ]
    '''
    forecast_list = []

    #add location, sunrise and sunset data
    timezone = result['city']['timezone']
    forecast_list.append([result['city']['name'], result['city']['sunrise'] + timezone, result['city']['sunset'] + timezone])

    for i in result['list']:
        forecast = []
        forecast.append(i['dt_txt'])
        forecast.append(i['main']['temp']-272.15) #convert to celsius
        forecast.append(i['clouds']['all'])
        forecast_list.append(forecast)
    print(forecast_list)
    return {"message": "Weather data received successfully"}

async def api_request(client):
    response = await client.get("http://api.openweathermap.org/data/2.5/forecast?q=" + LOCATION + "&cnt="+ OBSERVATION_COUNT + "&APPID=" + OPENWEATHERMAP_API_KEY)
    return response.text

# Start socket connection
socketManager = SocketManager()

# # Run uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
