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

from ulmo import util
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
        Two-letter state code used in stateCd parameter.
    site_type : str or ``None``
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
                  start=None, end=None, period=None, modified_since=None):
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
    start : datetime (see :ref:`dates-and-times`)
        Start of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    end : datetime (see :ref:`dates-and-times`)
        End of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    period : str or datetime.timedelta
        Period of time to use for requesting data. This will be passed along as
        the period parameter. This can either be 'all' to signal that you'd like
        the entire period of record, or string in ISO 8601 period format (e.g.
        'P1Y2M21D' for a period of one year, two months and 21 days) or it can
        be a datetime.timedelta object representing the period of time. This
        parameter is mutually exclusive with start/end dates.
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

    if not (start is None or end is None) and not period is None:
        raise ValueError("using date range with start/end AND period is allowed"
                " because it's ambiguous, use one or the other")
    if not period is None:
        if isinstance(period, basestring):
            if period == 'all':
                if service in ('iv', 'instantaneous'):
                    start = datetime.datetime(2007, 10, 1)
                if service in ('dv', 'daily'):
                    start = datetime.datetime(1851, 1, 1)
            else:
                url_params['period'] = period
        elif isinstance(period, datetime.timedelta):
            url_params['period'] = isodate.duration_isoformat(period)
    if not start is None:
        start_datetime = util.convert_datetime(start)
        url_params['startDT'] = isodate.datetime_isoformat(start_datetime)
    if not end is None:
        end_datetime = util.convert_datetime(end)
        url_params['endDT'] = isodate.datetime_isoformat(end_datetime)

    if service in ('daily', 'instantaneous'):
        values = _get_site_values(service, url_params)
    elif not service:
        values = _get_site_values('daily', url_params)
        values.update(
            _get_site_values('instantaneous', url_params))
    else:
        raise ValueError("service must either be 'daily', 'instantaneous' or none")

    return values


def _get_service_url(service):
    if service in ('daily', 'dv'):
        return DAILY_URL
    elif service in ('instantaneous', 'iv'):
        return INSTANTANEOUS_URL
    else:
        raise "service must be either 'daily' ('dv') or 'instantaneous' ('iv')"


def _get_site_values(service, url_params):
    """downloads and parses values for a site

    returns a values dict containing variable and data values
    """
    service_url = _get_service_url(service)

    query_isodate = isodate.datetime_isoformat(datetime.datetime.now())
    try:
        req = requests.get(service_url, params=url_params)
    except requests.exceptions.ConnectionError:
        log.info("There was a connection error with query:\n\t%s\n\t%s" % (service_url, url_params))
        return {}
    log.info("processing data from request: %s" % req.request.full_url)

    if req.status_code != 200:
        return {}
    content_io = StringIO.StringIO(str(req.content))
    util.save_pretty_printed_xml('a.out', content_io)

    data_dict = wml.parse_site_values(content_io, query_isodate)

    return data_dict
