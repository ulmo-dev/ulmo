from builtins import range
import datetime
import ulmo

import test_util


def test_get_stations():
    test_stations = [
        ('999999-94645', {
            'USAF': '999999',
            'WBAN': '94645',
            'begin': datetime.date(2002, 9, 20),
            'icao': '',
            'country': 'US',
            'elevation': 224.6,
            'end': datetime.date(2015, 3, 11),
            'latitude': 46.96,
            'longitude': -67.883,
            'name': 'LIMESTONE 4 NNW',
            'state': 'ME',
        }),
        ('999999-14896', {
            'USAF': '999999',
            'WBAN': '14896',
            'begin': datetime.date(1952, 1, 1),
            'icao': '',
            'country': 'US',
            'elevation': 323.1,
            'end': datetime.date(1957, 11, 30),
            'latitude': 41.033,
            'longitude': -81.483,
            'name': 'AKRON NAS',
            'state': 'OH'
        }),
        ('014881-99999', {
            'USAF': '014881',
            'WBAN': '99999',
            'begin': datetime.date(2010, 11, 23),
            'icao': 'ENFB',
            'country': 'NO',
            'elevation': 142.0,
            'end': datetime.date(2015, 3, 11),
            'latitude': 61.206,
            'longitude': 1.829,
            'name': 'STATFJORD B OIL PLATFORM',
            'state': ''
        }),
        ('997944-99999', {
            'USAF': '997944',
            'WBAN': '99999',
            'begin': datetime.date(2008, 7, 24),
            'icao': '',
            'country': 'US',
            'elevation': None,
            'end': datetime.date(2009, 9, 27),
            'latitude': None,
            'longitude': None,
            'name': 'DRIFTING BUOY 48592',
            'state': '',
        }),
    ]
    with test_util.mocked_urls('ncdc/gsod/isd-history.csv'):
        stations = ulmo.ncdc.gsod.get_stations()

    assert 27000 < len(stations) < 32000

    for test_code, test_station in test_stations:
        # drop end date from test
        del stations[test_code]['end']
        del test_station['end']
        assert stations[test_code] == test_station


def test_get_stations_with_country():
    with test_util.mocked_urls('ncdc/gsod/isd-history.csv'):
        stations = ulmo.ncdc.gsod.get_stations(country='AF')
        assert len(stations) > 100
        assert '409900-99999' in stations

        stations = ulmo.ncdc.gsod.get_stations(country=['US', 'MX', 'CA'])
        assert len(stations) > 9500
        assert '768420-99999' in stations
        assert '911660-99999' in stations
        assert '729675-99999' in stations


def test_get_stations_with_state():
    with test_util.mocked_urls('ncdc/gsod/isd-history.csv'):
        stations = ulmo.ncdc.gsod.get_stations(state='TX')
        assert len(stations) > 450
        assert '999999-93987' in stations

        stations = ulmo.ncdc.gsod.get_stations(state=['TX', 'AR', 'LA'])
        assert len(stations) > 750
        assert '999999-93987' in stations
        assert '999999-13963' in stations
        assert '994780-99999' in stations


def test_get_stations_with_start():
    with test_util.mocked_urls('ncdc/gsod/isd-history.csv'):
        stations = ulmo.ncdc.gsod.get_stations(start='2011-3-2')
    assert len(stations) > 15000
    assert '062390-99999' in stations
    assert '534780-99999' not in stations


def test_get_stations_with_end():
    with test_util.mocked_urls('ncdc/gsod/isd-history.csv'):
        stations = ulmo.ncdc.gsod.get_stations(end='1960-11-5')
    assert len(stations) > 8500
    assert '534780-99999' in stations
    assert '062390-99999' not in stations


