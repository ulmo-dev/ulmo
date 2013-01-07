import ulmo

import test_util


def test_core_get_sites_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_sites_file = 'get_sites_muddyriver_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSitesXml=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 14


def test_core_get_sites_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_sites_file = 'get_sites_ipswich_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSites=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 34


def test_core_get_site_info_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    site_info_file = 'get_site_info_muddyriver_14_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.wof.core.get_site_info(WSDL_URL, 'MuddyRiver:MuddyRiver_14')
    assert site_info['code'] == 'MuddyRiver_14'
    assert site_info['network'] == 'MuddyRiver'
    assert 'MR:MuddyRiver_ACID' in site_info['series']
    assert 'MR:MuddyRiver_pH' in site_info['series']
    assert 'MR:MuddyRiver_ZN' in site_info['series']
    assert len(site_info['series']) == 27


def test_core_get_site_data_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    site_info_file = 'get_site_info_ipswich_MMB_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.wof.core.get_site_info(WSDL_URL, 'ipswich:MMB')
    assert site_info['code'] == 'MMB'
    assert site_info['network'] == 'ipswich'
    assert 'ipswich:Temp' in site_info['series']
    assert 'ipswich:DO' in site_info['series']
    assert len(site_info['series']) == 3
