import isodate

from lxml import etree


def parse_site_values(content_io, namespace, query_isodate):
    """
    """
    data_dict = {}
    for (event, ele) in etree.iterparse(content_io):
        if ele.tag == namespace + "timeSeries":
            values_element = ele.find(namespace + 'values')
            values = _parse_values(values_element, namespace)
            var_element = ele.find(namespace + 'variable')
            variable = _parse_variable(var_element, namespace)
            code = variable['code']
            if 'statistic' in variable:
                code += ":" + variable['statistic']['code']
            data_dict[code] = {
                'last_refresh': query_isodate,
                'values': values,
                'variable': variable,
            }
    return data_dict


def parse_sites(content_io, namespace, site_info_name):
    """parses sites out of a waterml file; content_io should be a file-like object"""
    site_elements = dict(set([(ele.find(namespace + "siteCode").text, ele)
                    for (event, ele) in etree.iterparse(content_io)
                    if ele.tag == namespace + site_info_name]))
    sites = dict([(key, _parse_site_info(source_info, namespace))
                    for key, source_info in site_elements.iteritems()])
    return sites


def _parse_geog_location(geog_location, namespace):
    """returns a dict representation of a geogLocation etree element"""
    return {
        'srs': geog_location.attrib.get('srs'),
        'latitude': geog_location.find(namespace + 'latitude').text,
        'longitude': geog_location.find(namespace + 'longitude').text,
    }


def _parse_site_info(site_info, namespace):
    """returns a dict representation of a site given an etree sourceInfo object
    representing a site
    """
    geog_location = site_info.find(namespace.join(["", "geoLocation/", "geogLocation"]))
    site_code = site_info.find(namespace + "siteCode")
    timezone_info = site_info.find(namespace + "timeZoneInfo")

    return_dict = {
        'agency': site_code.attrib.get('agencyCode'),
        'code': site_code.text,
        'location': _parse_geog_location(geog_location, namespace),
        'name': site_info.find(namespace + "siteName").text,
        'network': site_code.attrib.get('network'),
    }

    if not timezone_info is None:
        return_dict['timezone_info'] = _parse_timezone_info(timezone_info, namespace)

    site_properties = {
        'county': 'countyCd',
        'huc': 'hucCd',
        'site_type': 'siteTypeCd',
        'state_code': 'stateCd',
    }

    for k, v in site_properties.iteritems():
        find_element = site_info.find(namespace + "siteProperty[@name='%s']" % v)
        if find_element:
            return_dict[k] = find_element.text

    return return_dict


def _parse_timezone_element(timezone_element):
    """returns a dict representation of a timezone etree element (either
    defaultTimeZone or daylightSavingsTimeZone)
    """
    return {
        'abbreviation': timezone_element.attrib.get('zoneAbbreviation'),
        'offset': timezone_element.attrib.get('zoneOffset'),
    }


def _parse_timezone_info(timezone_info, namespace):
    """returns a dict representation of a timeZoneInfo etree element"""
    return_dict = {}

    if timezone_info.attrib.get('siteUsesDaylightSavingsTime', "false") == "true":
        return_dict['uses_dst'] = True
        return_dict['dst_tz'] = _parse_timezone_element(timezone_info.find(namespace + 'daylightSavingsTimeZone'))

    return_dict['default_tz'] = _parse_timezone_element(timezone_info.find(namespace + 'defaultTimeZone'))

    return return_dict


def _parse_values(values_element, namespace):
    """returns a list of dicts that represent the values for a given etree
    values element
    """

    return [{'datetime': _parse_datetime(value.attrib['dateTime']),
             'value': value.text,
             'qualifiers': value.attrib['qualifiers']}
            for value in values_element.findall(namespace + 'value')]


def _parse_variable(variable_element, namespace):
    """returns a dict that represents a variable for a given etree variable element"""
    variable_code = variable_element.find(namespace + 'variableCode')
    statistic = variable_element.find(namespace + 'options/' + namespace + "option[@name='Statistic']")
    return_dict = {
        'code': variable_code.text,
        'description': variable_element.find(namespace + 'variableDescription').text,
        'id': variable_code.attrib.get('variableID'),
        'network': variable_code.attrib.get('network'),
        'name': variable_element.find(namespace + 'variableName').text,
        'unit': variable_element.find(namespace + 'unit/' + namespace + 'unitCode').text,
        'no_data_value': variable_element.find(namespace + 'noDataValue').text,
        'vocabulary': variable_code.attrib.get('vocabulary'),
    }

    if statistic is not None:
        return_dict['statistic'] = {
            'code': statistic.attrib.get('optionCode'),
            'name': statistic.text,
        }

    return return_dict


def _parse_datetime(datetime_str):
    """returns an iso 8601 datetime string; USGS returns fractions of a second
    which are usually all 0s. ISO 8601 does not limit the number of decimal
    places but we have to cut them off at some point
    """
    #XXX: this could be sped up if need be
    #XXX: also, we need to document that we are throwing away fractions of
    #     seconds
    return isodate.datetime_isoformat(isodate.parse_datetime(datetime_str))



