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
        ('MYST2', '2018-02-03', {
            'code': 'MYST2',
            'description': 'Pat Mayse Lake',
            'station_type': 'RESERVOIR',
            'timezone': 'US/Central',
            'values': {
                '2018-02-03 01:00:00': {'PRECIP PRE': 0.0, 'CIP(A) ELE': 0.0, 'VATION   S': 451.61, 'TORAGE': 121347.0, 'INFLOW   R': 0.0, 'ELEASE  AI': 59.0, 'R-TEMP  WI': 35.4, 'ND-DIRWIND': 75.0, '-SPEED REL': 5.36, '-HUMID SOL': 41.52, 'AR-RAD   V': -2.0, 'OLTAGE  BA': 12.37}
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
    data_file = 'usace/swtwc/DSNT2.current.html'
    with test_util.mocked_urls(data_file):
        station_data = ulmo.usace.swtwc.get_station_data('DSNT2')
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
