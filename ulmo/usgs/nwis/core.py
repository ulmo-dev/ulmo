"""
    ulmo.usgs.core
    ~~~~~~~~~~~~~~

    This module provides direct access to `USGS National Water Information
    System`_ web services.


    .. _USGS National Water Information System: http://waterdata.usgs.gov/nwis

"""
import contextlib
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


def get_sites(sites=None, state_code=None, site_type=None, service=None,
        input_file=None):
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
    service : {``None``, 'instantaneous', 'iv', 'daily', 'dv'}
        The service to use, either "instantaneous", "daily", or ``None``
        (default).  If set to ``None``, then both services are used.  The
        abbreviations "iv" and "dv" can be used for "instantaneous" and "daily",
        respectively.
    input_file: ``None``, file path or file object
        If ``None`` (default), then the NWIS web services will be queried, but
        if a file is passed then this file will be used instead of requesting
        data from the NWIS web services.

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

    if input_file is None:
        if not service:
            return_sites = get_sites(sites=sites, state_code=state_code,
                    site_type=site_type, service="daily", input_file=input_file)
            instantaneous_sites = get_sites(sites=sites, state_code=state_code,
                site_type=site_type, service="instantaneous", input_file=input_file)
            return_sites.update(instantaneous_sites)
            return return_sites

        url = _get_service_url(service)
        log.info('making request for sites: %s' % url)
        req = requests.get(url, params=url_params)
        log.info("processing data from request: %s" % req.request.url)
        input_file = StringIO.StringIO(str(req.content))

    with _open_input_file(input_file) as content_io:
        return_sites = wml.parse_site_infos(content_io)

    return_sites = dict([
        (code, _extract_site_properties(site))
        for code, site in return_sites.iteritems()
    ])

    return return_sites


def get_site_data(site_code, service=None, parameter_code=None, start=None,
        end=None, period=None, modified_since=None, input_file=None):
    """Fetches site data.


    Parameters
    ----------
    site_code : str
        The site code of the site you want to query data for.
    service : {``None``, 'instantaneous', 'iv', 'daily', 'dv'}
        The service to use, either "instantaneous", "daily", or ``None``
        (default).  If set to ``None``, then both services are used.  The
        abbreviations "iv" and "dv" can be used for "instantaneous" and "daily",
        respectively.
    parameter_code : str
        Parameter code(s) that will be passed as the parameterCd parameter.
    start : ``None`` or datetime (see :ref:`dates-and-times`)
        Start of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    end : ``None`` or datetime (see :ref:`dates-and-times`)
        End of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    period : {``None``, str, datetime.timedelta}
        Period of time to use for requesting data. This will be passed along as
        the period parameter. This can either be 'all' to signal that you'd like
        the entire period of record, or string in ISO 8601 period format (e.g.
        'P1Y2M21D' for a period of one year, two months and 21 days) or it can
        be a datetime.timedelta object representing the period of time. This
        parameter is mutually exclusive with start/end dates.
    modified_since : ``None`` or datetime.timedelta
        Passed along as the modifiedSince parameter.
    input_file: ``None``, file path or file object
        If ``None`` (default), then the NWIS web services will be queried, but
        if a file is passed then this file will be used instead of requesting
        data from the NWIS web services.


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

    if not (start is None or end is None) and period is not None:
        raise ValueError("must use either a date range with start/end OR a "
                "period, but not both")
    if period is not None:
        if isinstance(period, basestring):
            if period == 'all':
                if service in ('iv', 'instantaneous'):
                    start = datetime.datetime(2007, 10, 1)
                elif service in ('dv', 'daily'):
                    start = datetime.datetime(1851, 1, 1)
            else:
                url_params['period'] = period
        elif isinstance(period, datetime.timedelta):
            url_params['period'] = isodate.duration_isoformat(period)

    if service in ('dv', 'daily'):
        datetime_formatter = isodate.date_isoformat
    else:
        datetime_formatter = isodate.datetime_isoformat
    if start is not None:
        start_datetime = util.convert_datetime(start)
        url_params['startDT'] = datetime_formatter(start_datetime)
    if end is not None:
        end_datetime = util.convert_datetime(end)
        url_params['endDT'] = datetime_formatter(end_datetime)

    if service is not None:
        values = _get_site_values(service, url_params, input_file=input_file)
    else:
        kwargs = dict(parameter_code=parameter_code, start=start, end=end,
                period=period, modified_since=modified_since,
                input_file=input_file)
        values = get_site_data(site_code, service='daily', **kwargs)
        values.update(
            get_site_data(site_code, service='instantaneous', **kwargs))

    return values


def _extract_site_properties(site):
    rename_properties = [
        ('county_cd', 'county'),
        ('huc_cd', 'huc'),
        ('site_type_cd', 'site_type'),
        ('state_cd', 'state_code'),
    ]
    site_properties = site['site_property']
    for old, new in rename_properties:
        if old in site_properties:
            site[new] = site_properties[old]
            del site_properties[old]

    if len(site_properties) == 0:
        del site['site_property']
    else:
        site['site_property'] = site_properties

    return site


def _get_service_url(service):
    if service in ('daily', 'dv'):
        return DAILY_URL
    elif service in ('instantaneous', 'iv'):
        return INSTANTANEOUS_URL
    else:
        raise ValueError("service must be either 'daily' ('dv') or "
                "'instantaneous' ('iv')")


def _get_site_values(service, url_params, input_file=None):
    """downloads and parses values for a site

    returns a values dict containing variable and data values
    """
    if input_file is None:
        query_isodate = isodate.datetime_isoformat(datetime.datetime.now())
        service_url = _get_service_url(service)

        try:
            req = requests.get(service_url, params=url_params)
        except requests.exceptions.ConnectionError:
            log.info("There was a connection error with query:\n\t%s\n\t%s" % (service_url, url_params))
            return {}
        log.info("processing data from request: %s" % req.request.url)

        if req.status_code != 200:
            return {}
        input_file = StringIO.StringIO(str(req.content))
    else:
        query_isodate = None

    with _open_input_file(input_file) as content_io:
        data_dict = wml.parse_site_values(content_io, query_isodate)

        for variable_dict in data_dict.values():
            variable_dict['site'] = _extract_site_properties(variable_dict['site'])

    return data_dict


@contextlib.contextmanager
def _open_input_file(input_file):
    """helper context manager. If input_file is a string then it yields an open
    file handler, closing it afterwards. If input_file is already a file handler
    then it just yields the same file handler without closing.
    """
    if isinstance(input_file, basestring):
        with open(input_file, 'rb') as content_io:
            yield content_io
    elif hasattr(input_file, 'read'):
        yield input_file