def test_get_station_data():
    test_data = [
        (dict(
            station_codes='999999-14896',
            start='1952-01-01',
            end='1953-02-02'),
            [{
                'FRSHTT': '010000',
                'USAF': '999999',
                'WBAN': '14896',
                'date': datetime.date(1952, 1, 1),
                'dew_point': 52.4,
                'dew_point_count': 8,
                'max_gust': 999.9,
                'max_temp': 62.1,
                'max_temp_flag': '*',
                'max_wind_speed': 12.0,
                'mean_temp': 56.0,
                'mean_temp_count': 8,
                'mean_wind_speed': 9.0,
                'mean_wind_speed_count': 8,
                'min_temp': 48.0,
                'min_temp_flag': '*',
                'precip': 99.99,
                'precip_flag': ' ',
                'sea_level_pressure': 1014.4,
                'sea_level_pressure_count': 8,
                'snow_depth': 999.9,
                'station_pressure': 978.2,
                'station_pressure_count': 8,
                'visibility': 5.5,
                'visibility_count': 8,
            }, {
                'FRSHTT': '000000',
                'USAF': '999999',
                'WBAN': '14896',
                'date': datetime.date(1952, 1, 3),
                'dew_point': 18.4,
                'dew_point_count': 9,
                'max_gust': 999.9,
                'max_temp': 30.9,
                'max_temp_flag': '*',
                'max_wind_speed': 10.1,
                'mean_temp': 27.2,
                'mean_temp_count': 9,
                'mean_wind_speed': 8.3,
                'mean_wind_speed_count': 9,
                'min_temp': 23.0,
                'min_temp_flag': '*',
                'precip': 0.0,
                'precip_flag': 'I',
                'sea_level_pressure': 1033.0,
                'sea_level_pressure_count': 9,
                'snow_depth': 999.9,
                'station_pressure': 991.4,
                'station_pressure_count': 9,
                'visibility': 10.6,
                'visibility_count': 9,
            }, {
                'FRSHTT': '001000',
                'USAF': '999999',
                'WBAN': '14896',
                'date': datetime.date(1953, 2, 2),
                'dew_point': 12.0,
                'dew_point_count': 20,
                'max_gust': 999.9,
                'max_temp': 36.0,
                'max_temp_flag': '*',
                'max_wind_speed': 13.0,
                'mean_temp': 22.6,
                'mean_temp_count': 20,
                'mean_wind_speed': 8.2,
                'mean_wind_speed_count': 20,
                'min_temp': 14.0,
                'min_temp_flag': '*',
                'precip': 99.99,
                'precip_flag': ' ',
                'sea_level_pressure': 1022.8,
                'sea_level_pressure_count': 20,
                'snow_depth': 999.9,
                'station_pressure': 982.6,
                'station_pressure_count': 20,
                'visibility': 9.2,
                'visibility_count': 20,
            },
            ]
         ),
        (dict(
            station_codes='999999-14896',
            start='1952-01-01',
            end='1953-02-02',
            parameters='snow_depth'),
            [{
                'date': datetime.date(1952, 1, 1),
                'snow_depth': 999.9,
            }, {
                'date': datetime.date(1952, 1, 3),
                'snow_depth': 999.9,
            }, {
                'date': datetime.date(1953, 2, 2),
                'snow_depth': 999.9,
            },
            ]
         ),
        (dict(
            station_codes='999999-14896',
            start='1952-01-01',
            end='1953-02-02',
            parameters=['station_pressure', 'dew_point']),
            [{
                'date': datetime.date(1952, 1, 1),
                'dew_point': 52.4,
                'station_pressure': 978.2,
            }, {
                'date': datetime.date(1952, 1, 3),
                'dew_point': 18.4,
                'station_pressure': 991.4,
            }, {
                'date': datetime.date(1953, 2, 2),
                'dew_point': 12.0,
                'station_pressure': 982.6,
            },
            ]
         ),

    ]

    for kwargs, test_values in test_data:
        start = kwargs.get('start')
        end = kwargs.get('end')
        station_code = kwargs.get('station_codes')

        start_year = int(start.split('-')[0])
        end_year = int(end.split('-')[0])

        url_files = dict([
            ('http://www1.ncdc.noaa.gov/pub/data/gsod/%s/gsod_%s.tar' % (year, year),
                'ncdc/gsod/gsod_%s.tar' % year)
            for year in range(start_year, end_year + 1)
        ])

        with test_util.mocked_urls(url_files):
            station_data = ulmo.ncdc.gsod.get_data(**kwargs)

        for test_value in test_values:
            assert test_value in station_data[station_code]
