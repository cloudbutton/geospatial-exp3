# MAPPING WATER USE FOOTPRINT

This project corresponds to the experiment called **Mapping water use** footprint of the **geospatial** use case.

The first step in executing the project is to install all the dependencies found in the *requirements.txt* file. For this you can use the *pip* utility:

    pip install -r requirements.txt


In addition, the use of the following external tools is required:
- Sen2Cor (Available at http://step.esa.int/main/third-party-plugins-2/sen2cor/)
- GDAL (Available at https://gdal.org/)
    - ogr2ogr
    - gdal_translate

## PROJECT STRUCTURE

Within the project are the following packages:
- **aemet**: Contains a module to obtain data from the AEMET
- **data_fetcher**: Contains useful modules for downloading data sources
- **geoprocesses**: Contains the different geoprocesses used in the workflow for the calculation of water consumption
- **owm**: Contains a client for obtaining weather data from *Open Weather Map*
- **sample_data**: It is a directory with test data sources


## NDVI CALCULATION

The following geoprocesses are involved in the calculation of the NDVI:
- SelectStudyAreaProcess (*geoprocesses/select_study_area.py*)
- CropBandsProcess (*geoprocesses/crop_bands.py*)
- NDVIProcess (*geoprocesses/ndvi.py*)

In the file *cloudbutton.py* you can see the workflow of these geoprocesses, along with their inputs and outputs. Specifically, it is the code included in option 5 (line 171).