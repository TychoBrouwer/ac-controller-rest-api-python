import requests

# Import constants files
from constants import *

# Set url and data for request (for device settings update)
url = f'http://{SERVER_IP}:{SERVER_FLASK_PORT}/update-device'
# url = f'http://{SERVER_ADRESS}/update-device'
Data = {
  'ClientID': 'CLIENT IDENTIFIER',
  'DeviceID': 'DEVICE IDENTIFIER',
  'Data': 'second request'
}

# Send request to server
x = requests.post(url, json = Data)

# Get returned data (update request result)
print(x.text)
