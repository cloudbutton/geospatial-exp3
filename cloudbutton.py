"""

AUTHOR: Juanjo

DATE: 14/03/2019

"""

import errno
import os

import rasterio
from rasterio import plot

from constants import DATA_DIR, SENTINEL_DATA_DIR, SENTINEL_DOWNLOADS_DIR, SENTINEL_BANDS_DIR, LIDAR_DATA_DIR, \
    SIAM_DATA_DIR, STUDY_AREAS_DIR, NDVI_DIR, PARCELS_DIR
from data_fetcher import lidar
from data_fetcher import sentinel
from data_fetcher import siam
from geoprocesses import utils
from geoprocesses.atmospheric_correction import AtmosphericCorrectionProcess
from geoprocesses.crop_bands import CropBandsProcess
from geoprocesses.ndvi import NDVIProcess
from geoprocesses.ndvi_average import NDVIAverageByParcel
from geoprocesses.select_parcel import SelectParcelProcess
from geoprocesses.select_study_area import SelectStudyAreaProcess

# ************************************************
#
# Datos de entrada
#
# ************************************************

# SENTINEL
TILES = ['30SXG']


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_data_dirs():
    create_dir(DATA_DIR)
    create_dir(SENTINEL_DATA_DIR)
    create_dir(SENTINEL_BANDS_DIR)
    create_dir(NDVI_DIR)
    create_dir(LIDAR_DATA_DIR)
    create_dir(SIAM_DATA_DIR)
    create_dir(STUDY_AREAS_DIR)
    create_dir(PARCELS_DIR)


def show_menu():
    while True:
        print('')
        print('')
        print('---------------------------------------------------------------')
        print('[0] Salir')
        print('[1] Descargar imágenes de SENTINEL')
        print('[2] Aplicar corrección atmosférica')
        print('[3] Obtener ficheros Lidar')
        print('[4] Obtener datos de SIAM')
        print('[5] Calcular NDVI')
        print('[6] Seleccionar parcelas de la zona de estudio')
        print('[7] Estadísticas por parcela de la zona de estudio')
        option = input('Introduzca una opción >> ')

        try:
            option = int(option)
        except ValueError:
            continue

        if option == 0:
            exit(0)
        if option == 1:
            start_date = '20190101'
            end_date = '20190116'
            sentinel.download_bands(TILES, start_date, end_date, SENTINEL_DOWNLOADS_DIR)
        if option == 2:
            AtmosphericCorrectionProcess.run(SENTINEL_DOWNLOADS_DIR)
        if option == 3:
            state = '30'  # Código de Murcia
            lidar.download_files(state, LIDAR_DATA_DIR)
        if option == 4:
            siam.download_weather_info(SIAM_DATA_DIR)
        if option == 5:
            map_sheet_shp = 'data/cart/03_Hojas05_Murcia.shp'
            filter_field = 'HOJA_005'
            filter_value = '0955-7-7'
            study_area = SelectStudyAreaProcess.run(map_sheet_shp, filter_field, filter_value, STUDY_AREAS_DIR)

            product_dir = os.path.join(SENTINEL_DOWNLOADS_DIR,
                                       'S2A_MSIL2A_20190106T105431_N0207_R051_T30SXG_20190106T112304.SAFE')
            b4_b8 = utils.select_b4_b8_bands(product_dir)

            cropped_bands = CropBandsProcess.run(b4_b8, study_area, SENTINEL_BANDS_DIR)
            for b in cropped_bands:
                band = rasterio.open(b)
                plot.show(band)

            # TODO: ¿Cómo se hace la correspondencia entre los ficheros descargados de las bandas, los ficheros de las hojas, los filtros de atributos, ...?
            # Preguntar a Carlos para que todos se correspondan entre sí
            ndvi_file = NDVIProcess.run(cropped_bands, NDVI_DIR)
            ndvi = rasterio.open(ndvi_file)
            plot.show(ndvi)
        if option == 6:
            parcels_file_name = SelectParcelProcess.run(PARCELS_DIR,
                                                        'data/cart/SigPac_2019_servir.shp',
                                                        'data/sentinel/study_areas/HOJA_005__0955_7_7.shp')
        if option == 7:
            ndvi_stats = NDVIAverageByParcel.run('data/parcels/HOJA_005__0955_7_7.shp', 'data/ndvi/T30SXG_20190106T105431_10m-HOJA_005__0955_7_7.tiff')
            print(ndvi_stats)


def main():
    create_data_dirs()
    show_menu()


if __name__ == '__main__':
    main()
