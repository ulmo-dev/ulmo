import pyhis


def test_parse_get_sites():
    site_files = ['RI_daily.xml', 'RI_instantaneous.xml']
    sites = {}
    for site_file in site_files:
        with open(site_file, 'r') as f:
            sites.update(pyhis.waterml.v1_1.parse_sites(f))

    assert len(sites) == 63
    return sites

