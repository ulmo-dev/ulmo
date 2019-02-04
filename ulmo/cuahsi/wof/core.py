"""
    ulmo.wof.core
    ~~~~~~~~~~~~~

    This module provides direct access to `CUAHSI WaterOneFlow`_ web services.


    .. _CUAHSI WaterOneFlow: http://his.cuahsi.org/wofws.html
"""
from future import standard_library
standard_library.install_aliases()
from builtins import str
import io

import suds.client
import isodate

from ulmo import util
from ulmo import waterml


_suds_client = None


def get_sites(wsdl_url, suds_cache=("default",), timeout=None):
    """
    Retrieves information on the sites that are available from a WaterOneFlow
    service using a GetSites request.  For more detailed information including
    which variables and time periods are available for a given site, use
    ``get_site_info()``.

    Parameters
    ----------
    wsdl_url : str
        URL of a service's web service definition language (WSDL) description.
        All WaterOneFlow services publish a WSDL description and this url is the
        entry point to the service.
    suds_cache : ``None`` or tuple
        SOAP local cache duration for WSDL description and client object.
        Pass a cache duration tuple like ('days', 3) to set a custom duration.
        Duration may be in months, weeks, days, hours, or seconds.
        If unspecified, the default duration (1 day) will be used.
        Use ``None`` to turn off caching.
    timeout : int or float
        suds SOAP URL open timeout (seconds).
        If unspecified, the suds default (90 seconds) will be used.

    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
    """
    suds_client = _get_client(wsdl_url, suds_cache, timeout)

    waterml_version = _waterml_version(suds_client)
    if waterml_version == '1.0':
        response = suds_client.service.GetSitesXml('')
        response_buffer = io.BytesIO(util.to_bytes(response))
        sites = waterml.v1_0.parse_site_infos(response_buffer)
    elif waterml_version == '1.1':
        response = suds_client.service.GetSites('')
        response_buffer = io.BytesIO(util.to_bytes(response))
        sites = waterml.v1_1.parse_site_infos(response_buffer)

    return dict([
        (site['network'] + ':' + site['code'], site)
        for site in list(sites.values())
    ])


def get_site_info(wsdl_url, site_code, suds_cache=("default",), timeout=None):
    """
    Retrieves detailed site information from a WaterOneFlow service using a
    GetSiteInfo request.

    Parameters
    ----------
    wsdl_url : str
        URL of a service's web service definition language (WSDL) description.
        All WaterOneFlow services publish a WSDL description and this url is the
        entry point to the service.
    site_code : str
        Site code of the site you'd like to get more information for. Site codes
        MUST contain the network and be of the form <network>:<site_code>, as is
        required by WaterOneFlow.
    suds_cache : ``None`` or tuple
        SOAP local cache duration for WSDL description and client object.
        Pass a cache duration tuple like ('days', 3) to set a custom duration.
        Duration may be in months, weeks, days, hours, or seconds.
        If unspecified, the default duration (1 day) will be used.
        Use ``None`` to turn off caching.
    timeout : int or float
        suds SOAP URL open timeout (seconds).
        If unspecified, the suds default (90 seconds) will be used.

    Returns
    -------
    site_info : dict
        a python dict containing site information
    """
    suds_client = _get_client(wsdl_url, suds_cache, timeout)

    waterml_version = _waterml_version(suds_client)
    if waterml_version == '1.0':
        response = suds_client.service.GetSiteInfo(site_code)
        response_buffer = io.BytesIO(util.to_bytes(response))
        sites = waterml.v1_0.parse_sites(response_buffer)
    elif waterml_version == '1.1':
        response = suds_client.service.GetSiteInfo(site_code)
        response_buffer = io.BytesIO(util.to_bytes(response))
        sites = waterml.v1_1.parse_sites(response_buffer)

    if len(sites) == 0:
        return {}
    site_info = list(sites.values())[0]
    series_dict = dict([
        (series['variable']['vocabulary'] + ':' + series['variable']['code'],
            series)
        for series in site_info['series']
    ])
    site_info['series'] = series_dict
    return site_info


def get_values(wsdl_url, site_code, variable_code, start=None, end=None, 
               suds_cache=("default",), timeout=None):
    """
    Retrieves site values from a WaterOneFlow service using a GetValues request.

    Parameters
    ----------
    wsdl_url : str
        URL of a service's web service definition language (WSDL) description.
        All WaterOneFlow services publish a WSDL description and this url is the
        entry point to the service.
    site_code : str
        Site code of the site you'd like to get values for. Site codes MUST
        contain the network and be of the form <network>:<site_code>, as is
        required by WaterOneFlow.
    variable_code : str
        Variable code of the variable you'd like to get values for. Variable
        codes MUST contain the network and be of the form
        <vocabulary>:<variable_code>, as is required by WaterOneFlow.
    start : ``None`` or datetime (see :ref:`dates-and-times`)
        Start of a date range for a query. If both start and end parameters are
        omitted, the entire time series available will be returned.
    end : ``None`` or datetime (see :ref:`dates-and-times`)
        End of a date range for a query. If both start and end parameters are
        omitted, the entire time series available will be returned.
    suds_cache : ``None`` or tuple
        SOAP local cache duration for WSDL description and client object.
        Pass a cache duration tuple like ('days', 3) to set a custom duration.
        Duration may be in months, weeks, days, hours, or seconds.
        If unspecified, the default duration (1 day) will be used.
        Use ``None`` to turn off caching.
    timeout : int or float
        suds SOAP URL open timeout (seconds).
        If unspecified, the suds default (90 seconds) will be used.

    Returns
    -------
    site_values : dict
        a python dict containing values
    """
    suds_client = _get_client(wsdl_url, suds_cache, timeout)

    # Note from Emilio:
    #   Not clear if WOF servers really do handle time zones (time offsets or
    #   "Z" in the iso8601 datetime strings. In the past, I (Emilio) have
    #   passed naive strings to GetValues(). if a datetime object is passed to
    #   this ulmo function, the isodate code above will include it in the
    #   resulting iso8601 string; if not, no.  Test effect of dt_isostr having
    #   a timezone code or offset, vs not having it (the latter, naive dt
    #   strings, is what I've been using all along)

    # the interpretation of start and end time zone is server-dependent
    start_dt_isostr = None
    end_dt_isostr = None
    if start is not None:
        start_datetime = util.convert_datetime(start)
        start_dt_isostr = isodate.datetime_isoformat(start_datetime)
    if end is not None:
        end_datetime = util.convert_datetime(end)
        end_dt_isostr = isodate.datetime_isoformat(end_datetime)

    waterml_version = _waterml_version(suds_client)
    response = suds_client.service.GetValues(
        site_code, variable_code, startDate=start_dt_isostr,
        endDate=end_dt_isostr)

    response_buffer = io.BytesIO(util.to_bytes(response))
    if waterml_version == '1.0':
        values = waterml.v1_0.parse_site_values(response_buffer)
    elif waterml_version == '1.1':
        values = waterml.v1_1.parse_site_values(response_buffer)

    if not variable_code is None:
        return list(values.values())[0]
    else:
        return values


