"""

AUTHOR: Juanjo

DATE: 05/02/2019

"""

import errno
import os
import os.path
import shutil
import zipfile

SENTINEL_IMAGE_DIR = 'sentinel_images'
ZIP_EXTENSION = ".zip"
GRANULE_DIR = 'GRANULE'
IMAGE_DATA_DIR = 'IMG_DATA'
SAFE_EXTENSION = '.SAFE'
JP2_EXTENSION = '.jp2'


class SentinelProduct:
    def __init__(self, satellite, product_name, n, r, tile, start_date, end_date, a=None):
        self.satellite = satellite
        self.product_name = product_name
        self.n = n
        self.r = r
        self.tile = tile
        self.start_date = start_date
        self.end_date = end_date
        self.a = a


def sentinel_product(full_product_name):
    file_info = full_product_name.split('_')
    satellite = file_info[0]
    product_name = file_info[1]
    start_date = file_info[2]
    n = file_info[3][1:]
    r = file_info[4][1:]
    tile = file_info[5][1:]
    end_date = file_info[6]
    return SentinelProduct(satellite, product_name, n, r, tile, start_date, end_date)


def extract_bands(sentinel_image_dir, sentinel_zip_filename, bands):
    sentinel_zip_file = os.path.abspath(os.path.join(sentinel_image_dir, sentinel_zip_filename))
    zip_ref = zipfile.ZipFile(sentinel_zip_file)  # create zipfile object
    zip_ref.extractall(SENTINEL_IMAGE_DIR)  # extract file to dir SENTINEL_IMAGE_DIR
    zip_ref.close()

    full_product_name = sentinel_zip_filename.split('.')[0]
    sentinelp = sentinel_product(full_product_name)
    try:
        os.makedirs(os.path.join(sentinel_image_dir, full_product_name))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    product_safe_dir = full_product_name + SAFE_EXTENSION
    granule_dir = os.path.join(sentinel_image_dir, os.path.join(product_safe_dir, GRANULE_DIR))
    granule_dirs = [d for d in os.listdir(granule_dir) if
                    (os.path.isdir(os.path.join(granule_dir, d))) and (d != '.') and (d != '..')]

    for granule_content_dir in granule_dirs:
        a = granule_content_dir.split('_')[2]
        sentinelp.a = a
        img_data_path = os.path.join(granule_dir, os.path.join(granule_content_dir, IMAGE_DATA_DIR))
        band_files = [bf for bf in os.listdir(img_data_path)]
        selected_bands = []
        for band_file in band_files:
            for band in bands:
                if band_file.endswith(band + JP2_EXTENSION):
                    selected_bands.append(band_file)

        full_product_dir = os.path.abspath(os.path.join(sentinel_image_dir, full_product_name))
        a_dir = os.path.abspath(os.path.join(full_product_dir, a))
        os.makedirs(a_dir)
        for c in selected_bands:
            band_file = os.path.abspath(os.path.join(img_data_path, c))
            shutil.copy(band_file, a_dir)
    # shutil.rmtree(os.path.join(sentinel_image_dir, sentinel_zip_filename))  # delete zipped file
    shutil.rmtree(os.path.join(sentinel_image_dir, product_safe_dir))


def get_sentinel_data(sentinel_image_dir, bands):
    sentinel_files = [f for f in os.listdir(sentinel_image_dir) if
                      (os.path.isfile(os.path.join(sentinel_image_dir, f))) and (f.endswith(ZIP_EXTENSION))]
    for sentinel_zip_file in sentinel_files:
        extract_bands(sentinel_image_dir, sentinel_zip_file, bands)
        break  # TODO: Quitar


if __name__ == '__main__':
    get_sentinel_data(SENTINEL_IMAGE_DIR, ('B04', 'B08'))
