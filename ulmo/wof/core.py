"""
    ulmo.wof.core
    ~~~~~~~~~~~~~

    This module provides direct access to `CUAHSI WaterOneFlow`_ web services.


    .. _CUAHSI WaterOneFlow: http://his.cuahsi.org/wofws.html
"""
import cStringIO as StringIO

import suds

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

    return {
        site['network'] + ':' + site['code']: site
        for site in sites.values()
    }


def get_site_info(wsdl_url, site_code):
    """
    Retrieves detailed site information e_info.

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
    sites_dict : dict
        a python dict with site codes mapped to site information
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
    series_dict = {
        series['variable_code_vocabulary'] + ':' + series['variable_code']: series
        for series in site_info['series']
    }
    site_info['series'] = series_dict
    return site_info


def _waterml_version(suds_client):
    tns_str = str(suds_client.wsdl.tns[1])
    if tns_str == 'http://www.cuahsi.org/his/1.0/ws/':
        return '1.0'
    elif tns_str == 'http://www.cuahsi.org/his/1.1/ws/':
        return '1.1'
    else:
        raise NotImplementedError("only WaterOneFlow 1.0 and 1.1 are currently"
            " supported")
