import requests
import time
from constants import *
from private import VISUALCROSSINGP_API_KEY


class WeatherManager:
    def getWeather(self):
        time_unix = int(time.time())
        # Get weather data from VisualCrossing
        response = requests.get(
            f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}/{time_unix}/{time_unix+OBSERVATION_COUNT*3600}?unitGroup=metric&include=hours&key={VISUALCROSSING_API_KEY}&contentType=json'
        )
        # Check if request was successful
        if response.status_code != 200:
            print('Error while getting weather data, response code: ', response.status_code)
            return None
        # Return weather data
        return (response.json(), time_unix)
