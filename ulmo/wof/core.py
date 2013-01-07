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
    Retrieves information on available from a WaterOneFlow GetSites request.
    For more detailed information (including data available for a given site,
    use get_site_info.

    Parameters
    ----------
    wsdl_url : str

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


def get_site_data(wsdl_url, site_code, variable_code, variable_vocabulary):
    suds_client = suds.client.Client(wsdl_url)
    suds_client.service.GetValuesObject(
        '%s:%s' % (network, site_code),
        '%s:%s' % (timeseries.variable.vocabulary, timeseries.variable.code),
        begin_date_str,
        end_date_str)
    response_text = unicode(suds_client.last_received())
    response_buffer = StringIO.StringIO()


def _waterml_version(suds_client):
    tns_str = str(suds_client.wsdl.tns[1])
    if tns_str == 'http://www.cuahsi.org/his/1.0/ws/':
        return '1.0'
    elif tns_str == 'http://www.cuahsi.org/his/1.1/ws/':
        return '1.1'
    else:
        raise NotImplementedError("only WaterOneFlow 1.0 and 1.1 are currently"
            " supported")
