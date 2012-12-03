import pandas

from ulmo.ncdc import ghcn_daily

import test_util


test_stations = [{
        'country': 'US',
        'elevation': 286.5,
        'gsn_flag': 'GSN',
        'hcn_flag': 'HCN',
        'id': 'USW00003870',
        'latitude': 34.8831,
        'longitude': -82.2203,
        'name': 'GREER',
        'network': 'W',
        'network_id': '00003870',
        'state': 'SC',
        'wm_oid': '72312'
    }, {
        'country': 'US',
        'elevation': 91.1,
        'gsn_flag': None,
        'hcn_flag': None,
        'id': 'USW00003850',
        'latitude': 31.2667,
        'longitude': -85.7167,
        'name': 'CAIRNS FLD FT RUCKER',
        'network': 'W',
        'network_id': '00003850',
        'state': 'AL',
        'wm_oid': None
    }]


def test_get_stations_as_dicts():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations()
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        assert stations.get(station_id) == test_station


def test_get_stations_as_dataframe():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(as_dataframe=True)
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        station = stations.xs(station_id)
        station[pandas.isnull(station)] = None
        station_dict = station.to_dict()
        assert station_dict == test_station


def test_get_stations_by_country():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(country='US', as_dataframe=True)
    assert 45000 < len(stations) < 46000


def test_get_stations_by_state():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(state='TX', as_dataframe=True)
    assert 3200 < len(stations) < 3300
