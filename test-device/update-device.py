import requests

# Import constants files
from constants import SERVER_ADDRESS

# Set url and data for request (for device settings update)
url = f'https://{SERVER_ADDRESS}/update-device'
data = {
  'clientID': 'CLIENT IDENTIFIER',
  'deviceID': 'DEVICE IDENTIFIER',
  'data': {
    'op': 'update-settings',
    'settings': {
      'setting1': 'value1',
    }
  }
}

# Send request to server
x = requests.get(url, params = data)

# Get returned data (update request result)
print(x.text)
