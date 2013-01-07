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


def parse_site_infos(content_io, namespace, site_info_names):
    """parses information contained in site info elements out of a waterml file;
    content_io should be a file-like object
    """
    site_infos = {}
    for site_info_name in site_info_names:
        content_io.seek(0)
        site_info_elements = [
            element
            for (event, element) in etree.iterparse(content_io)
            if element.tag == namespace + site_info_name
        ]
        site_info_dicts = [
            _parse_site_info(site_info_element, namespace)
            for site_info_element in site_info_elements
        ]
        site_infos.update(dict([(d['code'], d) for d in site_info_dicts]))
    return site_infos


def _convert_to_underscore(s):
    """converts camelCase to underscore, originally from
    http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    first_sub = first_cap_re.sub(r'\1_\2', s)
    return all_cap_re.sub(r'\1_\2', first_sub).lower()


def _parse_geog_location(geog_location, namespace):
    """returns a dict representation of a geogLocation etree element"""
    return_dict = {
        'latitude': geog_location.find(namespace + 'latitude').text,
        'longitude': geog_location.find(namespace + 'longitude').text,
    }

    srs = geog_location.attrib.get('srs')
    if not srs is None:
        return_dict['srs'] = srs

    return return_dict


def _parse_site_info(site_info, namespace):
    """returns a dict representation of a site given an etree object
    representing a siteInfo element
    """
    site_code = site_info.find(namespace + "siteCode")

    return_dict = {
        'code': site_code.text,
        'name': site_info.find(namespace + "siteName").text,
        'network': site_code.attrib.get('network'),
    }

    agency = site_code.attrib.get('agencyCode')
    if agency:
        return_dict['agency'] = agency

    geog_location = site_info.find(
        namespace.join(["", "geoLocation/", "geogLocation"]))
    if not geog_location is None:
        return_dict['location'] = _parse_geog_location(geog_location, namespace)

    timezone_info = site_info.find(namespace + "timeZoneInfo")
    if not timezone_info is None:
        return_dict['timezone_info'] = _parse_timezone_info(timezone_info, namespace)

    elevation_m = site_info.find(namespace + 'elevation_m')
    if not elevation_m is None:
        return_dict['elevation_m'] = elevation_m.text

    # WaterML 1.0 notes
    notes = {
        _convert_to_underscore(note.attrib['title'].replace(' ', '')): note.text
        for note in site_info.findall(namespace + 'note')
    }
    if notes:
        return_dict['notes'] = notes

    # WaterML 1.1 siteProperties
    site_properties = {
        _convert_to_underscore(site_property.attrib['name'].replace(' ', '')): site_property.text
        for site_property in site_info.findall(namespace + 'site_property')
    }
    if site_properties:
        return_dict['site_properties'] = site_properties

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
