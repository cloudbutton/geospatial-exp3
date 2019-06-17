"""


AUTHOR: Juanjo

DATE: 17/04/2019

"""
import os

import numpy as np
import rasterio
from osgeo import gdal


class VectorizeNDVIByParcel:

    @staticmethod
    def run(parcel_raster, ndvi_stats):
        src_ds = gdal.Open(parcel_raster)
        srcband = src_ds.GetRasterBand(1)
        dst_layername = "PolyFtr"
        drv = ogr.GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(dst_layername + ".shp")
        dst_layer = dst_ds.CreateLayer(dst_layername, srs=None)
        newField = ogr.FieldDefn('Area', ogr.OFTInteger)
        dst_layer.CreateField(newField)
        gdal.Polygonize(srcband, None, dst_layer, 0, [],
                        callback=None)