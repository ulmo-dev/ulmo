"""
    ulmo.cuahsi.his_central.core
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides direct access to the `CUAHSI HIS Central`_ web service.

    .. _CUAHSI HIS Central: http://hiscentral.cuahsi.org/
"""
import os
from builtins import str

import suds.client
from suds.cache import ObjectCache

from ulmo import util


HIS_CENTRAL_WSDL_URL = 'http://hiscentral.cuahsi.org/webservices/hiscentral.asmx?WSDL'


def get_services(bbox=None, user_cache=False):
    """Retrieves a list of services.

    Parameters
    ----------
    bbox : ``None`` or 4-tuple
        Optional argument for a bounding box that covers the area you want to
        look for services in. This should be a tuple containing (min_longitude,
        min_latitude, max_longitude, and max_latitude) with these values in
        decimal degrees. If not provided then the full set of services will be
        queried from HIS Central.
    user_cache : bool
        If False (default), use the system temp location to store cache WSDL and
        other files. Use the default user ulmo directory if True.

    Returns
    -------
    services_dicts : list
        A list of dicts that each contain information on an individual service.
    """
    if user_cache:
        cache_dir = os.path.join(util.get_ulmo_dir(), 'suds')
        util.mkdir_if_doesnt_exist(cache_dir)
        suds_client = suds.client.Client(HIS_CENTRAL_WSDL_URL,
                                          cache=ObjectCache(location=cache_dir))
    else:
        suds_client = suds.client.Client(HIS_CENTRAL_WSDL_URL)

    if bbox is None:
        services = suds_client.service.GetWaterOneFlowServiceInfo()
    else:
        x_min, y_min, x_max, y_max = bbox
        services = suds_client.service.GetServicesInBox2(
            xmin=x_min, ymin=y_min, xmax=x_max, ymax=y_max)

    services = [
        _service_dict(service_info)
        for service_info in services.ServiceInfo
    ]
    return services


def _cast_if_text(obj):
    """casts sax.text.Text objects to regular python strings, but leaves other
    objects unchanged
    """
    if isinstance(obj, suds.sax.text.Text):
        try:
            return str(obj)
        except UnicodeEncodeError:
            return str(obj)
    else:
        return obj


def _service_dict(service_info):
    """converts a ServiceInfo etree object into a service info dict"""
    change_keys = [
        # (old_key, new_key)
        ('aabstract', 'abstract'),
        ('maxx', 'max_x'),
        ('maxy', 'max_y'),
        ('minx', 'min_x'),
        ('miny', 'min_y'),
        ('orgwebsite', 'organization_website'),
        ('serv_url', 'service_url'),
        ('sitecount', 'site_count'),
        ('valuecount', 'value_count'),
        ('variablecount', 'variable_count'),
    ]

    service_dict = dict([
        (util.camel_to_underscore(key), _cast_if_text(value))
        for key, value in dict(service_info).items()
    ])

    for old_key, new_key in change_keys:
        if old_key in service_dict:
            service_dict[new_key] = service_dict[old_key]
            del service_dict[old_key]

    return service_dict
