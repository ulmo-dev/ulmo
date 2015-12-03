import pytest

import ulmo
import test_util


def test_get_stations():
    stations_file = 'usace/swtwc/shefids.html'
    with test_util.mocked_urls(stations_file):
        stations = ulmo.usace.swtwc.get_stations()

    test_stations = [
        {'code': u'DSNT2', 'description': u'Lake Texoma, Denison Dam'},
        {'code': u'MYST2', 'description': u'Pat Mayse Lake'},
    ]

    for test_station in test_stations:
        assert stations[test_station['code']] == test_station
    assert 700 <= len(stations) <= 800


def test_get_station_data():
    test_station_data = [
        ('MYST2', '2013-02-18', {
            'code': 'MYST2',
            'description': 'Pat Mayse Lake',
            'station_type': 'RESERVOIR',
            'timezone': 'Cen',
            'values': {
                '2013-02-18 01:00:00': {
                    'AIR-TEMP': 55.2,
                    'BAT-LOAD': 12.83,
                    'ELEVATION': 447.0,
                    'INFLOW': 9.0,
                    'PRECIP': 0.0,
                    'PRECIP(2)': 0.0,
                    'REL-HUMID': 56.37,
                    'RELEASE': 0.0,
                    'SOLAR-RAD': 0.0,
                    'STORAGE': 96402.0,
                    'VOLTAGE': 12.99,
                    'WIND-DIR': 173.0,
                    'WIND-SPEED': 18.02
                },
            },
        }),
    ]

    for code, date, test_data in test_station_data:
        url_date = date.replace('-', '')
        filename = '%s.%s.html' % (code, url_date)
        data_file = 'usace/swtwc/' + filename
        with test_util.mocked_urls(data_file):
            station_data = ulmo.usace.swtwc.get_station_data(code, date)

        for key, value in test_data.items():
            if key == 'values':
                _compare_values(test_data['values'], station_data['values'])
            else:
                assert station_data[key] == test_data[key]


def test_get_station_data_current():
    # can't easily test current since it is a moving target changes, but mostly
    # just make sure it parses correctl: current will have '---' values where
    # previous days do not
    data_file = 'usace/swtwc/MYST2.current.html'
    with test_util.mocked_urls(data_file):
        station_data = ulmo.usace.swtwc.get_station_data('MYST2')
    assert len(station_data.get('values')) > 0


def test_get_station_data_out_of_range():
    # can't easily test current since it is a moving target changes, but mostly
    # just make sure it parses correctl: current will have '---' values where
    # previous days do not
    data_file = 'usace/swtwc/empty.html'
    with test_util.mocked_urls(data_file):
        with pytest.raises(ValueError):
            station_data = ulmo.usace.swtwc.get_station_data('MYST2', '1945-01-01')


def _compare_values(test_values, station_values):
    for key, test_value in test_values.items():
        assert station_values[key] == test_value
