import os

import tables

import pyhis


TEST_FILE_PATH = '/tmp/pyhis_test.h5'


def test_init():
    os.remove(TEST_FILE_PATH)
    assert not os.path.exists(TEST_FILE_PATH)
    pyhis.usgs.pytables.init_h5(TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH)


def test_parse_get_sites():
    site_files = ['RI_daily.xml', 'RI_instantaneous.xml']
    sites = {}
    for site_file in site_files:
        with open(site_file, 'r') as f:
            sites.update(pyhis.usgs.core._parse_sites(f))

    assert len(sites) == 63
    return sites


def test_update_site_list():
    assert _count_sites() == 0
    sites = test_parse_get_sites()
    pyhis.usgs.pytables._update_site_table(sites, TEST_FILE_PATH)
    assert _count_sites() == 63


def test_pytables_get_sites():
    sites = pyhis.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert len(sites) == 63


def _count_sites():
    h5file = tables.openFile(TEST_FILE_PATH, mode="r")
    sites_table = h5file.root.usgs.sites
    number_of_sites = len([1 for i in sites_table.iterrows()])
    h5file.close()
    return number_of_sites
