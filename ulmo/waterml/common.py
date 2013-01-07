import re

import isodate

from lxml import etree


# pre-compiled regexes for underscore conversion
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


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


def parse_sites(content_io, namespace):
    """parses information contained in site elements (including seriesCatalogs)
    out of a waterml file; content_io should be a file-like object
    """
    content_io.seek(0)
    site_elements = [
        ele for (event, ele) in etree.iterparse(content_io)
        if ele.tag == namespace + 'site']
    site_dicts = [
        _parse_site(site_element, namespace)
        for site_element in site_elements]
    sites = dict(
        [(site_dict['code'], site_dict)
         for site_dict in site_dicts])
    return sites


def _convert_to_underscore(s):
    """converts camelCase to underscore, originally from
    http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    first_sub = first_cap_re.sub(r'\1_\2', s)
    return all_cap_re.sub(r'\1_\2', first_sub).lower()


def _element_dict(element, exclude_children=None):
    """converts an element to a dict representation with CamelCase tag names and
    attributes converted to underscores; this is a generic converter for cases
    where special parsing isn't necessary.  In most cases you will want to
    update with this dict.

    Note: does not handle sibling elements
    """
    if element is None:
        return {}

    if exclude_children is None:
        exclude_children = []

    element_dict = {}
    element_name = _convert_to_underscore(element.tag.split('}')[-1])

    if len(element) == 0 and not element.text is None:
        element_dict[element_name] = element.text

    element_dict.update({
        _element_dict_attribute_name(key, element_name): value
        for key, value in element.attrib.iteritems()
    })

    for child in element.iterchildren():
        if not child.tag.split('}')[-1] in exclude_children:
            element_dict.update(_element_dict(child))

    return element_dict


def _element_dict_attribute_name(attribute_name, element_name):
    attribute_only = _convert_to_underscore(attribute_name.split('}')[-1])
    if attribute_only.startswith(element_name):
        return attribute_only
    else:
        return element_name + '_' + attribute_only


def _parse_datetime(datetime_str):
    """returns an iso 8601 datetime string; USGS returns fractions of a second
    which are usually all 0s. ISO 8601 does not limit the number of decimal
    places but we have to cut them off at some point
    """
    #XXX: this could be sped up if need be
    #XXX: also, we need to document that we are throwing away fractions of
    #     seconds
    return isodate.datetime_isoformat(isodate.parse_datetime(datetime_str))


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


def _parse_series(series, namespace):
    include_elements = [
        'method',
        'Method',
        'source',
        'Source',
        'QualityControlLevel',
        'qualityControlLevel',
        'variableTimeInterval',
        'valueCount',
    ]
    exclude_items = [
        'variable_time_interval_type',
    ]
    series_dict = {}

    variable_element = series.find(namespace + 'variable')
    series_dict['variable'] = _parse_variable(variable_element, namespace)

    for include_element in include_elements:
        element = series.find(namespace + include_element)
        if not element is None:
            series_dict.update(_element_dict(element))

    for exclude_item in exclude_items:
        try:
            del series_dict[exclude_item]
        except KeyError:
            pass

    return series_dict


def _parse_site(site, namespace):
    """returns a dict representation of a site given an etree object
    representing a site element
    """
    site_dict = _parse_site_info(site.find(namespace + 'siteInfo'), namespace)
    series_elements = site.iter(namespace + 'series')
    site_dict['series'] = [
        _parse_series(series_element, namespace)
        for series_element in series_elements
    ]

    return site_dict


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


def _parse_unit(unit_element, namespace):
    """returns a list of dicts that represent the values for a given etree
    values element
    """
    unit_dict = _element_dict(unit_element)
    tag_name = unit_element.tag.split('}')[-1]
    return_dict = {}

    if '1.0' in namespace:
        return_dict['name'] = unit_element.text

    keys = [
        'abbreviation',
        'code',
        'name',
        'type',
    ]
    for key in keys:
        dict_key = tag_name + '_' + key
        if dict_key in unit_dict:
            return_dict[key] = unit_dict[dict_key]

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
    return_dict = _element_dict(variable_element,
        exclude_children=['unit', 'units', 'variableCode', 'variableName',
            'variableDescription', 'options'])
    variable_code = variable_element.find(namespace + 'variableCode')
    return_dict.update({
        'code': variable_code.text,
        'id': variable_code.attrib.get('variableID'),
        'network': variable_code.attrib.get('network'),
        'name': variable_element.find(namespace + 'variableName').text,
        'vocabulary': variable_code.attrib.get('vocabulary'),
    })
    variable_description = variable_element.find(
            namespace + 'variableDescription')
    if not variable_description is None:
        return_dict['description'] = variable_description.text

    unit_element = variable_element.find(namespace + 'unit')
    if unit_element is None:
        unit_element = variable_element.find(namespace + 'units')

    if not unit_element is None:
        return_dict['unit'] = _parse_unit(unit_element, namespace)

    statistic = variable_element.find(namespace + 'options/' + namespace + "option[@name='Statistic']")
    if statistic is not None:
        return_dict['statistic'] = {
            'code': statistic.attrib.get('optionCode'),
            'name': statistic.text,
        }

    return return_dict
