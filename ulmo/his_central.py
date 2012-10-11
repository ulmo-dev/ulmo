import suds

HIS_CENTRAL_WSDL_URL = 'http://hiscentral.cuahsi.org/webservices/hiscentral.asmx?WSDL'


def services(x_min=-180, y_min=-90, x_max=180, y_max=90):
    """returns a list of tuples containing (service_name, wsdl_url,
    network_name) for all the services registered to HIS Central
    (http://hiscentral.cuahsi.org). Optional arguments are the x_min,
    y_min, x_max, and y_max for a bounding box that covers the area
    you want to look for services in. By default, these are set to
    cover the whole world.
    """

    his_central = suds.client.Client(HIS_CENTRAL_WSDL_URL)

    all_services_request = his_central.service.GetServicesInBox2(
        xmin=x_min, ymin=y_min, xmax=x_max, ymax=y_max)

    return [("%s: %s" % (service.organization, service.Title),
             str(service.servURL), str(service.NetworkName))
            for service in all_services_request.ServiceInfo]
