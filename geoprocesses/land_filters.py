"""

AUTHOR: Juanjo

DATE: 02/04/2019

"""

import ogr
import os
import subprocess


def create_filtered_shapefile(in_shapefile, filter_fields, dst_dir, out_shapefile_name):
    # Check if the dst file exists
    out_shapefile = os.path.join(dst_dir, out_shapefile_name)
    if os.path.exists(out_shapefile):
        return out_shapefile

    # Create query string
    filters = []
    for k, v in filter_fields.items():
        if isinstance(v, list):
            for item in v:
                filters.append("{} = '{}'".format(k, item))
        else:
            filters.append("{} = '{}'".format(k, v))
    query_str = ' or '.join(filters)

    val = subprocess.check_call(f'ogr2ogr -where "{query_str}" {out_shapefile} {in_shapefile}', shell=True)
    if val == 0:
        return out_shapefile
    else:
        return None


class CultivableLandFilterProcess:

    @staticmethod
    def run(in_shapefile, dst_dir, out_shapefile_name):
        filter_fields = {
            'uso_sigpac': ['CI', 'CF', 'CO', 'CS', 'CV', 'FF', 'FL', 'FS', 'FV', 'FY', 'IS', 'IV', 'OC', 'OF', 'OV', 'PS', 'TA', 'TH', 'VF', 'VI', 'VO', 'ZC']
        }
        return create_filtered_shapefile(in_shapefile, filter_fields, dst_dir, out_shapefile_name)


class UncultivableLandFilterProcess:

    @staticmethod
    def run(in_shapefile, dst_dir, out_shapefile_name):
        filter_fields = {
            'uso_sigpac': ['AG', 'CA', 'ED', 'FO', 'IM', 'PA', 'PR', 'ZU', 'ZV']
        }
        return create_filtered_shapefile(in_shapefile, filter_fields, dst_dir, out_shapefile_name)