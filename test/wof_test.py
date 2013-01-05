import ulmo

import test_util

def test_core_get_sites_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_sites_file = 'muddyriver_1_0_get_sites.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSitesXml=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 14


def test_core_get_sites_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_sites_file = 'get_sites_ipswich_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSites=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 34
