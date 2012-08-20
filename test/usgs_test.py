import datetime
import os

import isodate
import tables
import pytest

import pyhis


TEST_FILE_PATH = '/tmp/pyhis_test.h5'


def test_init():
    _remove_test_file()
    assert not os.path.exists(TEST_FILE_PATH)
    pyhis.usgs.pytables.init_h5(TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH)


def test_parse_get_sites():
    site_files = ['RI_daily.xml', 'RI_instantaneous.xml']
    sites = {}
    for site_file in site_files:
        with open(site_file, 'r') as f:
            sites.update(pyhis.waterml.v1_1.parse_sites(f))

    assert len(sites) == 63
    return sites


def test_update_site_table():
    test_init()
    assert _count_rows('/usgs/sites') == 0
    sites = test_parse_get_sites()
    pyhis.usgs.pytables._update_site_table(sites.values(), TEST_FILE_PATH)
    assert _count_rows('/usgs/sites') == 63


def test_pytables_get_sites():
    sites = pyhis.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert len(sites) == 63


def test_pytables_get_site():
    pyhis.usgs.pytables.get_sites(TEST_FILE_PATH)
    site = pyhis.usgs.pytables.get_site('01115100', TEST_FILE_PATH)
    assert len(site) == 11


def test_pytables_get_site_fallback_to_core():
    site_code = '08068500'
    sites = pyhis.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert site_code not in sites
    site = pyhis.usgs.pytables.get_site(site_code, TEST_FILE_PATH)
    assert len(site) == 11


def test_pytables_get_site_raises_lookup():
    with pytest.raises(LookupError):
        pyhis.usgs.pytables.get_site('98068500', TEST_FILE_PATH)


def test_update_or_append():
    h5file = tables.openFile(TEST_FILE_PATH, mode="r+")
    test_table = _create_test_table(h5file, 'update_or_append', pyhis.usgs.pytables.USGSValue)
    where_filter = '(datetime == "%(datetime)s")'

    initial_values = [
            {'datetime': isodate.datetime_isoformat(datetime.datetime(2000, 1, 1) + \
                datetime.timedelta(days=i)),
             'value': 'initial',
             'qualifiers': ''}
            for i in range(1000)]

    update_values = [
            {'datetime': isodate.datetime_isoformat(datetime.datetime(2000, 1, 1) + \
                datetime.timedelta(days=i)),
             'value': 'updated',
             'qualifiers': ''}
            for i in [20, 30, 10, 999, 1000, 2000, 399]]

    pyhis.usgs.pytables._update_or_append(test_table, initial_values, where_filter)
    h5file.close()

    assert _count_rows('/test/update_or_append') == 1000

    h5file = tables.openFile(TEST_FILE_PATH, mode="r+")
    test_table = h5file.getNode('/test/update_or_append')
    pyhis.usgs.pytables._update_or_append(test_table, update_values, where_filter)
    h5file.close()
    assert _count_rows('/test/update_or_append') == 1002


def test_non_usgs_site():
    site_code = '07335390'
    test_init()
    pyhis.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
    site_data = pyhis.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)
    assert len(site_data['00062:32400']['values']) > 1000


def test_update_site_list():
    test_init()
    assert _count_rows('/usgs/sites') == 0
    pyhis.usgs.pytables.update_site_list(state_code='RI', path=TEST_FILE_PATH)
    assert _count_rows('/usgs/sites') == 63


def test_core_get_sites_by_state_code():
    sites = pyhis.usgs.core.get_sites(state_code='RI')
    assert len(sites) == 63


def test_core_get_sites_single_site():
    sites = pyhis.usgs.core.get_sites(sites='08068500')
    assert len(sites) == 1


def test_core_get_sites_multiple_sites():
    sites = pyhis.usgs.core.get_sites(sites=['08068500', '08041500'])
    assert len(sites) == 2


def _count_rows(path):
    h5file = tables.openFile(TEST_FILE_PATH, mode="r")
    table = h5file.getNode(path)
    number_of_rows = len([1 for i in table.iterrows()])
    h5file.close()
    return number_of_rows


def _create_test_table(h5file, table_name, description):
    test_table = h5file.createTable('/test', table_name, description,
                                    createparents=True)
    return test_table


def _remove_test_file():
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)

