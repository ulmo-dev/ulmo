import ulmo

test_values = [
    {
        'state': 'AL',
        'climate_division': 1,
        'period': '2013-01-27/2013-02-02',
        'value': {
            'cmi': 2.71,
            'pdsi': 2.54,
            'period': '2013-01-27/2013-02-02',
            'potential_evap': 0.15,
            'precipitation': 1.57,
            'runoff': 1.42,
            'soil_moisture_lower': 5.0,
            'soil_moisture_upper': 1.0,
            'temperature': 47.4,
        }
    },
]


def test_get_data_by_state():
    data = ulmo.cpc.drought.get_data(state='AL')
    assert len(data) == 1
    assert 'AL' in data


def test_get_data():
    data = ulmo.cpc.drought.get_data()

    for test_value in test_values:
        values = data.get(test_value['state'], {}).get(test_value['climate_division'])
        value = [
            value for value in values
            if test_value['period'] == value['period']
        ][0]
        assert value == test_value['value']
