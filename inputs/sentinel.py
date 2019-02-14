"""
Este módulo contiene métodos de utilidad para la descarga de
imágenes del satélite Sentinel-2.

Los distintos tiles del sistema de coordenadas MGRS en que
se divide España se pueden encontrar
en esta web https://www.asturnatura.com/sinflac/utm-mgrs.php

La documentación de la librería sentinelsat se puede consultar
en la siguiente dirección:
https://sentinelsat.readthedocs.io/en/stable/api.html

"""

import collections
import errno
import os
import os.path
import shutil
import zipfile

import sentinelsat

RESULTS_DIR = 'results'
SENTINEL_IMGS_DIR = 'sentinel_images'

ZIP_EXTENSION = ".zip"
GRANULE_DIR = 'GRANULE'
IMAGE_DATA_DIR = 'IMG_DATA'
SAFE_EXTENSION = '.SAFE'
JP2_EXTENSION = '.jp2'


def download_products(sent_user, sent_pass, tiles, start_date, end_date, output_folder, show_progressbars=True):
    """
    Descarga todos los productos del satélite Sentinel-2 para los tipos de producto S2MS2Ap y S2MSI1C

    :param sent_user: Nombre de usuario del API del proyecto copérnico
    :param sent_pass: Password del API del proyecto copérnico
    :param tiles: Tiles para filtrar la descarga
    :param start_date: Fecha inicial en que se tomaron las imágenes
    :param end_date: Fecha final en que se tomaron las imágenes
    :param output_folder: Directorio en el que se almacenarán las imágenes
    :param show_progressbars: Indica si se muestran las barras de progreso durante la descarga
    """
    api = sentinelsat.SentinelAPI(user=sent_user,
                                  password=sent_pass,
                                  api_url='https://scihub.copernicus.eu/dhus',
                                  show_progressbars=show_progressbars)

    query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': ('S2MS2Ap', 'S2MSI1C'),
        'cloudcoverpercentage': (0, 15),
        'date': (start_date, end_date)
    }

    products = collections.OrderedDict()
    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)

    api.download_all(products, output_folder)


class SentinelProduct:
    """
    Clase que representa un producto descargado del satélite Sentinel-2
    """

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
    """
    Método factoría que para crear un objeto de la clase *SentinelProduct*
    a partir de un nombre de producto descargado.
    :param full_product_name: Nombre de producto. Se corresponde con el nombre de un fichero
    :return: Una instancia de SentinelProduct
    """
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
    """
    Recupera los ficheros correspondientes a las bandas *bands* contenidos en
    un fichero zip descargado como producto del satélite Sentinel-2.

    Como resultado de la operación, se elimina el fichero ZIP original.

    :param sentinel_image_dir: Directorio en el que se encuentran los ficheros descargados
    :param sentinel_zip_filename: Nombre del fichero del que extraer las bandas
    :param bands: Nombre de las bandas a extraer
    :return:
    """

    sentinel_zip_file = os.path.abspath(os.path.join(sentinel_image_dir, sentinel_zip_filename))
    zip_ref = zipfile.ZipFile(sentinel_zip_file)
    zip_ref.extractall(SENTINEL_IMGS_DIR)
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
    shutil.rmtree(os.path.join(sentinel_image_dir, sentinel_zip_filename))
    shutil.rmtree(os.path.join(sentinel_image_dir, product_safe_dir))


def filter_bands(sentinel_image_dir, bands):
    sentinel_files = [f for f in os.listdir(sentinel_image_dir) if
                      (os.path.isfile(os.path.join(sentinel_image_dir, f))) and (f.endswith(ZIP_EXTENSION))]
    for sentinel_zip_file in sentinel_files:
        extract_bands(sentinel_image_dir, sentinel_zip_file, bands)


if __name__ == '__main__':
    if not os.path.exists(RESULTS_DIR):
        try:
            os.makedirs(RESULTS_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    sentinel_imgs_dir_path = os.path.join(RESULTS_DIR, SENTINEL_IMGS_DIR)
    if not os.path.exists(sentinel_imgs_dir_path):
        try:
            os.makedirs(sentinel_imgs_dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    tiles = ['30SXH']
    start_date = '20190101'
    end_date = '20190116'
    download_products(sent_user='vmoreno',
                      sent_pass='12345678',
                      tiles=tiles,
                      start_date=start_date,
                      end_date=end_date,
                      output_folder=sentinel_imgs_dir_path
                      )

    filter_bands(SENTINEL_IMGS_DIR, ('B04', 'B08'))
