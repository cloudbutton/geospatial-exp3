"""
Weather observation classes and data structures.

AUTHOR: Juanjo

DATE: 04/01/2018

"""

import logging
from abc import ABC, abstractmethod

from .exceptions.parse_response_error import ParseResponseError

logger = logging.getLogger(__name__)


class OWMObservation(ABC):
    """
    An abstract base class for representing the weather which is currently being observed in a
    certain location in the world.

    Really, child classes of *OWMObservation* act as parsers of JSON responses from OWM API requests.
    Each weather param required, should be returned by a method which parses the JSON response.

    :param dict data: a dict containing the weather params observed returned by an OWM API request

    """

    def __init__(self, data):
        if data is None or len(data) == 0:
            raise ValueError("'data' must be specified")
        self.data = data

    @abstractmethod
    def get_wind_speed(self):
        pass

    @abstractmethod
    def get_rain(self):
        pass

    @abstractmethod
    def get_temperature(self):
        pass


class CurrentWeather(OWMObservation):
    """
    Parser for 'Current weather for one location' endpoint responses

    """

    def get_wind_speed(self):
        """
        Returns current wind speed info in meters per second

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

        """

        try:
            value = self.data['wind']['speed']
            return float(value)
        except KeyError:
            logger.exception('Unable to read wind speed info from JSON data')
            raise ParseResponseError('Impossible to read wind speed info from JSON data')
        except ValueError:
            logger.exception('Wind speed info from JSON data is not a float')
            raise ParseResponseError('Wind speed info from JSON data is not a float')

    def get_rain(self):
        """
        Returns current rain info in mm

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

        """

        try:
            if 'rain' in self.data:
                value = self.data['rain'].get('3h', 0.0)
            else:
                value = 0
            return float(value)
        except KeyError:
            logger.exception('Impossible to read rain info from JSON data')
            raise ParseResponseError('Impossible to read rain info from JSON data')
        except ValueError:
            logger.exception('Rain info from JSON data is not a float')
            raise ParseResponseError('Rain info from JSON data is not a float')

    def get_temperature(self):
        """
        Returns current temperature info in degrees Celsius

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

        """

        try:
            value = self.data['main']['temp']
            return float(value)
        except KeyError:
            logger.exception('Impossible to read temperature info from JSON data')
            raise ParseResponseError('Impossible to read temperature info from JSON data')
        except ValueError:
            logger.exception('Rain info from JSON data is not a float')
            raise ParseResponseError('Rain info from JSON data is not a float')


class WeatherForecast(OWMObservation):
    """
    Parser for '5 day / 3 hours forecast' endpoint responses

    """

    def get_wind_speed(self):
        """
        Returns wind speed forecast in meters per second

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

        """

        try:
            value = self.data['list'][0]['wind']['speed']
            return float(value)
        except KeyError:
            logger.warning('Unable to read wind speed info from JSON data')
            raise ParseResponseError('Impossible to read wind speed info from JSON data')
        except ValueError:
            logger.warning('Wind speed info from JSON data is not a float')
            raise ParseResponseError('Wind speed info from JSON data is not a float')

    def get_rain(self):
        """
        Returns rain forecast in mm

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

       """

        try:
            if 'rain' in self.data['list'][0]: 
                value = self.data['list'][0]['rain'].get('3h', 0.0)
            else:
                value = 0
            return float(value)
        except KeyError:
            logger.exception('Impossible to read rain info from JSON data')
            raise ParseResponseError('Impossible to read rain info from JSON data')
        except ValueError:
            logger.exception('Rain info from JSON data is not a float')
            raise ParseResponseError('Rain info from JSON data is not a float')

    def get_temperature(self):
        """
        Returns temperature forecast in degrees Celsius

        :returns: a float
        :raises: *ParseResponseError* if an error occurs when parses the response

        """

        try:
            value = self.data['list'][0]['main']['temp']
            return float(value)
        except KeyError:
            logger.exception('Impossible to read temp info from JSON data')
            raise ParseResponseError('Impossible to read temp info from JSON data')
        except ValueError:
            logger.exception('Temp info from JSON data is not a float')
            raise ParseResponseError('Temp info from JSON data is not a float')

    def get_weather_forecast_3_days(self):
        """
        Fetches the weather forecast and saves it in the database

        """

        logger.info('Getting weather forecast')

        add_value = 24 # Three days
        for i in range(len(self.data['list']) - 1, add_value, -1):
            del(self.data['list'][i])
        return self.data

