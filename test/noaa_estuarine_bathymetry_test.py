import pytest
import os
import shutil
import ulmo

path = './files/noaa/estuary_test/' 

def test_get_data_locations():
        
    temp_path = path + '/zip/'

    if (os.path.exists(temp_path)):
        shutil.rmtree(temp_path)

    bathymetry_feature_collection = ulmo.noaa.estuarine_bathymetry.get_data_locations(path)

    assert len(bathymetry_feature_collection['features']) == 71

def test_get_data():
    
    dem_format_dict = {
        '1 arc-second': '_B30.zip',
        '3 arc-second': '_B90.zip',
    }

    estuary_id = 'M070'
    dem_format = '1 arc-second'

    temp_path = path + '/zip_dem/'

    if (os.path.exists(temp_path)):
        shutil.rmtree(temp_path)

    ulmo.noaa.estuarine_bathymetry.get_data(estuary_id=estuary_id, path=path, dem_format=dem_format)

    zip_path = path + '/zip_dem/' + estuary_id + dem_format_dict.get(dem_format)

    assert (os.path.exists(zip_path))

   
    