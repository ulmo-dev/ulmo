import ulmo

import test_util


def test_get_stations():
    stations_file = 'usace/rivergages/get_stations.cfm'
    with test_util.mocked_requests(stations_file):
        stations = ulmo.usace.rivergages.get_stations()
    assert 1900 <= len(stations) <= 2000
    assert 'CE7F42E6' in stations
