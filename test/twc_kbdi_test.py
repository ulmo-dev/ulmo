import pandas

import ulmo

import test_util


test_sets = [
    {
    'filename' : 'twc/kbdi/summ20130409.txt',
    'start' : '2013-04-09',
    'end' : '2013-04-10',
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
    'filename' : 'twc/kbdi/summ20130409.txt',
    'start' : '2013-04-09',
    'end' : '2013-04-10',
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
    for test_set in test_sets:
        with test_util.mocked_requests(test_set['filename']):
            data = ulmo.twc.kbdi.get_data(county=test_set['fips'], start=test_set['start'],
                end=test_set['end'])
        assert len(data) == 1
        assert test_set['fips'] in data


def test_get_data():

    for test_set in test_sets:
        with test_util.mocked_requests(test_set['filename']):
            data = ulmo.twc.kbdi.get_data(start=test_set['start'], end=test_set['end'])

        values = data.get(test_set['fips'], {})

        test_values = test_set['values']

        for test_value in test_values:
            assert test_value in values


def test_get_data_as_dataframe():
    with test_util.mocked_requests('twc/kbdi/summ20130409.txt'):
        data = ulmo.twc.kbdi.get_data(start='2013-04-09', end='2013-04-10',
                as_dataframe=True)

        assert isinstance(data, pandas.DataFrame)
