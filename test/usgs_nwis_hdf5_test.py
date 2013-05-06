import os
import shutil

import freezegun
import pandas
import pytest

from ulmo.usgs import nwis
import test_util


TEST_FILE_DIR = os.path.abspath('tmp/')


@pytest.fixture
def test_file_path(request):
    return os.path.join(TEST_FILE_DIR, request.function.__name__ + '.h5')


def setup_module(module):
    if os.path.exists(TEST_FILE_DIR):
        shutil.rmtree(TEST_FILE_DIR)
    os.makedirs(TEST_FILE_DIR)


def teardown_module(module):
    shutil.rmtree(TEST_FILE_DIR)


def test_update_site_list(test_file_path):
    site_files = ['usgs/nwis/RI_daily.xml', 'usgs/nwis/RI_instantaneous.xml']
    for site_file in site_files:
        test_site_file = test_util.get_test_file_path(site_file)
        nwis.hdf5.update_site_list(path=test_file_path,
                input_file=test_site_file)

    sites = nwis.hdf5.get_sites(test_file_path)
    assert len(sites) == 64

    test_sites = {
        # uses_dst == False
        '01111410': {
            'agency': 'USGS',
            'code': '01111410',
            'county': '44007',
            'huc': '01090003',
            'location': {
                'latitude': '41.9409318',
                'longitude': '-71.6481214',
                'srs': 'EPSG:4326'
            },
            'name': 'CHEPACHET RIVER WEST OF GAZZA RD AT GAZZAVILLE, RI',
            'state_code': '44',
            'network': 'NWIS',
            'site_type': 'ST',
            'timezone_info': {
                'default_tz': {
                    'abbreviation': 'EST',
                    'offset': '-05:00'
                },
                'dst_tz': {
                    'abbreviation': 'EDT',
                    'offset': '-04:00',
                },
                'uses_dst': False,
            }
        },
        # only in RI_daily
        '01116300': {
            'agency': 'USGS',
            'code': '01116300',
            'county': '44007',
            'huc': '01090004',
            'location': {
                'latitude': '41.7564892',
                'longitude': '-71.4972824',
                'srs': 'EPSG:4326'
            },
            'name': 'FURNACE HILL BROOK AT CRANSTON, RI',
            'network': 'NWIS',
            'site_type': 'ST',
            'state_code': '44',
            'timezone_info': {
                'default_tz': {'abbreviation': 'EST', 'offset': '-05:00'},
                'dst_tz': {'abbreviation': 'EDT', 'offset': '-04:00'},
                'uses_dst': True
            },
        },
        # only in RI_instantaneous
        '01115170': {
            'agency': 'USGS',
            'code': '01115170',
            'county': '44007',
            'huc': '01090004',
            'location': {
                'latitude': '41.84093269',
                'longitude': '-71.584508',
                'srs': 'EPSG:4326',
            },
            'name': 'MOSWANSICUT STREAM NR NORTH SCITUATE, RI',
            'network': 'NWIS',
            'site_type': 'ST',
            'state_code': '44',
            'timezone_info': {
                'default_tz': {'abbreviation': 'EST', 'offset': '-05:00'},
                'dst_tz': {'abbreviation': 'EDT', 'offset': '-04:00'},
                'uses_dst': True
            },
        },
    }

    for test_code, test_value in test_sites.iteritems():
        assert sites[test_code] == test_value


def test_update_site_list_with_changes(test_file_path):
    site_files = [
        ('usgs/nwis/RI_daily.xml', {
            'agency': 'USGS',
            'code': '01106000',
            'county': '44005',
            'huc': '01090002',
            'location': {'latitude': '41.5584366',
                        'longitude': '-71.12921047',
                        'srs': 'EPSG:4326'},
            'name': 'ADAMSVILLE BROOK AT ADAMSVILLE, RI',
            'network': 'NWIS',
            'site_type': 'ST',
            'state_code': '44',
            'timezone_info': {
                'default_tz': {'abbreviation': 'EST', 'offset': '-05:00'},
                'dst_tz': {'abbreviation': 'EDT', 'offset': '-04:00'},
                'uses_dst': True}}),
        ('usgs/nwis/RI_daily_update.xml', {
            'agency': 'USGS',
            'code': '01106000',
            'county': '44005',
            'huc': '01090002',
            'location': {'latitude': '41.5584366',
                        'longitude': '-71.12921047',
                        'srs': 'EPSG:4326'},
            'name': 'UPDATED NAME',
            'network': 'NWIS',
            'site_type': 'ST',
            'state_code': '44',
            'timezone_info': {
                'default_tz': {'abbreviation': 'EST', 'offset': '-05:00'},
                'dst_tz': {'abbreviation': 'EDT', 'offset': '-04:00'},
                'uses_dst': True}}),
    ]
    for test_file, test_site in site_files:
        test_site_file = test_util.get_test_file_path(test_file)
        nwis.hdf5.update_site_list(path=test_file_path,
                input_file=test_site_file)
        sites = nwis.hdf5.get_sites(path=test_file_path)
        test_code = test_site['code']
        assert sites[test_code] == test_site


