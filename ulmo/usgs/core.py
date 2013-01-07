"""
    ulmo.usgs.core
    ~~~~~~~~~~~~~~

    This module provides direct access to `USGS National Water Information
    System`_ web services.


    .. _USGS National Water Information System: http://waterdata.usgs.gov/nwis

"""
import cStringIO as StringIO
import datetime
import logging

import isodate
import requests

import ulmo.waterml.v1_1 as wml


INSTANTANEOUS_URL = "http://waterservices.usgs.gov/nwis/iv/"
DAILY_URL = "http://waterservices.usgs.gov/nwis/dv/"

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_sites(sites=None, state_code=None, site_type=None, service=None):
    """Fetches site information from USGS services. See the USGS waterservices
    documentation for options.


    Parameters
    ----------
    sites : str, iterable of strings or ``None``
        The site to use or list of sites to use; lists will be joined by a ','.
    state_code : str or ``None``
    'National Climactic Data Center
        Two-letter state code used in stateCd parameter.
    site_type : str or ``None``
    'National Climactic Data Center
        Type of site used in siteType parameter.
    service : {``None``, 'individual', 'daily'}
        The service to use, either "individual", "daily", or ``None`` (default). If
        ``None``, then both services are used.


    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
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

        return_sites = wml.parse_site_infos(content_io)
    return return_sites


def get_site_data(site_code, service=None, parameter_code=None,
                  date_range=None, modified_since=None):
    """Fetches site data.


    Parameters
    ----------
    site_code : str
        The site code of the site you want to query data for.
    service : {``None``, 'individual', 'daily'}
        The service to use, either "individual", "daily", or ``None`` (default). If
        ``None``, then both services are used.
    parameter_code : str
        Parameter code(s) that will be passed as the parameterCd parameter.
    date_range : date range
        Date range to be used for the query. This will be deprecated very soon
        and replaced with more explicit parameters.
    modified_since : ``None`` or datetime.timedelta
        Passed along as the modifiedSince parameter.


    Returns
    -------
    data_dict : dict
        a python dict with parameter codes mapped to value dicts
    """
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

    data_dict = wml.parse_site_values(content_io, query_isodate)

    return data_dict
