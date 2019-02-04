import pytest

import ulmo

import test_util


TEST_FILE_PATH = '/tmp/ulmo_test.h5'


def test_get_sites_by_state_code():
    mocked_urls = {
        'http://waterservices.usgs.gov/nwis/dv/':
            'usgs/nwis/RI_daily.xml',
        'http://waterservices.usgs.gov/nwis/iv/':
            'usgs/nwis/RI_instantaneous.xml',
    }

    with test_util.mocked_urls(mocked_urls):
        sites = ulmo.usgs.nwis.get_sites(state_code='RI')
    assert len(sites) > 64


def test_get_sites_by_county_code():
    county_code='51059,51061'
    sites_data_file = 'usgs/nwis/sites_county_%s_daily.xml' % county_code
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(county_code=county_code, service='dv')
    assert len(sites) > 23


def test_get_sites_by_huc():
    huc='02070010'
    sites_data_file = 'usgs/nwis/sites_huc_%s_daily.xml' % huc
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(huc=huc, service='dv')
    assert len(sites) > 61


def test_get_sites_with_extra_kwarg():
    sites_data_file = 'usgs/nwis/sites_kwarg_agencyCD.xml'
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(state_code='TX', agencyCD='USCE', service='dv')
    assert len(sites) == 1


def test_get_sites_single_site():
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    with test_util.mocked_urls(site_data_file):
        sites = ulmo.usgs.nwis.get_sites(sites=site_code)
    assert len(sites) == 1


def test_get_site_data_single_site():
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    with test_util.mocked_urls(site_data_file):
        site_data = ulmo.usgs.nwis.get_site_data(site_code, methods='all')
    assert len(site_data) == 26


def test_get_site_data_bad_service_raises_error():
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    with test_util.mocked_urls(site_data_file):
        with pytest.raises(ValueError):
            ulmo.usgs.nwis.get_site_data(site_code,
                    service="bad_service")


def test_get_site_data_single_site_with_start_and_end():
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_08068500_instantaneous_2011-11-05_2011-11-18.xml'
    with test_util.mocked_urls(site_data_file):
        site_data = ulmo.usgs.nwis.get_site_data(site_code, start='2011-11-05',
                end='2011-11-18', service='instantaneous',
                methods={'00065': '2'})
    assert len(site_data) == 6
    assert len(site_data['63680:00000']['values']) == 1250


def test_get_site_data_single_site_with_period():
    site_data_file = 'usgs/nwis/site_01117800_instantaneous_P45D.xml'
    site_code = '01117800'
    with test_util.mocked_urls(site_data_file):
        site_data = ulmo.usgs.nwis.get_site_data(site_code, period='P45D',
                service='daily')
    assert len(site_data) >= 1
    assert len(site_data['00060:00003']['values']) == 45


def test_get_sites_multiple_sites():
    site_codes = ['08068500', '08041500']
    sites_data_file = 'usgs/nwis/sites_%s_daily.xml' % '_'.join(site_codes)
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(sites=site_codes)
    assert len(sites) == 2


def test_get_sites_by_bounding_box():
    bounding_box_values = '-83.0,36.5,-81.0,38.5'
    sites_data_file = 'usgs/nwis/sites_%s_daily.xml' % bounding_box_values
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(bounding_box=bounding_box_values, service='dv')
    assert len(sites) > 244

    
def test_get_sites_by_serving_parameter_code():
    site_code = '08068500'
    parameter_code_value = '00060'
    sites_data_file = 'usgs/nwis/sites_%s_%s_daily.xml' % (site_code, parameter_code_value)
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(sites=site_code, parameter_code=parameter_code_value, service='dv')
    assert len(sites) == 1

    
def test_get_sites_by_multiple_serving_parameter_code():
    site_code = '08068500'
    parameter_code_values = '00060,00065'
    sites_data_file = 'usgs/nwis/sites_%s_%s_daily.xml' % (site_code, parameter_code_values)
    with test_util.mocked_urls(sites_data_file):
        sites = ulmo.usgs.nwis.get_sites(sites=site_code, parameter_code=parameter_code_values, service='dv')
    assert len(sites) == 1

def test_get_site_data_multiple_methods():
    site_code = '08054500'
    site_data_file = 'usgs/nwis/site_08054500_multiple_methods.xml'
    with test_util.mocked_urls(site_data_file):
        site_data = ulmo.usgs.nwis.get_site_data(site_code, methods={'62614': 'all', '45592': 'all'})
        assert len(site_data['00054:00003']['values']) == 1
        assert len(site_data.keys()) == 17
