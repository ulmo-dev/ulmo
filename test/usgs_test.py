import datetime
import os

import isodate
import pytest
import time

import ulmo

import test_util
import waterml_v1_1_test

try:
    import tables
except ImportError:
    pass


TEST_FILE_PATH = '/tmp/ulmo_test.h5'


def test_init():
    _remove_test_file()


def test_update_sites_table():
    test_init()
    sites = waterml_v1_1_test.test_parse_site_infos()
    ulmo.usgs.pytables._update_sites_table(sites.values(), TEST_FILE_PATH)
    assert _count_rows('/usgs/sites') == 64


def test_pytables_get_sites():
    sites = ulmo.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert len(sites) == 64


def test_pytables_get_site():
    site_code = '08068500'
    site_data_file = 'site_%s_daily.xml' % site_code
    with test_util.mocked_requests(site_data_file):
        ulmo.usgs.pytables.get_site(site_code, TEST_FILE_PATH)

    site = ulmo.usgs.pytables.get_site(site_code, TEST_FILE_PATH)
    assert len(site) == 10


def test_pytables_get_site_fallback_to_core():
    site_code = '07335390'
    site_data_file = 'site_%s_daily.xml' % site_code

    sites = ulmo.usgs.pytables.get_sites(TEST_FILE_PATH)
    assert site_code not in sites

    with test_util.mocked_requests(site_data_file):
        site = ulmo.usgs.pytables.get_site(site_code, TEST_FILE_PATH)

    assert len(site) == 10


def test_pytables_get_site_raises_lookup():
    site_code = '98068500'
    site_data_file = 'site_%s_daily.xml' % site_code

    with test_util.mocked_requests(site_data_file):
        with pytest.raises(LookupError):
            ulmo.usgs.pytables.get_site(site_code, TEST_FILE_PATH)


def test_update_or_append():
    h5file = tables.openFile(TEST_FILE_PATH, mode="r+")
    test_table = _create_test_table(h5file, 'update_or_append', ulmo.usgs.pytables.USGSValue)
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

    ulmo.usgs.pytables._update_or_append(test_table, initial_values, where_filter)
    h5file.close()

    assert _count_rows('/test/update_or_append') == 1000

    h5file = tables.openFile(TEST_FILE_PATH, mode="r+")
    test_table = h5file.getNode('/test/update_or_append')
    ulmo.usgs.pytables._update_or_append(test_table, update_values, where_filter)
    h5file.close()
    assert _count_rows('/test/update_or_append') == 1002


def test_non_usgs_site():
    site_code = '07335390'
    site_data_file = 'site_%s_daily.xml' % site_code
    test_init()
    with test_util.mocked_requests(site_data_file):
        ulmo.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
    site_data = ulmo.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)
    assert len(site_data['00062:32400']['values']) > 1000


def test_update_site_list():
    test_init()

    mocked_urls = {
        'http://waterservices.usgs.gov/nwis/dv/?stateCd=RI&format=waterml':
            'RI_daily.xml',
        'http://waterservices.usgs.gov/nwis/iv/?stateCd=RI&format=waterml':
            'RI_instantaneous.xml',
    }

    with test_util.mocked_requests(mocked_urls):
        ulmo.usgs.pytables.update_site_list(state_code='RI', path=TEST_FILE_PATH)

    assert _count_rows('/usgs/sites') == 64


def test_pytables_update_site_data():
    test_init()
    site_code = '01117800'
    site_data_file = 'site_%s_daily.xml' % site_code
    with test_util.mocked_requests(site_data_file):
        ulmo.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
        site_data = ulmo.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)

        last_value = site_data['00060:00003']['values'][-1]

        assert last_value['value'] == '74'
        assert last_value['last_checked'] == last_value['last_modified']
        original_timestamp = last_value['last_checked']

    # sleep for a second so last_modified changes
    time.sleep(1)

    update_data_file = 'site_%s_daily_update.xml' % site_code
    with test_util.mocked_requests(update_data_file):
        ulmo.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
        site_data = ulmo.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)

    last_value = site_data['00060:00003']['values'][-1]
    assert last_value['last_checked'] != original_timestamp
    assert last_value['last_checked'] == last_value['last_modified']

    modified_timestamp = last_value['last_checked']

    test_values = [
        dict(datetime="1963-01-23T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='7'),
        dict(datetime="1964-01-23T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='1017'),
        dict(datetime="1964-01-24T00:00:00", last_checked=original_timestamp, last_modified=original_timestamp, qualifiers="A", value='191'),
        dict(datetime="1969-05-26T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='1080'),
        dict(datetime="2012-05-25T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='56'),
        dict(datetime="2012-05-26T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='55'),
        dict(datetime="2012-05-27T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='52'),
        dict(datetime="2012-05-28T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='48'),
        dict(datetime="2012-05-29T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='1099'),
        dict(datetime="2012-05-30T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='1098'),
        dict(datetime="2012-05-31T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='41'),
        dict(datetime="2012-06-01T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='37'),
        dict(datetime="2012-06-02T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='1097'),
        dict(datetime="2012-06-03T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='69'),
        dict(datetime="2012-06-04T00:00:00", last_checked=modified_timestamp, last_modified=original_timestamp, qualifiers="P", value='81'),
        dict(datetime="2012-06-05T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='1071'),
        dict(datetime="2012-06-06T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='2071'),
    ]

    for test_value in test_values:
        assert site_data['00060:00003']['values'].index(test_value) >= 0


def test_pytables_last_refresh_gets_updated():
    test_init()
    site_code = '01117800'
    site_data_file = 'site_%s_daily.xml' % site_code
    with test_util.mocked_requests(site_data_file):
        ulmo.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
        site_data = ulmo.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)

    # sleep for a second so last_modified changes
    time.sleep(1)

    update_data_file = 'site_%s_daily_update.xml' % site_code
    with test_util.mocked_requests(update_data_file):
        ulmo.usgs.pytables.update_site_data(site_code, path=TEST_FILE_PATH)
        site_data = ulmo.usgs.pytables.get_site_data(site_code, path=TEST_FILE_PATH)

    last_value = site_data['00060:00003']['values'][-1]
    last_checked = last_value['last_checked']

    site = ulmo.usgs.pytables.get_site(site_code, path=TEST_FILE_PATH)
    with ulmo.util.open_h5file(TEST_FILE_PATH, mode="r+") as h5file:
        last_refresh = ulmo.usgs.pytables._last_refresh(site, h5file)

    assert last_refresh == last_checked


def test_core_get_sites_by_state_code():
    mocked_urls = {
        'http://waterservices.usgs.gov/nwis/dv/?stateCd=RI&format=waterml':
            'RI_daily.xml',
        'http://waterservices.usgs.gov/nwis/iv/?stateCd=RI&format=waterml':
            'RI_instantaneous.xml',
    }

    with test_util.mocked_requests(mocked_urls):
        sites = ulmo.usgs.core.get_sites(state_code='RI')
    assert len(sites) == 64


def test_core_get_sites_single_site():
    site_code = '08068500'
    site_data_file = 'site_%s_daily.xml' % site_code
    with test_util.mocked_requests(site_data_file):
        sites = ulmo.usgs.core.get_sites(sites=site_code)
    assert len(sites) == 1


def test_core_get_sites_multiple_sites():
    site_codes = ['08068500', '08041500']
    sites_data_file = 'sites_%s_daily.xml' % '_'.join(site_codes)
    with test_util.mocked_requests(sites_data_file):
        sites = ulmo.usgs.core.get_sites(sites=site_codes)
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
