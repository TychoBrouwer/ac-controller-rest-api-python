import requests

# Import constants files
from constants import *

# Set url and data for request (for getting device settings)
# url = f'http://{SERVER_IP}:{SERVER_FLASK_PORT}/get-device'
url = f'http://{SERVER_ADDRESS}/get-device'
Data = {
  'ClientID': 'CLIENT IDENTIFIER',
  'DeviceID': 'DEVICE IDENTIFIER',
}

# Send request to server
x = requests.get(url, params = Data)

# Get returned data (current device settings)
print(x.text)
