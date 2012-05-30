import cStringIO as StringIO
import datetime
import logging

import isodate
from lxml.etree import iterparse
import requests
import pytz


INSTANTANEOUS_URL = "http://waterservices.usgs.gov/nwis/iv/"
DAILY_URL = "http://waterservices.usgs.gov/nwis/dv/"
NS = "{http://www.cuahsi.org/waterML/1.1/}"

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


def get_sites(state_code, site_type=None, service="daily"):
    """returns a dict containing site code and site names; currently
    only supports queries by state_code
    """
    url = _get_service_url(service)

    url_params = {'format': 'waterml',
                  'stateCd': state_code}

    if site_type:
        url_params['siteType'] = site_type

    log.info('making request for sites: %s' % url)
    req = requests.get(url, params=url_params)
    content_io = StringIO.StringIO(str(req.content))

    site_elements = dict(set([(ele.find(NS + "siteCode").text, ele)
                     for (event, ele) in iterparse(content_io)
                     if ele.tag == NS + "sourceInfo"]))
    sites = dict([(key, _parse_site_info(source_info))
                    for key, source_info in site_elements.iteritems()])
    return sites


def get_site_data(service_url, site_code, parameter_code=None,
                  date_range=None, modified_since=None):
    """queries service for data and returns a data dict"""
    url_params = {'format': 'waterml',
                  'site': site_code}
    if parameter_code:
        url_params['parameterCd'] = parameter_code
    if modified_since:
        url_params['modifiedSince'] = isodate.duration_isoformat(modified_since)

    url_params.update(_date_range_url_params(date_range, service_url))

    req = requests.get(service_url, params=url_params)
    print "processing data from request: %s" % req.request.full_url

    if req.status_code != 200:
        # try again with period of 120 days if full range doesn't work
        if date_range == 'all':
            date_range = datetime.timedelta(days=120)
            return get_site_data(service_url, site_code, parameter_code, date_range, modified_since)
        else:
            return {}
    content_io = StringIO.StringIO(str(req.content))
    return _parse_site_data_from_waterml(content_io, service_url)


def _date_range_url_params(date_range, url):
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
        if 'iv' in url:
            return dict(startDT=isodate.date_isoformat(datetime.datetime(2007, 10, 1)))
        if 'dv' in url:
            return dict(startDT=isodate.datetime_isoformat(datetime.datetime(1851, 1, 1)))

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


def _parse_datetime(iso_datetime_str):
    """returns a naive timezone from a given """
    datetime = isodate.parse_datetime(iso_datetime_str)
    if datetime.tzinfo is not None:
        return datetime.astimezone(tz=pytz.utc).replace(tzinfo=None)
    else:
        return datetime


def _parse_geog_location(geog_location):
    """returns a dict representation of a geogLocation etree element"""
    return {
        'srs': geog_location.attrib.get('srs'),
        'latitude': geog_location.find(NS + 'latitude').text,
        'longitude': geog_location.find(NS + 'longitude').text,
    }


def _parse_site_data_from_waterml(content_io, service_url):
    data_dict = {}

    for (event, ele) in iterparse(content_io):
        if ele.tag == NS + "timeSeries":
            values_element = ele.find(NS + 'values')
            values = _parse_values(values_element)
            var_element = ele.find(NS + 'variable')
            code = var_element.find(NS + 'variableCode').text
            data_dict[code] = values
    return data_dict


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
        'county': site_info.find(NS + "siteProperty" + "[@name='countyCd']").text,
        'huc': site_info.find(NS + "siteProperty" + "[@name='hucCd']").text,
        'location': _parse_geog_location(geog_location),
        'name': site_info.find(NS + "siteName").text,
        'network': site_code.attrib.get('network'),
        'site_type': site_info.find(NS + "siteProperty" + "[@name='siteTypeCd']").text,
        'state_code': site_info.find(NS + "siteProperty" + "[@name='stateCd']").text,
        'timezone_info': _parse_timezone_info(timezone_info),
    }


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
        'offset': timezone_element.attrib.get('zoneOffset'),
        'abbreviation': timezone_element.attrib.get('zoneAbbreviation'),
    }


def _parse_values(values_element):
    """returns a list of dicts that represent the values for a given etree
    values element
    """

    return [{'datetime_utc': _parse_datetime(value.attrib['dateTime']),
             'value': value.text,
             'qualifiers': value.attrib['qualifiers']}
            for value in values_element.findall(NS + 'value')]