def get_variable_info(wsdl_url, variable_code=None, 
                      suds_cache=("default",), timeout=None):
    """
    Retrieves site values from a WaterOneFlow service using a GetVariableInfo
    request.

    Parameters
    ----------
    wsdl_url : str
        URL of a service's web service definition language (WSDL) description.
        All WaterOneFlow services publish a WSDL description and this url is the
        entry point to the service.
    variable_code : `None` or str
        If `None` (default) then information on all variables will be returned,
        otherwise, this should be set to the variable code of the variable you'd
        like to get more information on.  Variable codes MUST contain the
        network and be of the form <vocabulary>:<variable_code>, as is required
        by WaterOneFlow.
    suds_cache : ``None`` or tuple
        SOAP local cache duration for WSDL description and client object.
        Pass a cache duration tuple like ('days', 3) to set a custom duration.
        Duration may be in months, weeks, days, hours, or seconds.
        If unspecified, the default duration (1 day) will be used.
        Use ``None`` to turn off caching.
    timeout : int or float
        suds SOAP URL open timeout (seconds).
        If unspecified, the suds default (90 seconds) will be used.

    Returns
    -------
    variable_info : dict
        a python dict containing variable information. If no variable code is
        `None` (default) then this will be a nested set of dicts keyed by
        <vocabulary>:<variable_code>
    """
    suds_client = _get_client(wsdl_url, suds_cache, timeout)

    waterml_version = _waterml_version(suds_client)
    response = suds_client.service.GetVariableInfo(variable_code)
    response_buffer = io.BytesIO(util.to_bytes(response))

    if waterml_version == '1.0':
        variable_info = waterml.v1_0.parse_variables(response_buffer)
    elif waterml_version == '1.1':
        variable_info = waterml.v1_1.parse_variables(response_buffer)

    if not variable_code is None and len(variable_info) == 1:
        return list(variable_info.values())[0]
    else:
        return dict([
            ('%s:%s' % (var['vocabulary'], var['code']), var)
            for var in list(variable_info.values())
        ])


def _waterml_version(suds_client):
    tns_str = str(suds_client.wsdl.tns[1])
    if tns_str == 'http://www.cuahsi.org/his/1.0/ws/':
        return '1.0'
    elif tns_str == 'http://www.cuahsi.org/his/1.1/ws/':
        return '1.1'
    else:
        raise NotImplementedError(
            "only WaterOneFlow 1.0 and 1.1 are currently supported")


def _get_client(wsdl_url, suds_cache=("default",), suds_timeout=None):
    """
    Open and re-use (persist) a suds.client.Client instance _suds_client throughout
    the session, to minimize WOF server impact and improve performance.  _suds_client
    is global in scope.

    Parameters
    ----------
    wsdl_url : str
        URL of a service's web service definition language (WSDL) description.
        All WaterOneFlow services publish a WSDL description and this url is the
        entry point to the service.
    suds_cache : ``None`` or tuple
        suds client local cache duration for WSDL description and client object.
        Pass a cache duration tuple like ('days', 3) to set a custom duration.
        Duration may be in months, weeks, days, hours, or seconds.
        If unspecified, the suds default (1 day) will be used.
        Use ``None`` to turn off caching.
    suds_timeout : int or float
        suds SOAP URL open timeout (seconds).
        If unspecified, the suds default (90 seconds) will be used.

    Returns
    -------
    _suds_client : suds Client
        Newly or previously instantiated (reused) suds Client object.
    """
    global _suds_client

    # Handle new or changed client request (create new client)
    if _suds_client is None or _suds_client.wsdl.url != wsdl_url or not suds_timeout is None:
        _suds_client = suds.client.Client(wsdl_url)
        if suds_cache is None:
            _suds_client.set_options(cache=None)
        else:
            cache = _suds_client.options.cache
            # could add some error catching ...
            if suds_cache[0] == "default":
                cache.setduration(days=1)
            else:
                cache.setduration(**dict([suds_cache]))

        if not suds_timeout is None:
            _suds_client.set_options(timeout=suds_timeout)

    return _suds_client
