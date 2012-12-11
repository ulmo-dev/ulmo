import os.path

import numpy as np
import pandas

from ulmo.ncdc import ghcn_daily

import test_util

import pytest

__module__ = pytest.mark.ghcn_daily


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

test_data = {
    'USW00003870': {
        'ACMH': {
            '1965-03-27': (50, np.nan, np.nan, 'X'),
        },
        'PRCP': {
            '1962-10-01': (np.nan, np.nan, np.nan, np.nan),
            '1962-10-14': (np.nan, np.nan, np.nan, np.nan),
            '1962-10-15': (0, np.nan, np.nan, 'X'),
            '1962-10-16': (0, 'T', np.nan, 'X'),
            '1962-10-17': (0, np.nan, np.nan, 'X'),
            '1962-10-21': (102, np.nan, np.nan, 'X'),
            '1962-10-31': (30, np.nan, np.nan, 'X'),
            '1963-02-01': (15, np.nan, np.nan, '0'),
            '1963-02-28': (0, np.nan, np.nan, '0'),
            '1963-03-01': (249, np.nan, np.nan, '0'),
            '1984-02-01': (0, np.nan, np.nan, '0'),
            '1984-02-06': (8, np.nan, np.nan, '0'),
            '1984-02-28': (20, np.nan, np.nan, '0'),
            '1984-02-29': (0, np.nan, np.nan, '0'),
            '1984-03-01': (0, np.nan, np.nan, '0'),
            '1984-03-05': (287, np.nan, np.nan, '0'),
            '2012-03-01': (0, 'T', np.nan, 'X'),
            '2012-03-02': (10, np.nan, np.nan, 'X'),
            '2012-03-03': (422, np.nan, np.nan, 'X'),
        },
    },
}

mocked_stations_file = 'ghcnd-stations.txt'


def test_get_data_as_dataframes():
    for station_id, sample_data in test_data.iteritems():
        elements = sample_data.keys()
        station_data = ghcn_daily.core.get_data(station_id, elements=elements,
                as_dataframe=True)

        for element_id, element_test_data in sample_data.iteritems():
            element_df = station_data[element_id]
            for date, test_value in element_test_data.iteritems():
                value = element_df.xs(date)
                test_array = np.array(test_value, dtype=value.dtype)

                nulls = pandas.isnull(value)

                assert np.all(pandas.isnull(test_array) == nulls)
                assert np.all(value[~nulls] == test_array[~nulls])


def test_get_data_as_dicts():
    for station_id, sample_data in test_data.iteritems():
        elements = sample_data.keys()
        station_data = ghcn_daily.core.get_data(station_id, elements=elements)

        for element_id, element_test_data in sample_data.iteritems():
            element_dict = station_data[element_id]
            for date, test_value in element_test_data.iteritems():
                value_dict = element_dict[date]
                values = [
                    value_dict.get(v)
                    for v in ['value', 'mflag', 'qflag', 'sflag']
                ]
                value = np.array(values, dtype=object)
                test_array = np.array(test_value, dtype=value.dtype)

                nulls = pandas.isnull(value)

                assert np.all(pandas.isnull(test_array) == nulls)
                assert np.all(value[~nulls] == test_array[~nulls])


def test_get_stations_as_dicts():
    with test_util.mocked_requests(mocked_stations_file):
        stations = ghcn_daily.core.get_stations()
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        assert stations.get(station_id) == test_station


def test_get_stations_as_dataframe():
    with test_util.mocked_requests(mocked_stations_file):
        stations = ghcn_daily.core.get_stations(as_dataframe=True)
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        station = stations.xs(station_id)
        station[pandas.isnull(station)] = None
        station_dict = station.to_dict()
        assert station_dict == test_station


def test_get_stations_by_country():
    with test_util.mocked_requests(mocked_stations_file):
        stations = ghcn_daily.core.get_stations(country='US', as_dataframe=True)
    assert 45000 < len(stations) < 47000


def test_get_stations_by_state():
    with test_util.mocked_requests(mocked_stations_file):
        stations = ghcn_daily.core.get_stations(state='TX', as_dataframe=True)
    assert 3200 < len(stations) < 3300


