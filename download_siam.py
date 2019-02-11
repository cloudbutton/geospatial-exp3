"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 11/02/2019

"""

import requests

url = 'http://siam.imida.es'

response = requests.get(url)
if response.status_code != 200:
    print(response.text)
    exit(response.status_code)
url = response.url
response = requests.get(url)
if response.status_code != 200:
    print(response.text)
    exit(response.status_code)
print(response.text)