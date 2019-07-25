"""

AUTHOR: Juanjo

DATE: 14/03/2019

"""

import errno
import os

import time

import rasterio
from rasterio import plot

from constants import DATA_DIR, SENTINEL_DATA_DIR, SENTINEL_DOWNLOADS_DIR, SENTINEL_BANDS_DIR, LIDAR_DATA_DIR, \
    SIAM_DATA_DIR, STUDY_AREAS_DIR, NDVI_DIR, PARCELS_DIR, LAND_DATA_DIR
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
from geoprocesses.det_temperature import DetTemperatureProcess
from geoprocesses.land_filters import CultivableLandFilterProcess, UncultivableLandFilterProcess, \
    IrrigatedLandFilterProcess, WoodLandFilterProcess, CultivatedLandFilterProcess, NakedLandFilterProcess

# ************************************************
#
# Datos de entrada
#
# ************************************************

# SENTINEL

TILES = ['30SXG']
ndvi_stats = None
siam_stations = {
    'AL31': {'Lon': '1 30 47,29', 'Lat': '37 43 56,99', 'alt': 236},
    'AL41': {'Lon': '1 25 0,39', 'Lat': '37 47 32,05', 'alt': 169},
    'AL51': {'Lat': '37 53 57,91', 'Lon': '1 20 18,01', 'alt': 164},
    'AL52': {'Lat': '37 53 25,64', 'Lon': '1 18 34,41', 'alt': 125},
    'AL62': {'Lat': '37 33 44', 'Lon': '1 24 3,5', 'alt': 94},
    'AL91': {'Lat': '37 36 52', 'Lon': '1 22 44', 'alt': 112},
    'CA12': {'Lat': '37 41 19,92', 'Lon': '0 57 3,09', 'alt': 30},
    'CA21': {'Lat': '37 49 53,04', 'Lon': '1 7 22,49', 'alt': 227},
    'CA42': {'Lat': '37 44 53,89', 'Lon': '1 7 45,14', 'alt': 138},
    'CA52': {'Lat': '37 40 37,25', 'Lon': '1 4 14,18', 'alt': 84},
    'CA73': {'Lat': '37 36 40,14', 'Lon': '0 48 13,65', 'alt': 92},
    'CA91': {'Lat': '37 41 56,52', 'Lon': '1 14 16,96', 'alt': 175},
    'CI22': {'Lat': '38 14 7,43', 'Lon': '1 18 35,57', 'alt': 282},
    'CI32': {'Lat': '38 11 28,96', 'Lon': '1 15 28,53', 'alt': 236},
    'CI42': {'Lat': '38º 17 2', 'Lon': '1 29 46,84', 'alt': 244},
    'CI52': {'Lat': '38 15 12,59', 'Lon': '1 41 41,89', 'alt': 275},
    'CI71': {'Lat': '38 16 10,2', 'Lon': '1 35 6', 'alt': 282},
    'CR12': {'Lat': '38 2 38,24', 'Lon': '1 58 48,67', 'alt': 869},
    'CR32': {'Lat': '38 6 39,35', 'Lon': '1 40 59,06', 'alt': 433},
    'CR42': {'Lat': '38 11 54,35', 'Lon': '1 48 37,5', 'alt': 456},
    'CR52': {'Lat': '38 6 16,26', 'Lon': '1 46 48,18', 'alt': 507},
    'CR61': {'Lat': '38 6 52,3', 'Lon': '2 5 46,41', 'alt': 1232},
    'JU12': {'Lat': '38 2 38,24', 'Lon': '1 58 48,67', 'alt': 395},
    'JU42': {'Lat': '38 39 31,9', 'Lon': '1 11 8,73', 'alt': 658},
    'JU52': {'Lat': '38 33 45,57', 'Lon': '1 6 44,57', 'alt': 567},
    'JU71': {'Lat': '38 23 40,01', 'Lon': '1 14 21,58', 'alt': 401},
    'JU81': {'Lat': '38 19 11,3', 'Lon': '1 19 27,58', 'alt': 341},
    'LO11': {'Lat': '37 36 6,23', 'Lon': '1 18 59,92', 'alt': 324},
    'LO21': {'Lat': '37 30 13,86', 'Lon': '1 41 38,07', 'alt': 356},
    'LO31': {'Lat': '37 25 6,96', 'Lon': '1 35 31,94', 'alt': 31},
    'LO41': {'Lat': '37 51 18,72', 'Lon': '1 49 6,62', 'alt': 693},
    'LO51': {'Lat': '37 29 16,45', 'Lon': '1 37 26,29', 'alt': 329},
    'LO61': {'Lat': '37 35 25,7', 'Lon': '1 43 32', 'alt': 319},
    'ML12': {'Lat': '38 3 57,14', 'Lon': '1 25 46,2', 'alt': 264},
    'ML21': {'Lat': '38 2 27,76', 'Lon': '1 28 ,49', 'alt': 276},
    'MO12': {'Lat': '38 0 25,31', 'Lon': '1 18 9,23', 'alt': 161},
    'MO22': {'Lat': '38 7 39,04', 'Lon': '1 13 14,36', 'alt': 146},
    'MO31': {'Lat': '38 4 16,1', 'Lon': '1 14 1,25', 'alt': 80},
    'MO41': {'Lat': '38 10 12,02', 'Lon': '1 3 55,75', 'alt': 162},
    'MO51': {'Lat': '38 9 39,79', 'Lon': '1 9 9,43', 'alt': 197},
    'MO62': {'Lat': '38 6 47,94', 'Lon': '1 20 21,94', 'alt': 206},
    'MU21': {'Lat': '38 2 4,33', 'Lon': '0 59 58,72', 'alt': 27},
    'MU31': {'Lat': '37 53 53,59', 'Lon': '1 16 5,75', 'alt': 140},
    'MU52': {'Lat': '37 58 39,15', 'Lon': '0 59 ,69', 'alt': 125},
    'MU62': {'Lat': '37 56 24,24', 'Lon': '1 8 4,99', 'alt': 56},
    'TP22': {'Lat': '37 47 30,1', 'Lon': '0 49 10,48', 'alt': 7},
    'TP42': {'Lat': '37 46 25,89', 'Lon': '0 53 54,62', 'alt': 31},
    'TP52': {'Lat': '37 50 53,23', 'Lon': '0 53 ,75', 'alt': 91},
    'TP73': {'Lat': '37 49 26,02', 'Lon': '0 55 53,33', 'alt': 92},
    'TP91': {'Lat': '37 44 51,81', 'Lon': '0 59 12,02', 'alt': 56}
}  # TODO: Pasar al algoritmo que calcula la altitud determinada la info de las estaciones


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
    create_dir(LAND_DATA_DIR)


