import ulmo

import test_util


def test_get_stations():
    stations_file = 'usace/rivergages/get_stations.cfm'
    with test_util.mocked_requests(stations_file):
        stations = ulmo.usace.rivergages.get_stations()
    assert 1900 <= len(stations) <= 2000
    assert 'CE7F42E6' in stations


def test_get_station_parameters():
    test_values = [
            ('CE7F42E6', {
                'HP': u'Pool Level (Ft)',
                'PC': u'Cumulative Precipitation (In)'
            })
    ]

    for station_code, test_value in test_values:
        stations_file = 'usace/rivergages/parameters_%s.cfm' % station_code
        with test_util.mocked_requests(stations_file):
            parameters = ulmo.usace.rivergages.get_station_parameters(station_code)

        assert parameters == test_value
