import isodate
from lxml.etree import iterparse


NS = "{http://www.cuahsi.org/waterML/1.1/}"


def _parse_datetime(datetime_str):
    """returns an iso 8601 datetime string; USGS returns fractions of a second
    which are usually all 0s. ISO 8601 does not limit the number of decimal
    places but we have to cut them off at some point
    """
    #XXX: this could be sped up if need be
    #XXX: also, we need to document that we are throwing away fractions of
    #     seconds
    return isodate.datetime_isoformat(isodate.parse_datetime(datetime_str))


def _parse_geog_location(geog_location):
    """returns a dict representation of a geogLocation etree element"""
    return {
        'srs': geog_location.attrib.get('srs'),
        'latitude': geog_location.find(NS + 'latitude').text,
        'longitude': geog_location.find(NS + 'longitude').text,
    }


def _parse_site_info(site_info):
    """returns a dict representation of a site given an etree sourceInfo object
    representing a site
    """
    geog_location = site_info.find(NS.join(["", "geoLocation/", "geogLocation"]))
    site_code = site_info.find(NS + "siteCode")
    timezone_info = site_info.find(NS + "timeZoneInfo")

    return {
        'agency': site_code.attrib.get('agencyCode'),
        'code': site_code.text,
        'county': site_info.find(NS + "siteProperty[@name='countyCd']").text,
        'huc': site_info.find(NS + "siteProperty[@name='hucCd']").text,
        'location': _parse_geog_location(geog_location),
        'name': site_info.find(NS + "siteName").text,
        'network': site_code.attrib.get('network'),
        'site_type': site_info.find(NS + "siteProperty[@name='siteTypeCd']").text,
        'state_code': site_info.find(NS + "siteProperty[@name='stateCd']").text,
        'timezone_info': _parse_timezone_info(timezone_info),
    }


def parse_sites(content_io):
    """parses sites out of a waterml file; content_io should be a file-like object"""
    site_elements = dict(set([(ele.find(NS + "siteCode").text, ele)
                    for (event, ele) in iterparse(content_io)
                    if ele.tag == NS + "sourceInfo"]))
    sites = dict([(key, _parse_site_info(source_info))
                    for key, source_info in site_elements.iteritems()])
    return sites


def _parse_timezone_info(timezone_info):
    """returns a dict representation of a timeZoneInfo etree element"""
    return_dict = {}

    if timezone_info.attrib.get('siteUsesDaylightSavingsTime', "false") == "true":
        return_dict['uses_dst'] = True
        return_dict['dst_tz'] = _parse_timezone_element(timezone_info.find(NS + 'daylightSavingsTimeZone'))

    return_dict['default_tz'] = _parse_timezone_element(timezone_info.find(NS + 'defaultTimeZone'))

    return return_dict


def _parse_timezone_element(timezone_element):
    """returns a dict representation of a timezone etree element (either
    defaultTimeZone or daylightSavingsTimeZone)
    """
    return {
        'abbreviation': timezone_element.attrib.get('zoneAbbreviation'),
        'offset': timezone_element.attrib.get('zoneOffset'),
    }


def _parse_values(values_element):
    """returns a list of dicts that represent the values for a given etree
    values element
    """

    return [{'datetime': _parse_datetime(value.attrib['dateTime']),
             'value': value.text,
             'qualifiers': value.attrib['qualifiers']}
            for value in values_element.findall(NS + 'value')]


def _parse_variable(variable_element):
    """returns a dict that represents a variable for a given etree variable element"""
    variable_code = variable_element.find(NS + 'variableCode')
    statistic = variable_element.find(NS + 'options/' + NS + "option[@name='Statistic']")
    return_dict = {
        'code': variable_code.text,
        'description': variable_element.find(NS + 'variableDescription').text,
        'id': variable_code.attrib.get('variableID'),
        'network': variable_code.attrib.get('network'),
        'name': variable_element.find(NS + 'variableName').text,
        'unit': variable_element.find(NS + 'unit/' + NS + 'unitCode').text,
        'no_data_value': variable_element.find(NS + 'noDataValue').text,
        'vocabulary': variable_code.attrib.get('vocabulary'),
    }

    if statistic is not None:
        return_dict['statistic'] = {
            'code': statistic.attrib.get('optionCode'),
            'name': statistic.text,
        }

    return return_dict
