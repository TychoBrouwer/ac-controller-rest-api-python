import requests
import json

# Import constants files
from constants import SERVER_ADDRESS

operation = {
  'op': 'update-settings',
  'settings': {
    'setting1': 'value1',
  }
}

# Set url and data for request (for device settings update)
url = f'https://{SERVER_ADDRESS}/update-device'
data = {
  'clientID': 'CLIENT IDENTIFIER',
  'deviceID': 'DEVICE IDENTIFIER',
  'operation': json.dumps(operation)
}

# Send request to server
x = requests.get(url, params = data)

# Get returned data (update request result)
print(x.text)
