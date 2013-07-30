"""
    ulmo.wof.core
    ~~~~~~~~~~~~~

    This module provides direct access to `CUAHSI WaterOneFlow`_ web services.


    .. _CUAHSI WaterOneFlow: http://his.cuahsi.org/wofws.html
"""
import cStringIO as StringIO

import suds
import isodate

from ulmo import util
from ulmo import waterml


def get_sites(wsdl_url):
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

    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
    """
    suds_client = suds.client.Client(wsdl_url)

    waterml_version = _waterml_version(suds_client)
    if waterml_version == '1.0':
        response = suds_client.service.GetSitesXml('')
        response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))
        sites = waterml.v1_0.parse_site_infos(response_buffer)
    elif waterml_version == '1.1':
        response = suds_client.service.GetSites('')
        response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))
        sites = waterml.v1_1.parse_site_infos(response_buffer)

    return dict([
        (site['network'] + ':' + site['code'], site)
        for site in sites.values()
    ])


def get_site_info(wsdl_url, site_code):
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

    Returns
    -------
    site_info : dict
        a python dict containing site information
    """
    suds_client = suds.client.Client(wsdl_url)

    waterml_version = _waterml_version(suds_client)
    if waterml_version == '1.0':
        response = suds_client.service.GetSiteInfo(site_code)
        response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))
        sites = waterml.v1_0.parse_sites(response_buffer)
    elif waterml_version == '1.1':
        response = suds_client.service.GetSiteInfo(site_code)
        response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))
        sites = waterml.v1_1.parse_sites(response_buffer)

    if len(sites) == 0:
        return {}
    site_info = sites.values()[0]
    series_dict = dict([
        (series['variable']['vocabulary'] + ':' + series['variable']['code'],
            series)
        for series in site_info['series']
    ])
    site_info['series'] = series_dict
    return site_info


def get_values(wsdl_url, site_code, variable_code=None, start=None, end=None):
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

    Returns
    -------
    site_values : dict
        a python dict containing values
    """
    suds_client = suds.client.Client(wsdl_url)

    # Note from Emilio:
    #   Not clear if WOF servers really do handle time zones (time offsets or
    #   "Z" in the iso8601 datetime strings. In the past, I (Emilio) have
    #   passed naive strings to GetValues(). if a datetime object is passed to
    #   this ulmo function, the isodate code above will include it in the
    #   resulting iso8601 string; if not, no.  Test effect of dt_isostr having
    #   a timezone code or offset, vs not having it (the latter, naive dt
    #   strings, is what I've been using all along)

    # the intepretation of start and end time zone is server-dependent
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

    response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))
    if waterml_version == '1.0':
        values = waterml.v1_0.parse_site_values(response_buffer)
    elif waterml_version == '1.1':
        values = waterml.v1_1.parse_site_values(response_buffer)

    if not variable_code is None:
        return values.values()[0]
    else:
        return values


def get_variable_info(wsdl_url, variable_code=None):
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

    Returns
    -------
    variable_info : dict
        a python dict containing variable information. If no variable code is
        `None` (default) then this will be a nested set of dicts keyed by
        <vocabulary>:<variable_code>
    """
    suds_client = suds.client.Client(wsdl_url)

    waterml_version = _waterml_version(suds_client)
    response = suds_client.service.GetVariableInfo(variable_code)
    response_buffer = StringIO.StringIO(response.encode('ascii', 'ignore'))

    if waterml_version == '1.0':
        variable_info = waterml.v1_0.parse_variables(response_buffer)
    elif waterml_version == '1.1':
        variable_info = waterml.v1_1.parse_variables(response_buffer)

    if not variable_code is None and len(variable_info) == 1:
        return variable_info.values()[0]
    else:
        return dict([
            ('%s:%s' % (var['vocabulary'], var['code']), var)
            for var in variable_info.values()
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
