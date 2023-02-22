import requests
import json

# Import constants files
from constants import SERVER_ADDRESS

# Set url and data for request (for getting device settings)
url = f'https://{SERVER_ADDRESS}/get-device'
data = {
  'clientID': 'CLIENT IDENTIFIER',
  'deviceID': 'DEVICE IDENTIFIER',
}

# Send request to server
x = requests.get(url, params = data)

# Get returned data (current device settings)
print(x.text)
