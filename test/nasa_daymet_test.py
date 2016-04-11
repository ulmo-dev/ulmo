import numpy as np
import pandas

from ulmo import util
from ulmo.nasa import daymet

import test_util

def test_get_variables():
    variables = daymet.get_variables()
    assert type(variables) == dict
    for var in ['srad', 'tmin', 'tmax', 'swe', 'vp', 'dayl', 'prcp']:
        assert var in variables.keys()


test_pixels = [
    {'latitude':35.0,
     'longitude':-110.0,
     'variables':['tmax', 'tmin', 'prcp'],
     'years':[1980]},
    {'latitude':28.5,
     'longitude':-81.5,
     'variables':['srad', 'tmin', 'tmax', 'swe', 'vp', 'dayl', 'prcp'],
     'years':[2014, 2015]},]

def test_get_data_as_dataframes():
    for test_pixel_kwargs in test_pixels:
        pixel_data = daymet.get_daymet_singlepixel(**test_pixel_kwargs)
        assert pixel_data.shape == (len(test_pixel_kwargs['years'])*365, len(test_pixel_kwargs['variables'])+2)
        assert pixel_data.iloc[0].year == test_pixel_kwargs['years'][0]
        assert pixel_data.iloc[-1].year == test_pixel_kwargs['years'][-1]
        for var in test_pixel_kwargs['variables']:
            assert var in pixel_data.keys()


def test_get_data_as_dicts():
    for test_pixel_kwargs in test_pixels:
        test_pixel_kwargs['as_dataframe'] = False
        pixel_data = daymet.get_daymet_singlepixel(**test_pixel_kwargs)
        assert len(pixel_data.keys()) ==  len(test_pixel_kwargs['variables'])
        assert "{}-01-01".format(test_pixel_kwargs['years'][0]) in pixel_data[test_pixel_kwargs['variables'][0]].keys()
        assert "{}-12-30".format(test_pixel_kwargs['years'][-1]) in pixel_data[test_pixel_kwargs['variables'][0]].keys()
        for var in test_pixel_kwargs['variables']:
            assert var in pixel_data.keys()


