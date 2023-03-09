import requests

from constants import *
from private import OPENWEATHERMAP_API_KEY


class WeatherManager:
    def getWeather(self):
        # Get weather data from openweathermap
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&cnt={OBSERVATION_COUNT}&appid={OPENWEATHERMAP_API_KEY}&units=metric')
        # Check if request was successful
        if response.status_code != 200:
            print('Error while getting weather data')
            return None
        # Return weather data
        return response.json()
