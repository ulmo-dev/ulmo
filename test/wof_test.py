import ulmo

def test_core_get_sites_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    assert len(sites) == 14


def test_core_get_sites_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 34
