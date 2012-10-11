import cStringIO as StringIO

import suds

import ulmo.waterml.v1_0 as wml


def get_sites(wsdl_url):
    suds_client = suds.client.Client(wsdl_url)
    suds_client.service.GetSites('')
    response_text = unicode(suds_client.last_received())
    response_buffer = StringIO.StringIO()

    # hacks: Hydroserver doesn't declare soap namespace so it doesn't validate
    inject_namespaces = ['soap', 'wsa', 'wsse', 'wsu', 'xsi']
    response_buffer.write(response_text[:53])
    for inject_namespace in inject_namespaces:
        response_buffer.write(' xmlns:%s="http://soap/envelope/"' % inject_namespace)
    response_buffer.write(response_text[53:])
    response_buffer.seek(0)
    sites = wml.parse_sites(response_buffer)
    return sites


def get_site_data(wsdl_url, site_code, network, variable_code, variable_vocabulary):
        #kservice=None, parameter_code=None,
                  #date_range=None, modified_since=None):
    suds_client = suds.client.Client(wsdl_url)
    suds_client.service.GetValuesObject(
        '%s:%s' % (network, site_code),
        '%s:%s' % (timeseries.variable.vocabulary, timeseries.variable.code),
        begin_date_str,
        end_date_str)
    suds_client.service.GetSites('')
    response_text = unicode(suds_client.last_received())
    response_buffer = StringIO.StringIO()

