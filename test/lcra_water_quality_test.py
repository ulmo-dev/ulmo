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
    os.environ["ULMO_TESTING"] ="1"

    service_info_url = 'http://waterquality.lcra.org/parameter.aspx?qrySite=12147'
    service_info_file = 'lcra/waterquality/12147_params.html'

    service_data_url = 'http://waterquality.lcra.org/events.aspx'
    service_data_file = 'lcra/waterquality/12147_results.html'

    url_files = {
        (service_info_url, ('GET',)): service_info_file,
        (service_data_url, ('POST',)): service_data_file,
    }

    with test_util.mocked_urls(url_files):
        results = get_historical_data(12147)

    assert len(results) == 12
    for data in results:
        assert data['Site'] == u'12147'

    del os.environ["ULMO_TESTING"]


def test_get_recent_data():
    data_file = 'lcra/waterquality/recent_data_site_6996.html'
    test_values = pandas.DataFrame([
        {'salinity_ppt': 15.46,
          'ph': 7.84,
          'depth_m': 1.17,
          'do_mgperl': 8.15,
          'do_sat_percent': 87.70,
          'water_temp_deg_c': 14.36},
        {'salinity_ppt': 15.72,
         'ph': 7.82,
         'depth_m': 1.12,
         'do_mgperl': 7.97,
         'do_sat_percent': 85.70,
         'water_temp_deg_c': 14.28
         },
    ], index=[pandas.Timestamp('2015-12-04 03:25:00'),
              pandas.Timestamp('2015-12-04 04:40:00')])
    with test_util.mocked_urls(data_file):
        site_data = get_recent_data('6996', as_dataframe=True)

    are_equal = test_values == site_data.ix[test_values.index][test_values.columns]
    assert pandas.np.all(are_equal)
    assert site_data.shape[0] == 256
