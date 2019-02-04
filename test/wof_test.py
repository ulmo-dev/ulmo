import ulmo
import test_util


def test_core_get_sites_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_sites_file = 'cuahsi/wof/get_sites_muddyriver_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSitesXml=get_sites_file)):
        sites = ulmo.cuahsi.wof.get_sites(WSDL_URL)
    assert len(sites) == 14


def test_core_get_sites_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_sites_file = 'cuahsi/wof/get_sites_ipswich_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSites=get_sites_file)):
        sites = ulmo.cuahsi.wof.get_sites(WSDL_URL)
    assert len(sites) == 34


def test_core_get_site_info_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    site_info_file = 'cuahsi/wof/get_site_info_muddyriver_14_1_0.xml'
    with test_util.mocked_suds_client('1.0', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.cuahsi.wof.get_site_info(WSDL_URL, 'MuddyRiver:MuddyRiver_14')
    assert site_info['code'] == 'MuddyRiver_14'
    assert site_info['network'] == 'MuddyRiver'
    assert 'MR:MuddyRiver_ACID' in site_info['series']
    assert 'MR:MuddyRiver_pH' in site_info['series']
    assert 'MR:MuddyRiver_ZN' in site_info['series']
    assert len(site_info['series']) == 27
    site_info['series']['MR:MuddyRiver_ACID']['variable']['units'] == {
        'abbreviation': 'degC',
        'code': '96',
        'name': 'degree celsius',
        'type': 'Temperature',
    }


def test_core_get_site_info_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    site_info_file = 'cuahsi/wof/get_site_info_ipswich_MMB_1_1.xml'
    with test_util.mocked_suds_client('1.1', dict(GetSiteInfo=site_info_file)):
        site_info = ulmo.cuahsi.wof.get_site_info(WSDL_URL, 'ipswich:MMB')
    assert site_info['code'] == 'MMB'
    assert site_info['network'] == 'IRWA'
    assert 'IRWA:Temp' in site_info['series']
    assert 'IRWA:DO' in site_info['series']
    assert len(site_info['series']) == 4
    site_info['series']['IRWA:Temp']['variable']['units'] == {
        'abbreviation': 'degC',
        'code': '96',
        'name': 'degree celsius',
        'type': 'Temperature',
    }


def test_core_get_values_waterml_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_values_file = 'cuahsi/wof/get_values_1_0_MuddyRiver_MuddyRiver_14_MR_MuddyRiver_ACID.xml'
    with test_util.mocked_suds_client('1.0', dict(GetValues=get_values_file)):
        values = ulmo.cuahsi.wof.get_values(
            WSDL_URL, 'MuddyRiver:MuddyRiver_14', 'MR:MuddyRiver_ACID')
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


def test_core_get_values_start_and_end_parsing():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    file_template = 'cuahsi/wof/get_values_1_0_MuddyRiver_MuddyRiver_14_MR_MuddyRiver_ACID_%(start)s_%(end)s.xml'

    start_ends = [
        ('2006-07-21', '2008-04-04'),
        ('2008-01-01', None),
        (None, '2007-03-13'),
    ]

    for start, end in start_ends:
        get_values_file = file_template % {'start': start, 'end': end}
        with test_util.mocked_suds_client('1.0', dict(GetValues=get_values_file)):
            values = ulmo.cuahsi.wof.get_values(
                WSDL_URL, 'MuddyRiver:MuddyRiver_14', 'MR:MuddyRiver_ACID',
                start=start, end=end)

            assert len(values['values']) > 0
            timestamps = [value.get('datetime') for value in values['values']]
            if start:
                for timestamp in timestamps:
                    assert timestamp > start

            if end:
                for timestamp in timestamps:
                    assert timestamp < end


def test_core_get_values_waterml_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_values_file = 'cuahsi/wof/get_values_1_1_ipswich_MMB_ipswich_Temp.xml'
    with test_util.mocked_suds_client('1.1', dict(GetValues=get_values_file)):
        values = ulmo.cuahsi.wof.get_values(WSDL_URL, 'ipswich:MMB', 'ipswich:Temp')
    assert len(values['values']) == 198
    assert values['values'][0] == {
        'censor_code': 'nc',
        'date_time_utc': '1997-08-24T06:00:00',
        'datetime': '1997-08-24T00:00:00',
        'method_code': '21',
        'quality_control_level_code': '1',
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
    assert values['methods'] == {'21': {'code': '21', 'description': '6"" Glass Thermometer, Centigrade Scale', 'id': '21'}}
    assert values['sources'] == {'1': {'id': '1', 'code': '1', 'organization': 'Ipswich River Watershed Association', 'description': 'The Ipswich River Watershed Association (IRWA) is the voice of the Ipswich River.� IRWA works to protect nature and make sure that there is enough clean water for people, fish and wildlife, today and for our children and theirs.', 'topic_category': 'inlandWaters', 'title': 'Ipswich River RiverWatch Program', 'abstract': 'The RiverWatch program, in operation since 1997, enlists a group of volunteers to collect water quality data on the Ipswich River and its tributaries. The purpose of the program is to establish baseline data in order to identify and address impairments to water quality and quantity, as well as to promote awareness and stewardship of the river. Volunteers monitor according to a state-approved monitoring plan that ensures that the data collected is of good quality. The goals of the program are to document River conditions in order to identify water quality problems (including adequate river flow) and to use this data to develop solutions to observed problems. A Quality Assurance Project Plan (QAPP) was finalized in 1999 and most recently updated in 2013. ', 'profile_version': 'Unknown', 'metadata_link': 'http://ipswich-river.org/resources/monitoring-data/', 'contact_name': "Ryan O'Donnell", 'type_of_contact': 'main', 'email': 'rodonnell@ipswichriver.org', 'phone': '978-412-8200', 'address': 'P.O. Box 576,143 County Rd.\n,Ipswich, MA 01938-2557', 'link': 'http://www.ipswichriver.org', 'citation': 'RiverWatch Water Quality Volunteer Monitoring Program Annual Results Reports. http://ipswichriver.org/resources/monitoring-data/'}}


def test_core_get_variable_info_waterml_single_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_variable_info_file = 'cuahsi/wof/get_variable_info_1_0_MR_MuddyRiver_ACID.xml'
    with test_util.mocked_suds_client('1.0', dict(GetVariableInfo=get_variable_info_file)):
        variable_info = ulmo.cuahsi.wof.get_variable_info(WSDL_URL, 'MR:MuddyRiver_ACID')
    assert variable_info == {
        'code': 'MuddyRiver_ACID',
        'data_type': 'Sporadic',
        'general_category': 'Water Quality',
        'id': '16',
        'name': 'Acid neutralizing capacity',
        'no_data_value': '-9999',
        'sample_medium': 'Surface Water',
        'time': {
            'is_regular': False,
        },
        'units': {
            'abbreviation': 'mg/L',
            'code': '199',
            'name': 'milligrams per liter',
        },
        'value_type': 'Sample',
        'vocabulary': 'MR'
    }


def test_core_get_variable_info_waterml_all_1_0():
    WSDL_URL = 'http://hydroportal.cuahsi.org/muddyriver/cuahsi_1_0.asmx?WSDL'
    get_variable_info_file = 'cuahsi/wof/get_variable_info_1_0_MR_all.xml'
    with test_util.mocked_suds_client('1.0', dict(GetVariableInfo=get_variable_info_file)):
        variable_info = ulmo.cuahsi.wof.get_variable_info(WSDL_URL)

    check_includes = [
        'MR:MuddyRiver_ACID',
        'MR:MuddyRiver_FC',
        'MR:MuddyRiver_FCOLOR',
        'MR:MuddyRiver_pH',
    ]

    for check in check_includes:
        assert check in variable_info

    assert variable_info['MR:MuddyRiver_ACID'] == {
        'code': 'MuddyRiver_ACID',
        'data_type': 'Sporadic',
        'general_category': 'Water Quality',
        'id': '16',
        'name': 'Acid neutralizing capacity',
        'no_data_value': '-9999',
        'sample_medium': 'Surface Water',
        'time': {
            'is_regular': False,
        },
        'units': {
            'abbreviation': 'mg/L',
            'code': '199',
            'name': 'milligrams per liter',
        },
        'value_type': 'Sample',
        'vocabulary': 'MR'
    }


def test_core_get_variable_info_waterml_single_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_variable_info_file = 'cuahsi/wof/get_variable_info_1_1_ipswich_Temp.xml'
    with test_util.mocked_suds_client('1.1', dict(GetVariableInfo=get_variable_info_file)):
        variable_info = ulmo.cuahsi.wof.get_variable_info(WSDL_URL, 'ipswich:Temp')

    assert variable_info == {'value_type': 'Sample', 'data_type': 'Sporadic', 'general_category': 'Water Quality', 'sample_medium': 'Surface Water', 'no_data_value': '-9999', 'speciation': 'Not Applicable', 'code': 'Temp', 'id': '3', 'name': 'Temperature', 'vocabulary': 'IRWA', 'time': {'is_regular': True, 'interval': '0', 'units': {'abbreviation': 'month', 'code': '106', 'name': 'month', 'type': 'Time'}}, 'units': {'abbreviation': 'degC', 'code': '96', 'name': 'degree celsius', 'type': 'Temperature'}}


def test_core_get_variable_info_waterml_all_1_1():
    WSDL_URL = 'http://hydroportal.cuahsi.org/ipswich/cuahsi_1_1.asmx?WSDL'
    get_variable_info_file = 'cuahsi/wof/get_variable_info_1_1_ipswich_all.xml'
    with test_util.mocked_suds_client('1.1', dict(GetVariableInfo=get_variable_info_file)):
        variable_info = ulmo.cuahsi.wof.get_variable_info(WSDL_URL)

    check_includes = [
        'IRWA:DO',
        'IRWA:PercDO',
        'IRWA:Temp',
    ]
    for check in check_includes:
        assert check in variable_info

    assert variable_info['IRWA:Temp'] == {'value_type': 'Sample', 'data_type': 'Sporadic', 'general_category': 'Water Quality', 'sample_medium': 'Surface Water', 'no_data_value': '-9999', 'speciation': 'Not Applicable', 'code': 'Temp', 'id': '3', 'name': 'Temperature', 'vocabulary': 'IRWA', 'time': {'is_regular': True, 'interval': '0', 'units': {'abbreviation': 'month', 'code': '106', 'name': 'month', 'type': 'Time'}}, 'units': {'abbreviation': 'degC', 'code': '96', 'name': 'degree celsius', 'type': 'Temperature'}}
