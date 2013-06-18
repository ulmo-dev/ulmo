import glob
import os

import pandas

import ulmo

import test_util

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files/twc/kbdi')
MOCKED_URLS = dict([
    ('http://twc.tamu.edu/weather_images/summ/' + os.path.basename(path), path)
    for path in glob.glob(os.path.join(DATA_DIR, '*'))
])

test_sets = [
    {
        'start': '2013-04-09',
        'end': '2013-04-09',
        'fips': '48507',
        'values': [{
            'county': 'ZAVALA',
            'date': '2013-04-09',
            'kbdi_avg': 572,
            'kbdi_max': 708,
            'kbdi_min': 423,
        }]
    },
    {
        'start': '2013-04-09',
        'end': '2013-04-09',
        'fips': '48007',
        'values': [{
            'county':  'ARANSAS',
            'date': '2013-04-09',
            'kbdi_avg': 497,
            'kbdi_max': 561,
            'kbdi_min': 439,
        }]
    },
]


def test_get_data_by_county():
    with test_util.temp_dir() as data_dir:
        for test_set in test_sets:
            with test_util.mocked_urls(MOCKED_URLS):
                data = ulmo.twc.kbdi.get_data(
                    county=test_set['fips'],
                    start=test_set['start'],
                    end=test_set['end'],
                    data_dir=data_dir,
                )
            assert len(data) == 1
            assert test_set['fips'] in data


def test_get_data():
    with test_util.temp_dir() as data_dir:
        for test_set in test_sets:
            with test_util.mocked_urls(MOCKED_URLS):
                data = ulmo.twc.kbdi.get_data(
                    start=test_set['start'],
                    end=test_set['end'],
                    data_dir=data_dir,
                )

            values = data.get(test_set['fips'], {})
            test_values = test_set['values']

            for test_value in test_values:
                assert test_value in values


def test_get_data_as_dataframe():
    with test_util.temp_dir() as data_dir:
        with test_util.mocked_urls(MOCKED_URLS):
            data = ulmo.twc.kbdi.get_data(
                start='2013-04-09',
                end='2013-04-09',
                as_dataframe=True,
                data_dir=data_dir,
            )

            assert isinstance(data, pandas.DataFrame)


def test_data_dir_used():
    with test_util.temp_dir() as data_dir:
        with test_util.mocked_urls(MOCKED_URLS):
            ulmo.twc.kbdi.get_data(
                start='2013-04-09',
                end='2013-04-11',
                as_dataframe=True,
                data_dir=data_dir,
            )
        files_glob = glob.glob(os.path.join(data_dir, '*'))
        assert len(files_glob) == 3
