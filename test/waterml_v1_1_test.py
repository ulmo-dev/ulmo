import ulmo

import test_util


def test_parse_site_infos():
    site_files = ['usgs/nwis/RI_daily.xml', 'usgs/nwis/RI_instantaneous.xml']
    site_infos = {}
    for site_file in site_files:
        test_site_file = test_util.get_test_file_path(site_file)
        with open(test_site_file, 'r') as f:
            site_infos.update(ulmo.waterml.v1_1.parse_site_infos(f))

    assert len(site_infos) == 64
    return site_infos


def test_parse_site_values():
    query_isodate = '2000-01-01'
    value_file = test_util.get_test_file_path('usgs/nwis/site_07335390_daily.xml')
    with open(value_file, 'rb') as content_io:
        values = ulmo.waterml.v1_1.parse_site_values(content_io, query_isodate)

    assert len(values['00062:32400']['values']) == 3404
