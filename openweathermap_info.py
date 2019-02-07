"""

AUTHOR: Juanjo

DATE: 07/02/2019

"""

from owm.openweathermap_client import OpenWeatherMapClient


def fetch_weather(api_key, city_id):
    owm_murcia = OpenWeatherMapClient(api_key, city_id)
    current_weather = owm_murcia.fetch_current_weather()
    weather = dict()
    weather['temperature'] = current_weather.get_temperature()
    weather['rain'] = current_weather.get_rain()
    weather['wind_speed'] = current_weather.get_wind_speed()
    return weather


weather = fetch_weather('77d76b5088577c44866d05c63a0a80d1', '6355234')
print("Temperatura actual {}".format(weather['temperature']))
print("Lluvia actual {}".format(weather['rain']))
print("Velocidad del viento actual {}".format(weather['wind_speed']))
