import requests

# Import constants files
from constants import *

# Set url and data for request (for device settings update)
# url = f'http://{SERVER_IP}:{SERVER_FLASK_PORT}/update-device'
url = f'https://{SERVER_ADDRESS}/update-device'
print(url)
Data = {
  'ClientID': 'CLIENT IDENTIFIER',
  'DeviceID': 'DEVICE IDENTIFIER',
  'Data': 'second request'
}

# Send request to server
x = requests.get(url, params = Data)

# Get returned data (update request result)
print(x.text)
