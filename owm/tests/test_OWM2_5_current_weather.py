# -*- coding: UTF-8 -*-

"""

AUTHOR: Juanjo

DATE: 10/01/2018

"""

import unittest

from app.owm.openweathermap_client import OpenWeatherMapClient


class OWMCurrentWeatherTestCase(unittest.TestCase):

    def setUp(self):
        owm_client = OpenWeatherMapClient('77d76b5088577c44866d05c63a0a80d1', '3128026')
        self.current_weather = owm_client.fetch_current_weather()

    def test_get_wind_speed(self):
        self.current_weather.get_wind_speed()

    def test_get_rain(self):
        self.current_weather.get_rain()

    def test_get_temperature(self):
        self.current_weather.get_temperature()