def test_sites_table_remains_unique(test_file_path):
    site_files = ['usgs/nwis/RI_daily.xml', 'usgs/nwis/RI_instantaneous.xml']
    for site_file in site_files:
        test_site_file = test_util.get_test_file_path(site_file)
        nwis.hdf5.update_site_list(path=test_file_path,
            input_file=test_site_file)

    with pandas.io.pytables.get_store(test_file_path) as store:
        sites_df = store.select('sites')
    assert len(sites_df) == len(set(sites_df.index))


def test_get_site(test_file_path):
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    input_file = test_util.get_test_file_path(site_data_file)
    nwis.hdf5.update_site_list(path=test_file_path,
            input_file=input_file)

    site = nwis.hdf5.get_site(site_code, path=test_file_path)
    assert site == {
        'agency': 'USGS',
        'code': '08068500',
        'county': '48339',
        'huc': '12040102',
        'location': {
            'latitude': '30.11049517',
            'longitude': '-95.4363275',
            'srs': 'EPSG:4326'
        },
        'name': 'Spring Ck nr Spring, TX',
        'network': 'NWIS',
        'site_type': 'ST',
        'state_code': '48',
        'timezone_info': {
            'default_tz': {'abbreviation': 'CST', 'offset': '-06:00'},
            'dst_tz': {'abbreviation': 'CDT', 'offset': '-05:00'},
            'uses_dst': True
        },
    }


def test_get_sites_isnt_cached_between_calls(test_file_path):
    site_data_file = 'usgs/nwis/RI_daily.xml'
    input_file = test_util.get_test_file_path(site_data_file)

    nwis.hdf5.update_site_list(input_file=input_file, path=test_file_path)
    sites = nwis.hdf5.get_sites(path=test_file_path)
    assert len(sites) > 0

    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    sites = nwis.hdf5.get_sites(path=test_file_path)
    assert len(sites) == 0


def test_empty_update_list_doesnt_error(test_file_path):
    site_code = '98068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    input_file = test_util.get_test_file_path(site_data_file)

    sites = nwis.hdf5.get_sites(path=test_file_path)
    assert sites == {}
    nwis.hdf5.update_site_list(path=test_file_path,
        input_file=input_file)

    sites = nwis.hdf5.get_sites(path=test_file_path)
    assert sites == {}


def test_get_site_for_missing_raises_lookup(test_file_path):
    site_code = '08068500'
    site_data_file = 'usgs/nwis/site_%s_daily.xml' % site_code
    input_file = test_util.get_test_file_path(site_data_file)
    nwis.hdf5.update_site_list(path=test_file_path,
        input_file=input_file)

    with pytest.raises(LookupError):
        missing_code = '98068500'
        nwis.hdf5.get_site(missing_code, path=test_file_path)


def test_non_usgs_site(test_file_path):
    site_code = '07335390'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_instantaneous.xml' % site_code)
    nwis.hdf5.update_site_data(site_code, period='all',
            path=test_file_path, input_file=site_data_file)

    site_data = nwis.hdf5.get_site_data(site_code, path=test_file_path)
    assert len(site_data['00062:00011']['values']) > 1000


def test_site_data_is_sorted(test_file_path):
    site_code = '01117800'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily.xml' % site_code)
    nwis.hdf5.update_site_data(site_code, path=test_file_path,
            input_file=site_data_file)
    site_data = nwis.hdf5.get_site_data(site_code, path=test_file_path)

    values = site_data['00060:00003']['values']
    assert all(
        values[i]['datetime'] < values[i+1]['datetime']
        for i in xrange(len(values) - 1))


def test_update_site_data_basic_data_parsing(test_file_path):
    site_code = '01117800'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily.xml' % site_code)
    nwis.hdf5.update_site_data(site_code, path=test_file_path,
            input_file=site_data_file)
    site_data = nwis.hdf5.get_site_data(site_code, path=test_file_path)

    test_values = [
        dict(datetime="1964-01-23T00:00:00", last_checked=None, last_modified=None, qualifiers="A", value='240'),
        dict(datetime="1964-08-22T00:00:00", last_checked=None, last_modified=None, qualifiers="A", value='7.9'),
        dict(datetime="2011-12-15T00:00:00", last_checked=None, last_modified=None, qualifiers="P Eqp", value='-999999'),
        dict(datetime="2012-01-15T00:00:00", last_checked=None, last_modified=None, qualifiers="P e", value='97'),
        dict(datetime="2012-06-05T00:00:00", last_checked=None, last_modified=None, qualifiers="P", value='74'),
    ]

    site_values = site_data['00060:00003']['values']

    for test_value in test_values:
        assert test_value in site_values


