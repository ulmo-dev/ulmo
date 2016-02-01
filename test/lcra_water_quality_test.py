import os
import pandas
from ulmo.lcra.waterquality import get_sites, get_historical_data, get_recent_data
import test_util

def test_get_sites():
    data_file = 'lcra/waterquality/sites.html'
    with test_util.mocked_urls(data_file):
        sites = get_sites()

    assert len(sites['features']) == 469


def test_get_historical_data():
    parameters_file = 'lcra/waterquality/12147_params.html'
    data_file = 'lcra/waterquality/12147_results.html'

    with test_util.mocked_urls(data_file):
        results = get_historical_data(12147)

    assert len(results) == 12
    for data in results:
        assert data['Site'] == u'12147'

def test_get_recent_data():
    data_file = 'lcra/waterquality/recent_data_site_6996.html'
    with test_util.mocked_urls(data_file):
        site_data = get_recent_data('6996', as_dataframe=True)

    assert site_data.size > 0
