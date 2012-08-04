import pyhis

TEST_FILE_PATH = '/tmp/pyhis_test.h5'
TWDB_WSDL_URL = 'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL'


#def test_init():
    #_remove_test_file()
    #assert not os.path.exists(TEST_FILE_PATH)
    #pyhis.usgs.pytables.init_h5(TEST_FILE_PATH)
    #assert os.path.exists(TEST_FILE_PATH)


def test_core_get_sites():
    sites = pyhis.wof.core.get_sites(TWDB_WSDL_URL)
    import pytest; pytest.set_trace()
    assert len(sites) == 74

