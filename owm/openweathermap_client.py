"""
Module containing the OWM API main entry point

AUTHOR: Juanjo

DATE: 03/01/2018

"""

import logging

import requests

from .exceptions.api_call_error import APICallError
from . import OWMObservation

logger = logging.getLogger(__name__)


class OpenWeatherMapClient:
    """
    A class representing the OWM web API entry point for version 2.5. Every query to the
    API is done programmatically via a concrete instance of this class.

    The class provides methods for differents API endpoints.

    OWM API Recommendation: Do not send requests more than 1 time per 10 minutes from one device/one API key.
    Normally the weather is not changing so frequently.

    :param str app_id: API key to get access to weather OWM API
    :param str city_id: City Id for which gets weather predictions
    :returns: an *OpenWeatherMapClient* instance

    """

    def __init__(self, app_id, city_id):
        self.app_id = app_id
        self.city_id = city_id

    def fetch_weather_forecast(self):
        """
        Returns weather information for '5 day / 3 hours forecast' endpoint.

        :returns: a *WeatherForecast* instance
        :raises: *APICallError* if there are any problems during the OWM API request.

        """

        logger.info('Fetching OWM weather forecast')
        url = 'https://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}&units=metric'.format(self.city_id,
                                                                                                    self.app_id)
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as re:
            logger.exception('Error ocurred in OWM API request')
            raise APICallError('Error ocurred during fetching weather forecast', re)
        data = response.json()
        logger.info('OWM Weather forecast fetched')
        return OWMObservation.WeatherForecast(data)

    def fetch_current_weather(self):
        """
        Returns weather information for 'Current weather for one location' endpoint.

        :returns: a *CurrentWeather* instance
        :raises: *APICallError* if there are any problems during the OWM API request.

        """

        logger.info('Fetching OWM current weather')
        url = 'https://api.openweathermap.org/data/2.5/weather?id={}&APPID={}&units=metric'.format(self.city_id,
                                                                                                   self.app_id)
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as re:
            logger.exception('Error ocurred in OWM API request')
            raise APICallError('Error ocurred during fetching current weather', re)
        data = response.json()
        logger.info('OWM Current weather fetched')
        return OWMObservation.CurrentWeather(data)
