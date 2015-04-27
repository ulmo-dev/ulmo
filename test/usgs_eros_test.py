import pytest

import ulmo

import test_util


def test_get_attribute_list():
    attribute_list = ulmo.usgs.eros.get_attribute_list(as_dataframe=True)
    assert len(attribute_list) == 38

def test_get_themes():
    themes = ulmo.usgs.eros.get_themes(as_dataframe=True)
    assert len(themes) == 22

test_sets = [
	{'layer': '1 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	},
	{'layer': '1/3 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	},
	{'layer': 'Alaska 2 arc-second',
	 'bbox': (-150.4969, 60.7338, -148.4600, 61.5253),
	},
]


def test_get_site_available_datasets():
    available_dataSets = ulmo.usgs.eros.get_available_datasets(*test_sets[0]['bbox'], epsg=4326, attrs=None, as_dataframe=True)    
    assert len(available_dataSets) == 29

def test_get_site_available_formats():
    available_dataSets = ulmo.usgs.eros.get_available_datasets(*test_sets[0]['bbox'], epsg=4326, attrs=None, as_dataframe=True)    
    product_key = str(available_dataSets['PRODUCTKEY'][12])    
    
    available_formats = ulmo.usgs.eros.get_available_formats(product_key, as_dataframe=True)
     
    assert len(available_formats) == 1

"""
def test_get_site_data_single_site_with_start_and_end():
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_08068500_instantaneous_2011-11-05_2011-11-18.xml'
    with test_util.mocked_urls(site_data_file):
        site_data = ulmo.usgs.nwis.get_site_data(site_code, start='2011-11-05',
                end='2011-11-18', service='instantaneous')
    assert len(site_data) == 7
    assert len(site_data['63680:00011']['values']) == 1250


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
"""