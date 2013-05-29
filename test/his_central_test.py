import ulmo

import test_util


def test_get_services():
    wsdl = ulmo.cuahsi.his_central.core.HIS_CENTRAL_WSDL_URL.split('?')[0]
    wsdl_file = 'his_central/wsdl.xml'
    service_info_url = 'http://hiscentral.cuahsi.org/webservices/hiscentral.asmx'
    service_info_file = 'his_central/get_services.xml'

    url_files = {
        (wsdl, ('GET',)): wsdl_file,
        (service_info_url, ('POST',)): service_info_file,
    }

    with test_util.mocked_urls(url_files):
        services = ulmo.cuahsi.his_central.get_services()

    check_services = [
        {
            'abstract': ' The USGS National Water Information System (NWIS) provides access to millions of sites measuring streamflow, groundwater levels, and water quality. This web service provides methods for retrieving daily values data, such as discharge and water levels, from NWIS. For more information about NWIS, see the NWIS home page at http://waterdata.usgs.gov/nwis',
            'citation': 'USGS National Water Information System                                                                                                                                                                                                                         ',
            'email': 'valentin@sdsc.edu',
            'max_x': 179.2467,
            'max_y': 72.701,
            'min_x': -176.6633,
            'min_y': -14.3075,
            'network_name': 'NWISDV',
            'organization': 'USGS',
            'organization_website': 'http://www.usgs.gov',
            'phone': None,
            'service_description_url': 'http://hiscentral.cuahsi.org/pub_network.aspx?n=1',
            'service_id': 1,
            'service_status': None,
            'service_url': 'http://river.sdsc.edu/wateroneflow/NWIS/DailyValues.asmx?WSDL',
            'site_count': 31881,
            'title': 'NWIS Daily Values',
            'value_count': 311783702,
            'variable_count': 427
        },
    ]

    assert 90 <= len(services) <= 100

    for check_service in check_services:
        assert check_service in services
