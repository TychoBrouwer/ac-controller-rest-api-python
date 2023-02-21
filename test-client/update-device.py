import requests

# Import constants files
from constants import *

# Set url and data for request (for device settings update)
url = f'https://{SERVER_API_ADDRESS}/update-device'
Data = {
  'ClientID': 'CLIENT IDENTIFIER',
  'DeviceID': 'DEVICE IDENTIFIER',
  'Data': 'second request'
}

# Send request to server
x = requests.get(url, params = Data)

# Get returned data (update request result)
print(x.text)
