"""

AUTHOR: Juanjo

DATE: 15/03/2019

"""

import os

DATA_DIR = os.path.abspath('data')
SENTINEL_DATA_DIR = os.path.abspath(os.path.join(DATA_DIR, 'sentinel'))
SENTINEL_DOWNLOADS_DIR = os.path.abspath(os.path.join(SENTINEL_DATA_DIR, 'downloads'))
SENTINEL_BANDS_DIR = os.path.abspath(os.path.join(SENTINEL_DATA_DIR, 'bands'))
STUDY_AREAS_DIR = os.path.abspath(os.path.join(SENTINEL_DATA_DIR, 'study_areas'))
PARCELS_DIR = os.path.abspath(os.path.join(DATA_DIR, 'parcels'))
NDVI_DIR = os.path.abspath(os.path.join(DATA_DIR, 'ndvi'))
LIDAR_DATA_DIR = os.path.abspath(os.path.join(DATA_DIR, 'lidar'))
SIAM_DATA_DIR = os.path.abspath(os.path.join(DATA_DIR, 'siam'))
LAND_DATA_DIR = os.path.abspath(os.path.join(DATA_DIR, 'land'))
