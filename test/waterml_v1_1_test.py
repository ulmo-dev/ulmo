import ulmo

import test_util


def test_parse_get_sites():
    site_files = ['RI_daily.xml', 'RI_instantaneous.xml']
    sites = {}
    for site_file in site_files:
        test_site_file = test_util.get_test_file_path(site_file)
        with open(test_site_file, 'r') as f:
            sites.update(ulmo.waterml.v1_1.parse_sites(f))

    assert len(sites) == 63
    return sites


def test_parse_site_values():
    query_isodate = '2000-01-01'
    value_file = test_util.get_test_file_path('site_07335390_daily.xml')
    with open(value_file, 'rb') as content_io:
        values = ulmo.waterml.v1_1.parse_site_values(content_io, query_isodate)

    assert len(values['00062:32400']['values']) == 3404
