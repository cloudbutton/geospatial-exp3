"""
Este script calcula el índice NDVI

AUTHOR: Juanjo

DATE: 06/02/2019

"""

import os

import numpy as np
import rasterio
from rasterio import plot

bands_path = 'sentinel_images/S2A_MSIL1C_20190106T105431_N0207_R051_T30SXH_20190106T112304/A018495/'
bands = os.listdir(bands_path)
for band in bands:
    if band.endswith('B04.jp2'):
        band4 = rasterio.open(bands_path + band)
    elif band.endswith('B08.jp2'):
        band8 = rasterio.open(bands_path + band)

# Number of raster bands
print("Raster bands {}".format(band4.count))
print("Raster columns {}".format(band4.width))
print("Raster rows {}".format(band4.height))
print("Type of raster byte {}".format(band4.dtypes[0]))
print("Raster system of reference {}".format(band4.crs))

# Generate nir and red objects
nir = band8.read(1).astype('uint16')
red = band4.read(1).astype('uint16')

# Ndvi calculation, empty cells or nodata cells are reported as 0
ndvi = np.where(
    (nir + red) == 0.,
    0,
    (nir - red) / (nir + red)
).astype('uint16')

if not os.path.exists('results'):
    os.makedirs('results')
if os.path.exists('results/ndvi.jp2'):
    os.remove('results/ndvi.jp2')

# Export ndvi image
ndvi_image = rasterio.open(
    'results/ndvi.jp2', 'w+',
    driver='JP2OpenJPEG',
    width=band4.width, height=band4.height,
    count=1,
    crs=band4.crs,
    transform=band4.transform,
    dtype='uint16')
ndvi_image.write(ndvi, 1)
ndvi_image.close()

# Plot ndvi
ndvi = rasterio.open('results/ndvi.jp2')
plot.show(ndvi, cmap='Greens')
