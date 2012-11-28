from ulmo.ncdc import ghcn_daily

import test_util


def test_get_stations_as_dicts():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations()
    assert len(stations) > 80000


def test_get_stations_as_dataframe():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(as_dataframe=True)
    assert len(stations) > 80000


def test_get_stations_by_country():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(country='US', as_dataframe=True)
    assert 45000 < len(stations) < 46000


def test_get_stations_by_state():
    with test_util.mocked_requests('ghcnd-stations.txt'):
        stations = ghcn_daily.core.get_stations(state='TX', as_dataframe=True)
    assert 3200 < len(stations) < 3300
