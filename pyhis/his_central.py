import suds

HIS_CENTRAL_WSDL_URL = 'http://hiscentral.cuahsi.org/webservices/hiscentral.asmx?WSDL'


def services():
    """returns a list of tuples containing (service_name, wsdl_url,
    network_name) for all the services registered to HIS Central
    (http://hiscentral.cuahsi.org)
    """

    his_central = suds.client.Client(HIS_CENTRAL_WSDL_URL)

    all_services_request = his_central.service.GetServicesInBox2(
        xmin=-180, ymin=-90, xmax=180, ymax=90)

    return [("%s: %s" % (service.organization, service.Title),
             str(service.servURL), str(service.NetworkName))
            for service in all_services_request.ServiceInfo]
