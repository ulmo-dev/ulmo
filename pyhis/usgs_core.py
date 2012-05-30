import cStringIO as StringIO
import logging

from lxml.etree import iterparse
import requests


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


def _parse_geog_location(geog_location):
    """returns a dict representation of a geogLocation etree element"""
    return {
        'srs': geog_location.attrib.get('srs'),
        'latitude': geog_location.find(NS + 'latitude').text,
        'longitude': geog_location.find(NS + 'longitude').text,
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


def _get_service_url(service):
    if service in ('daily', 'dv'):
        return DAILY_URL
    elif service in ('instantaneous', 'iv'):
        return INSTANTANEOUS_URL
    else:
        raise "service must be either 'daily' ('dv') or 'instantaneous' ('iv')"
