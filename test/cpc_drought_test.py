import pandas

import ulmo

import test_util


test_sets = [
    {
        'state': 'AL',
        'climate_division': 1,
        'values': [{
            'cmi': 0.05,
            'pdsi': 0.53,
            'period': '2010-06-06/2010-06-12',
            'potential_evap': 1.37,
            'precipitation': 0.71,
            'runoff': 0.0,
            'soil_moisture_lower': 4.86,
            'soil_moisture_upper': 0.0,
            'temperature': 77.6
        }]
    },
]


def test_get_data_by_state():
    with test_util.mocked_requests('cpc/drought/palmer10'):
        data = ulmo.cpc.drought.get_data(state='AL', start='2010-5-20',
                end='2010-6-13')
    assert len(data) == 1
    assert 'AL' in data


def test_get_data():
    with test_util.mocked_requests('cpc/drought/palmer10'):
        data = ulmo.cpc.drought.get_data(start='2010-5-20', end='2010-6-13')

    for test_set in test_sets:
        values = data.get(test_set['state'], {}).get(test_set['climate_division'])
        test_values = test_set['values']

        for test_value in test_values:
            assert test_value in values


def test_get_data_as_dataframe():
    with test_util.mocked_requests('cpc/drought/palmer10'):
        data = ulmo.cpc.drought.get_data(start='2010-5-20', end='2010-6-13',
                as_dataframe=True)

        assert isinstance(data, pandas.DataFrame)
