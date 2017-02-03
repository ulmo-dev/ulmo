import ulmo
import pandas as pd

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

    #with test_util.mocked_urls(url_files):
    services = ulmo.cuahsi.his_central.get_services()

    check_services = [
        {'abstract': 'The USGS National Water Information System (NWIS) provides access to millions of sites measuring streamflow, groundwater levels, and water quality. This web service provides methods for retrieving daily values data, such as discharge and water levels, from NWIS. For more information about NWIS data services, see http://waterservices.usgs.gov/',
         'citation': 'U.S. Geological Survey, [YEAR], National Water Information System data, accessed [DATE ACCESSED] via HIS Central (http://hiscentral.cuahsi.org).                                                                                                                                                                                                                    ',
         'email': 'help@cuahsi.org',
         'max_x': -64.69125,
         'max_y': 71.29403,
         'min_x': -176.6633,
         'min_y': -14.3075,
         'network_name': 'NWISDV',
         'organization': 'U.S. Geological Survey (USGS)',
         'organization_website': 'http://www.usgs.gov',
         'phone': '339-221-5400',
         'service_description_url': 'http://hiscentral.cuahsi.org/pub_network.aspx?n=1',
         'service_id': 1,
         'service_status': None,
         'service_url': 'http://hydroportal.cuahsi.org/nwisdv/cuahsi_1_1.asmx?WSDL',
         'site_count': 34841,
         'title': 'NWIS Daily Values',
         'value_count': 387092632,
         'variable_count': 484},
    ]

    assert 89 <= len(services) <= 110

    services = pd.DataFrame(services)
    for check_service in check_services:
        assert check_service['network_name'] in services['network_name'].tolist()
        assert check_service['organization'] in services['organization'].tolist()
        assert check_service['title'] in services['title'].tolist()
