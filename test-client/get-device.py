import requests

# Import constants files
from constants import *

# Set url and data for request (for getting device settings)
url = f'http://{SERVER_ADRESS}/api/get-device'
Data = {
  'ClientID': 'CLIENT IDENTIFIER',
  'DeviceID': 'DEVICE IDENTIFIER',
}

# Send request to server
x = requests.post(url, json = Data)

# Get returned data (current device settings)
print(x.text)