def test_site_data_update_site_list_with_multiple_updates(test_file_path):
    first_timestamp = '2013-01-01T01:01:01'
    second_timestamp = '2013-02-02T02:02:02'
    site_code = '01117800'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily.xml' % site_code)
    with test_util.mocked_requests(site_data_file):
        with freezegun.freeze_time(first_timestamp):
            nwis.hdf5.update_site_data(site_code, path=test_file_path)
    site_data = nwis.hdf5.get_site_data(site_code, path=test_file_path)

    last_value = site_data['00060:00003']['values'][-1]

    assert first_timestamp == last_value['last_checked'] == last_value['last_modified']

    update_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily_update.xml' % site_code)
    with test_util.mocked_requests(update_data_file):
        with freezegun.freeze_time(second_timestamp):
            nwis.hdf5.update_site_data(site_code, path=test_file_path)
    updated_site_data = nwis.hdf5.get_site_data(site_code, path=test_file_path)

    updated_values = updated_site_data['00060:00003']['values']
    last_value = updated_values[-1]
    assert last_value['last_checked'] != first_timestamp
    assert second_timestamp == last_value['last_checked'] == last_value['last_modified']

    original_timestamp = first_timestamp
    modified_timestamp = second_timestamp

    test_values = [
        dict(datetime="1963-01-23T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='7'),
        dict(datetime="1964-01-23T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='1017'),
        dict(datetime="1964-01-24T00:00:00", last_checked=original_timestamp, last_modified=original_timestamp, qualifiers="A", value='191'),
        dict(datetime="1964-08-22T00:00:00", last_checked=original_timestamp, last_modified=original_timestamp, qualifiers="A", value='7.9'),
        dict(datetime="1969-05-26T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="A", value='1080'),
        dict(datetime="2011-12-06T00:00:00", last_checked=modified_timestamp, last_modified=modified_timestamp, qualifiers="P", value='222'),
        dict(datetime="2011-12-15T00:00:00", last_checked=original_timestamp, last_modified=original_timestamp, qualifiers="P Eqp", value='-999999'),
        dict(datetime="2012-01-15T00:00:00", last_checked=original_timestamp, last_modified=original_timestamp, qualifiers="P e", value='97'),
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
        assert updated_values.index(test_value) >= 0


def test_last_refresh_gets_updated(test_file_path):
    first_timestamp = '2013-01-01T01:01:01'
    second_timestamp = '2013-02-02T02:02:02'
    forth_timestamp = '2013-03-03T03:03:03'
    site_code = '01117800'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily.xml' % site_code)

    with test_util.mocked_requests(site_data_file):
        with freezegun.freeze_time(first_timestamp):
            nwis.hdf5.update_site_data(site_code, path=test_file_path)
        first_refresh = nwis.hdf5._get_last_refresh(site_code, test_file_path)
        assert first_refresh == first_timestamp

        with freezegun.freeze_time(second_timestamp):
            nwis.hdf5.update_site_data(site_code, path=test_file_path)
        second_refresh = nwis.hdf5._get_last_refresh(site_code, test_file_path)
        assert second_refresh == second_timestamp

        nwis.hdf5.update_site_data(site_code, path=test_file_path,
                input_file=site_data_file)
        third_refresh = nwis.hdf5._get_last_refresh(site_code, test_file_path)
        assert third_refresh == None

        with freezegun.freeze_time(forth_timestamp):
            nwis.hdf5.update_site_data(site_code, path=test_file_path)
        forth_refresh = nwis.hdf5._get_last_refresh(site_code, test_file_path)
        assert forth_refresh is not None
        assert forth_refresh == forth_timestamp


def test_update_site_data_updates_site_list(test_file_path):
    site_code = '01117800'
    site_data_file = test_util.get_test_file_path(
        'usgs/nwis/site_%s_daily.xml' % site_code)
    nwis.hdf5.update_site_data(site_code, path=test_file_path,
            input_file=site_data_file)
    site = nwis.hdf5.get_site(site_code, path=test_file_path)

    test_site = {
        'agency': 'USGS',
        'code': '01117800',
        'county': '44009',
        'huc': '01090005',
        'location': {
            'latitude': '41.5739884',
            'longitude': '-71.72062318',
            'srs': 'EPSG:4326'
        },
        'name': 'WOOD RIVER NEAR ARCADIA, RI',
        'network': 'NWIS',
        'site_type': 'ST',
        'state_code': '44',
        'timezone_info': {
            'default_tz': {'abbreviation': 'EST', 'offset': '-05:00'},
            'dst_tz': {'abbreviation': 'EDT', 'offset': '-04:00'},
            'uses_dst': True
        }
    }

    assert site == test_site
