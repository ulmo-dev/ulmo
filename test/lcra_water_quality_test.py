from ulmo.lcra.waterquality import get_sites, get_site_data
import test_util
import os

def test_get_sites():
    service_info_url = 'http://waterquality.lcra.org/sitelist.aspx'
    service_info_file = 'lcra/waterquality/sites.html'

    url_files = {
        (service_info_url, ('GET',)): service_info_file,
    }

    with test_util.mocked_urls(url_files):
        sites = get_sites()

    assert len(sites) == 6
    assert "SH 35 SOUTHWEST" in sites['20460'] 

def test_get_site_data():
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
        results = get_site_data(12147)

    assert len(results) == 12
    for data in results:
        assert data['Site'] == u'12147'

    del os.environ["ULMO_TESTING"]