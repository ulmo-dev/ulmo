import ulmo

import test_util


def test_core_get_sites_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_sites_file = 'get_sites_muddyriver_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSitesXml=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 14


def test_core_get_sites_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_sites_file = 'get_sites_ipswich_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSites=get_sites_file)):
        sites = ulmo.wof.core.get_sites(WSDL_URL)
    assert len(sites) == 34


def test_core_get_site_info_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    site_info_file = 'get_site_info_muddyriver_14_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.wof.core.get_site_info(WSDL_URL, 'MuddyRiver:MuddyRiver_14')
    assert site_info['code'] == 'MuddyRiver_14'
    assert site_info['network'] == 'MuddyRiver'
    assert 'MR:MuddyRiver_ACID' in site_info['series']
    assert 'MR:MuddyRiver_pH' in site_info['series']
    assert 'MR:MuddyRiver_ZN' in site_info['series']
    assert len(site_info['series']) == 27
    site_info['series']['MR:MuddyRiver_ACID']['variable']['unit'] == {
        'abbreviation': 'degC',
        'code': '96',
        'name': 'degree celsius',
        'type': 'Temperature',
    }


def test_core_get_site_info_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    site_info_file = 'get_site_info_ipswich_MMB_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.wof.core.get_site_info(WSDL_URL, 'ipswich:MMB')
    assert site_info['code'] == 'MMB'
    assert site_info['network'] == 'ipswich'
    assert 'ipswich:Temp' in site_info['series']
    assert 'ipswich:DO' in site_info['series']
    assert len(site_info['series']) == 3
    site_info['series']['ipswich:Temp']['variable']['unit'] == {
        'abbreviation': 'degC',
        'code': '96',
        'name': 'degree celsius',
        'type': 'Temperature',
    }


def test_core_get_values_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_values_file = 'get_values_1_0_MuddyRiver_MuddyRiver_14_MR_MuddyRiver_ACID.xml'
    with test_util.mocked_suds_client('1.0', dict(GetValues=get_values_file)):
        values = ulmo.wof.core.get_values(WSDL_URL,
                'MuddyRiver:MuddyRiver_14', 'MR:MuddyRiver_ACID')
    assert len(values['values']) == 28
    assert values['methods'] == {
        '0': {
            'id': '0',
            'description': 'No method specified',
        }
    }
    assert values['sources'] == {
        '1': {
            'address': '400 Snell Engineering Center\n,Boston, MA 02115',
            'contact_name': 'Ferdi L. Hellweger',
            'description': 'Muddy River Water Quality Monitoring',
            'email': 'ferdi@coe.neu.edu',
            'id': '1',
            'link': 'http://www.muddyrivermmoc.org/index.html',
            'organization': 'Northeastern University',
            'phone': '(617) 373-3992',
            'type_of_contact': 'main',
        }
    }


def test_core_get_values_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_values_file = 'get_values_1_1_ipswich_MMB_ipswich_Temp.xml'
    with test_util.mocked_suds_client('1.1', dict(GetValues=get_values_file)):
        values = ulmo.wof.core.get_values(WSDL_URL, 'ipswich:MMB', 'ipswich:Temp')
    assert len(values['values']) == 112
    assert values['values'][0] == {
        'censor_code': 'nc',
        'date_time_utc': '1997-08-24T15:35:00.383',
        'datetime': '1997-08-24T09:35:00',
        'method_code': '2',
        'quality_control_level_code': '3',
        'source_code': '1',
        'time_offset': '-06:00',
        'value': '19',
    }
    assert values['censor_codes'] == {
        'nc': {
            'censor_code': 'nc',
            'description': 'not censored',
        }
    }
    assert values['methods'] == {
        '2': {
                'code': '2',
                'description': '6" Glass Thermometer, Centigrade Scale',
                'id': '2',
            }
        }
    assert values['sources'] == {
        '1': {
            'abstract': 'The Ipswich River Watershed Associations (IRWA) RiverWatch water quality monitoring program, in operation since 1997, enlists volunteers to collect data on the health of the Ipswich River and its tributaries. Volunteers monitor according to a state-approved monitoring plan that ensures that the data they collect is of good quality. The goals of the program are to document River conditions in order to identify water quality problems (including adequate river flow) and to use this data to develop solutions to observed problems.',
            'address': 'P.O. Box 576, 143 County Rd.\n,Ipswich, MA 01938-2557',
            'citation': 'RiverWatch Water Quality Volunteer Monitoring Program Annual Results Reports. http://ipswichriver.org/resources/monitoring-data/',
            'code': '1',
            'contact_name': 'Ryan ODonnell',
            'description': 'The Ipswich River Watershed Association (IRWA) is the voice of the Ipswich River. IRWA works to protect nature and make sure that there is enough clean water for people, fish and wildlife, today and for our children and theirs.',
            'email': 'rodonnell@ipswichriver.org',
            'id': '1',
            'link': 'http://www.ipswichriver.org',
            'metadata_link': 'http://ipswich-river.org/resources/monitoring-data/',
            'organization': 'Ipswich River Watershed Association',
            'phone': '978-412-8200',
            'profile_version': 'Unknown',
            'title': 'Ipswich River RiverWatch Program',
            'topic_category': 'inlandWaters',
            'type_of_contact': 'main',
        }
    }
