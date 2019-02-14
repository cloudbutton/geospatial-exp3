# -*- coding: UTF-8 -*-

"""

AUTHOR: Juanjo

DATE: 10/01/2018

"""

import unittest

from app.owm.openweathermap_client import OpenWeatherMapClient


class OWMWeatherForecastTestCase(unittest.TestCase):

    def setUp(self):
        owm_client = OpenWeatherMapClient('77d76b5088577c44866d05c63a0a80d1', '3128026')
        self.w_forecast = owm_client.fetch_weather_forecast()

    def test_get_wind_speed(self):
        self.w_forecast.get_wind_speed()

    def test_get_rain(self):
        self.w_forecast.get_rain()

    def test_get_temperature(self):
        self.w_forecast.get_temperature()
