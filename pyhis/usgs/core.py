import cStringIO as StringIO
import datetime
import logging

import isodate
from lxml.etree import iterparse
import requests


INSTANTANEOUS_URL = "http://waterservices.usgs.gov/nwis/iv/"
DAILY_URL = "http://waterservices.usgs.gov/nwis/dv/"
NS = "{http://www.cuahsi.org/waterML/1.1/}"

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


def get_sites(sites=None, state_code=None, site_type=None, service=None):
    """Fetches sites from USGS services. See the USGS waterservices documentation for options

    :param sites: The site to use or list of sites to use; lists will be joined by a ','
    :param state_code: Two-letter state code used in stateCd parameter
    :param site_type: Type of site used in siteType parameter
    :param service: The service to use, either "individual" or "daily" if None (default), then both services are used

    :returns: a dict containing site code and site names
    :rtype: dict
    """
    url_params = {'format': 'waterml'}

    if state_code:
        url_params['stateCd'] = state_code

    if sites:
        if isinstance(sites, basestring):
            url_params['sites'] = sites
        else:
            url_params['sites'] = ','.join(sites)

    if site_type:
        url_params['siteType'] = site_type

    if not service:
        return_sites = get_sites(sites=sites, state_code=state_code, site_type=site_type, service="daily")
        return_sites.update(get_sites(sites=sites, state_code=state_code, site_type=site_type, service="instantaneous"))

    else:
        url = _get_service_url(service)
        log.info('making request for sites: %s' % url)
        req = requests.get(url, params=url_params)
        log.info("processing data from request: %s" % req.request.full_url)
        content_io = StringIO.StringIO(str(req.content))

        return_sites = _parse_sites(content_io)
    return return_sites


def get_site_data(site_code, service=None, parameter_code=None,
                  date_range=None, modified_since=None):
    """queries service for data and returns a data dict"""
    url_params = {'format': 'waterml',
                  'site': site_code}
    if parameter_code:
        url_params['parameterCd'] = parameter_code
    if modified_since:
        url_params['modifiedSince'] = isodate.duration_isoformat(modified_since)

    if service in ('daily', 'instantaneous'):
        values = _get_site_values(service, date_range, url_params)
    elif not service:
        values = _get_site_values('daily', date_range, url_params)
        values.update(
            _get_site_values('instantaneous', date_range, url_params))
    else:
        raise ValueError("service must either be 'daily', 'instantaneous' or none")

    return values


def _date_range_url_params(date_range, service):
    """returns a dict of url parameters that should be used for the
    date_range, depending on what type of object date_range is. If
    date_range is a single datetime, returns startDT. If date_range is
    a pair of datetimes then it returns a startDT and endDT. If
    date_range is a timedelta then it returns a period. If date_range
    is the string 'all', then it returns that will get all the
    available data from the service, depending on the service
    (instantaneous is only the last 120 days, daily values queries
    data starting in 1851).
    """
    if date_range is None:
        return {}
    if type(date_range) is datetime.datetime:
        return dict(startDT=isodate.datetime_isoformat(date_range))
    if type(date_range) is list or type(date_range) is tuple:
        return dict(startDT=isodate.datetime_isoformat(date_range[0]),
                    endDT=isodate.datetime_isoformat(date_range[1]))
    if type(date_range) is datetime.timedelta:
        return dict(period=isodate.duration_isoformat(date_range))
        #return dict(startDT=isodate.datetime_isoformat(dt.now() - date_range))
    if date_range == 'all':
        if service in ('iv', 'instantaneous'):
            return dict(startDT=isodate.date_isoformat(datetime.datetime(2007, 10, 1)))
        if service in ('dv', 'daily'):
            return dict(startDT=isodate.date_isoformat(datetime.datetime(1851, 1, 1)))

    raise(TypeError,
          "date_range must be either a datetime, a 2-tuple of "
          "datetimes, a timedelta object, or 'all'")


def _get_service_url(service):
    if service in ('daily', 'dv'):
        return DAILY_URL
    elif service in ('instantaneous', 'iv'):
        return INSTANTANEOUS_URL
    else:
        raise "service must be either 'daily' ('dv') or 'instantaneous' ('iv')"


def _get_site_values(service, date_range, url_params):
    """downloads and parses values for a site

    returns a values dict containing variable and data values
    """
    url_params.update(_date_range_url_params(date_range, service))
    service_url = _get_service_url(service)

    query_isodate = isodate.datetime_isoformat(datetime.datetime.now())
    try:
        req = requests.get(service_url, params=url_params)
    except requests.exceptions.ConnectionError:
        log.info("There was a connection error with query:\n\t%s\n\t%s" % (service_url, url_params))
        return {}
    log.info("processing data from request: %s" % req.request.full_url)

    if req.status_code != 200:
        # try again with period of 120 days if full range doesn't work
        if service == 'instantaneous' and date_range == 'all':
            date_range = datetime.timedelta(days=120)
            return _get_site_values(service, date_range, url_params)
        else:
            return {}
    content_io = StringIO.StringIO(str(req.content))

    data_dict = {}
    for (event, ele) in iterparse(content_io):
        if ele.tag == NS + "timeSeries":
            values_element = ele.find(NS + 'values')
            values = _parse_values(values_element)
            var_element = ele.find(NS + 'variable')
            variable = _parse_variable(var_element)
            code = variable['code']
            if 'statistic' in variable:
                code += ":" + variable['statistic']['code']
            data_dict[code] = {
                'last_refresh': query_isodate,
                'values': values,
                'variable': variable,
            }

    return data_dict


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


def _parse_sites(content_io):
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
