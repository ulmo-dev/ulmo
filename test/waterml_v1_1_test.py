import ulmo

import test_util


def test_parse_site_infos():
    site_files = ['usgs/nwis/RI_daily.xml', 'usgs/nwis/RI_instantaneous.xml']
    site_infos = {}
    for site_file in site_files:
        test_site_file = test_util.get_test_file_path(site_file)
        with open(test_site_file, 'rb') as f:
            site_infos.update(ulmo.waterml.v1_1.parse_site_infos(f))

    assert len(site_infos) == 64

    test_sites = {
        '01111410': {
            'agency': 'USGS',
            'code': '01111410',
            'location': {
                'latitude': '41.9409318',
                'longitude': '-71.6481214',
                'srs': 'EPSG:4326',
            },
            'name': 'CHEPACHET RIVER WEST OF GAZZA RD AT GAZZAVILLE, RI',
            'network': 'NWIS',
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
            },
            'site_property': {
                'site_type_cd': 'ST',
                'huc_cd': '01090003',
                'state_cd': '44',
                'county_cd': '44007',
            }
        }
    }

    for test_code, test_dict in test_sites.items():
        assert site_infos[test_code] == test_dict
    return site_infos


def test_parse_site_values():
    query_isodate = '2000-01-01'
    value_file = test_util.get_test_file_path(
            'usgs/nwis/site_07335390_instantaneous.xml')
    with open(value_file, 'rb') as content_io:
        values = ulmo.waterml.v1_1.parse_site_values(content_io, query_isodate)

    assert len(values['00062:00011']['values']) > 1000