def show_menu():

    while True:
        print('')
        print('')
        print('---------------------------------------------------------------')
        print('[0]  Salir')
        print('[1]  Descargar imágenes de SENTINEL')
        print('[2]  Aplicar corrección atmosférica')
        print('[3]  Obtener ficheros Lidar')
        print('[4]  Obtener datos de SIAM')
        print('[5]  Calcular NDVI')
        print('[6]  Seleccionar parcelas de la zona de estudio')
        print('[7]  Estadísticas por parcela de la zona de estudio')
        print('[8]  Vectorizar la información de las estadísticas de NDVI por parcela')
        print('[9]  Cálculo de la temperatura determinada (Estaciones de SIAM)')
        print('[10] Determinar las áreas de suelo agrícola')
        print('[11] Determinar las áreas de suelo no agrícola')
        print('[12] Determinar las áreas de suelo de regadío')
        print('[13] Determinar las áreas de suelo arbolado')
        print('[14] Determinar las áreas de suelo cultivado')
        print('[15] Determinar las áreas de suelo desnudo')
        option = input('Introduzca una opción >> ')

        try:
            option = int(option)
        except ValueError:
            continue

        if option == 0:
            exit(0)
        if option == 1:
            start_date = '20190106'
            end_date = '20190107'
            start = time.time()
            sentinel.download_bands(TILES, start_date, end_date, SENTINEL_DOWNLOADS_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la descarga de imágenes de SENTINEL: {end - start}')
        if option == 2:
            start = time.time()
            AtmosphericCorrectionProcess.run(SENTINEL_DOWNLOADS_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la corrección atmosférica: {end - start}')
        if option == 3:
            state = '30'  # Código de Murcia
            start = time.time()
            lidar.download_files(state, LIDAR_DATA_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la descarga de imágenes LIDAR: {end - start}')
        if option == 4:
            start = time.time()
            siam.download_weather_info(SIAM_DATA_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la descarga de información meteorológica de SIAM: {end - start}')
        if option == 5:
            map_sheet_shp = 'sample_data/03_Hojas05_Murcia.shp'
            filter_field = 'HOJA_005'
            filter_value = '0955-7-7'
            start = time.time()
            study_area = SelectStudyAreaProcess.run(map_sheet_shp, filter_field, filter_value, STUDY_AREAS_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la selección del área de estudio: {end - start}')

            b4_b8 = ('sample_data/T30SXG_20190106T105431_B04_10m.jp2',
                     'sample_data/T30SXG_20190106T105431_B08_10m.jp2')

            start = time.time()
            cropped_bands = CropBandsProcess.run(b4_b8, study_area, SENTINEL_BANDS_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución del recorte de imágenes de SENTINEL: {end - start}')
            for b in cropped_bands:
                band = rasterio.open(b)
                plot.show(band)

            # TODO: ¿Cómo se hace la correspondencia entre los ficheros descargados de las bandas, los ficheros de las hojas, los filtros de atributos, ...?
            # Preguntar a Carlos para que todos se correspondan entre sí
            start = time.time()
            ndvi_file = NDVIProcess.run(cropped_bands, NDVI_DIR)
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo del NDVI: {end - start}')
            ndvi = rasterio.open(ndvi_file)
            plot.show(ndvi)
        if option == 6:
            start = time.time()
            parcels_file_name = SelectParcelProcess.run(PARCELS_DIR,
                                                        'data/cart/SigPac_2019_servir.shp',
                                                        'data/sentinel/study_areas/HOJA_005__0955_7_7.shp')
            end = time.time()
            print(f'>>> Tiempo de ejecución de la selección de parcelas: {end - start}')
        if option == 7:
            start = time.time()
            global ndvi_stats
            ndvi_stats = NDVIAverageByParcel.run('data/parcels/HOJA_005__0955_7_7.shp', 'data/ndvi/T30SXG_20190106T105431_10m-HOJA_005__0955_7_7.tiff')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo del NDVI medio por parcela: {end - start}')
            print(ndvi_stats)
        if option == 8:
            start = time.time()
            # VectorizeNDVIByParcel.run('data/parcels/HOJA_005__0955_7_7.shp', ndvi_stats)
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo del NDVI vectorizado por parecla: {end - start}')
        if option == 9:
            start = time.time()
            temperatures = siam.temperature_by_station('data/siam/siam_14_05_19.csv')
            det_temperature = DetTemperatureProcess.run(siam_stations, temperatures)
            print(det_temperature)
            end = time.time()
            print(f'>>> Tiempo de ejecución de la temperatura determinada: {end - start}')
        if option == 10:
            start = time.time()
            CultivableLandFilterProcess.run('data/parcels/HOJA_005__0955_7_7.shp', LAND_DATA_DIR, 'out_agricola.shp')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo del suelo agrícola: {end - start}')
        if option == 11:
            start = time.time()
            UncultivableLandFilterProcess.run('data/parcels/HOJA_005__0955_7_7.shp', LAND_DATA_DIR, 'out_no_agricola.shp')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo del suelo no agrícola: {end - start}')
        if option == 12:
            start = time.time()
            IrrigatedLandFilterProcess.run('data/parcels/HOJA_005__0955_7_7.shp', LAND_DATA_DIR, 'out_regadio.shp')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo de suelo de regadío: {end - start}')
        if option == 13:
            start = time.time()
            WoodLandFilterProcess.run('data/parcels/HOJA_005__0955_7_7.shp', LAND_DATA_DIR, 'out_arbolado.shp')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo de suelo arbolado: {end - start}')
        if option == 14:
            start = time.time()
            ndvi_file_abspath = os.path.join(NDVI_DIR, 'T30SXG_20190106T105431_10m-HOJA_005__0955_7_7.tiff')
            CultivatedLandFilterProcess.run(ndvi_file_abspath, LAND_DATA_DIR, 'out_cultivado.tiff')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo de suelo cultivado: {end - start}')
        if option == 15:
            start = time.time()
            ndvi_file_abspath = os.path.join(NDVI_DIR, 'T30SXG_20190106T105431_10m-HOJA_005__0955_7_7.tiff')
            NakedLandFilterProcess.run(ndvi_file_abspath, LAND_DATA_DIR, 'out_desnudo.tiff')
            print('El proceso finalizó')
            end = time.time()
            print(f'>>> Tiempo de ejecución del cálculo de suelo desnudo: {end - start}')


def main():
    create_data_dirs()
    show_menu()


if __name__ == '__main__':
    main()
