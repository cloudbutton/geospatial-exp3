"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 11/02/2019

"""

import requests
import urllib.parse
from bs4 import BeautifulSoup

url = 'http://siam.imida.es'

response = requests.get(url)
if response.status_code != 200:
    print('>>>>>>>>>>> Error: ' + response.text)
    exit(response.status_code)
soup = BeautifulSoup(response.text, 'lxml')
report_link = soup.find('a', text='INFORME AGROMETEOROLÓGICO DE UN DÍA')
report_page_link = urllib.parse.urljoin(url, '/apex/' + report_link['href'])

response = requests.get(report_page_link)
if response.status_code != 200:
    print('>>>>>>>>>>> Error: ' + response.text)
    exit(response.status_code)
soup = BeautifulSoup(response.text, 'lxml')
date_str = soup.find('input', {'id': 'P47_FECHA'})['value']
date_str = date_str.replace('/', '_')
csv_report_link = report_page_link + ':CSV::::'
response = requests.get(csv_report_link)
if response.status_code != 200:
    print('>>>>>>>>>>> Error: ' + response.text)
    exit(response.status_code)
else:
    with open('siam_' + date_str + '.csv', 'wb') as siam_csv_file:
        siam_csv_file.write(response.content)
print('>>> Terminó')
