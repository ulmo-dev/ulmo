import numpy as np
import pandas

from ulmo import util
from ulmo.ncdc import ghcn_daily

import test_util


test_stations = [
    {
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
    },
]

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
    'USC00411885': {
        'PRCP': {
            '1912-09-01': (0, 'P', np.nan, '6'),
            '1912-09-05': (0, 'P', np.nan, '6'),
            '1912-09-06': (0, 'P', np.nan, '6'),
            '1912-09-07': (0, 'P', np.nan, '6'),
            '1912-09-08': (0, 'P', np.nan, '6'),
            '1912-09-30': (0, 'P', np.nan, '6'),
        },
    },
}


def test_get_data_as_dataframes():
    for station_id, sample_data in test_data.items():
        elements = list(sample_data.keys())
        with test_util.mocked_urls('ncdc/ghcnd/%s.dly' % station_id):
            station_data = ghcn_daily.get_data(
                station_id, elements=elements, as_dataframe=True)

            for element_id, element_test_data in sample_data.items():
                element_df = station_data[element_id]
                for date, test_value in element_test_data.items():
                    date = pandas.Period(pandas.Timestamp(date), freq='D')
                    value = element_df.xs(date)
                    test_array = np.array(test_value, dtype=value.dtype)

                    nulls = pandas.isnull(value)

                    assert np.all(pandas.isnull(test_array) == nulls)
                    assert np.all(value[~nulls.values] == test_array[~nulls.values])


def test_get_data_as_dicts():
    for station_id, sample_data in test_data.items():
        elements = list(sample_data.keys())
        with test_util.mocked_urls('ncdc/ghcnd/%s.dly' % station_id):
            station_data = ghcn_daily.get_data(station_id, elements=elements)

            for element_id, element_test_data in sample_data.items():
                element_dict = station_data[element_id]
                for date, test_value in element_test_data.items():
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
    with test_util.mocked_urls('ncdc/ghcnd/ghcnd-stations.txt'):
        stations = ghcn_daily.get_stations()
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        assert stations.get(station_id) == test_station


def test_get_stations_as_dataframe():
    with test_util.mocked_urls('ncdc/ghcnd/ghcnd-stations.txt'):
        stations = ghcn_daily.get_stations(as_dataframe=True)
    assert len(stations) > 80000

    for test_station in test_stations:
        station_id = test_station.get('id')
        station = stations.xs(station_id)
        station_dict = util.misc._nans_to_nones(station.to_dict())
        assert station_dict == test_station


def test_get_stations_by_country():
    with test_util.mocked_urls('ncdc/ghcnd/ghcnd-stations.txt'):
        stations = ghcn_daily.get_stations(country='US', as_dataframe=True)
    assert len(stations) > 45000


def test_get_stations_by_state():
    with test_util.mocked_urls('ncdc/ghcnd/ghcnd-stations.txt'):
        stations = ghcn_daily.get_stations(state='TX', as_dataframe=True)
    assert len(stations) > 3200


def test_get_stations_with_date_range():
    test_ranges = [
        {
            'start': 2011,
            'end': None,
            'includes': [
                'KE000063661',
                'USS0021E07S',
                'ZI000067983',
            ],
            'excludes': [
                'JQW00021601',
                'USC00448257',
                'ZI000067991',
            ],
        }, {
            'start': None,
            'end': 1920,
            'includes': [
                'USW00094957',
                'WZ004451000',
                'WZ004455110',
                'WZ004834260',
            ],
            'excludes': [
                'ASN00005063',
                'CA00405DJDN',
                'CA005040896',
            ],
        }, {
            'start': 1937,
            'end': 1945,
            'includes': [
                'ASN00015621',
                'ASN00023053',
                'WZ004451000',
                'WZ004834260',
            ],
            'excludes': [
                'ASN00041460',
                'ASN00023301',
                'US1COLR0770',
                'US1COLR0850',
            ],
        }, {
            'start': 1960,
            'end': 1960,
            'includes': [
                'ASN00078019',
                'ASN00041435',
            ],
            'excludes': [
                'US1COLR0770',
                'US1COLR0850',
            ],
        },
    ]

    url_files = {
        'ghcnd-stations': 'ncdc/ghcnd/ghcnd-stations.txt',
        'ghcnd-inventory': 'ncdc/ghcnd/ghcnd-inventory.txt'
    }

    with test_util.mocked_urls(url_files):
        for test_range in test_ranges:
            start = test_range.get('start')
            end = test_range.get('end')
            stations = ghcn_daily.get_stations(start_year=start,
                end_year=end, as_dataframe=True)
            _check_stations_dataframe(stations,
                test_range.get('includes'),
                test_range.get('excludes'))


def test_get_stations_with_elements():
    test_elements = [
        {
            'elements': 'PRCP',
            'includes': [
                'ASN00008230',
                'WA006567710',
                'VQC00672823',
            ],
            'excludes': ['SWE00136141', 'USR0000OHOR', 'USC00450935', 'USR0000THEN', 'USR0000MDRY'],
        }, {
            'elements': ['SNOW', 'TMAX'],
            'includes': [
                'ACW00011604',
                'USW00094895',
                'VQW00011640',
                'ZI000067991',
            ],
            'excludes': ['BR037642870', 'BR00C8-0100', 'BR048519530', 'BR002548070', 'IN009081600']
        },
    ]
    url_files = {
        'ghcnd-stations': 'ncdc/ghcnd/ghcnd-stations.txt',
        'ghcnd-inventory': 'ncdc/ghcnd/ghcnd-inventory.txt'
    }

    with test_util.mocked_urls(url_files):
        for test_element in test_elements:
            elements = test_element.get('elements')
            stations = ghcn_daily.get_stations(elements=elements,
                as_dataframe=True)
            _check_stations_dataframe(stations,
                test_element.get('includes'),
                test_element.get('excludes'))


def _check_stations_dataframe(stations, includes, excludes):
    for include in includes:
        assert include in stations['id']
    for exclude in excludes:
        assert not exclude in stations['id']
