"""
En esta web https://www.asturnatura.com/sinflac/utm-mgrs.php
se pueden consultar las coordenadas del sistema MGRS (tiles)
"""

import sentinelsat
import collections

# https://sentinelsat.readthedocs.io/en/stable/api.html

api = sentinelsat.SentinelAPI(user="vmoreno",
                              password="12345678",
                              api_url='https://scihub.copernicus.eu/dhus',
                              show_progressbars=True)

# Reading all the tiles
# tiles = []
# tiletxt = open("SpainPen_tiles.txt", mode = "r")
# tilelines = tiletxt.read().splitlines()
# tiletxt.close()
# for t in tilelines:
#    tiles.append(t)

tiles = ["30SXH"]

dateStart = "20190101"
dateEnd = "20190116"

query_kwargs = {
    'platformname': 'Sentinel-2',
    'producttype': ('S2MS2Ap', 'S2MSI1C'),
    'cloudcoverpercentage': (0, 15),
    'date': (dateStart, dateEnd)
}

products = collections.OrderedDict()
for tile in tiles:
    kw = query_kwargs.copy()
    kw['tileid'] = tile
    pp = api.query(**kw)
    products.update(pp)

# Define folder where download into
output_folder = "sentinel_images"
api.download_all(products, output_folder)
