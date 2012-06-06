import datetime
import os

import isodate
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
    assert _count_rows('/usgs/sites') == 0
    sites = test_parse_get_sites()
    pyhis.usgs.pytables._update_site_table(sites, TEST_FILE_PATH)
    assert _count_rows('/usgs/sites') == 63


def test_pytables_get_sites():
    sites = pyhis.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert len(sites) == 63


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
