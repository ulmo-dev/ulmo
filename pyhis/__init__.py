"""
    PyHIS
    ~~~~~~~

    PyHIS is a python library for querying CUAHSI*-HIS** web
    services.

    * CUAHSI is the Consortium of Universities for the
    Advancement of Hydrologic Science, Inc.
    ** HIS stands for Hydrlogic Information System
"""
import shapely
import suds

import util


class Site(object):
    """
    Contains information about a site
    """

    def __init__(self, name=None, code=None, id=None, network=None,
                 location=None):
        self.name = name
        self.code = code
        self.id = id
        self.network = network
        self.location = util._get_shapely_from_geolocation(location)

    def __repr__(self):
        return "<Site: %s [%s]>" % (self.name,
                                    self.code)


class Client(object):
    """Main client object"""

    suds_client = None

    def __init__(self, wsdl_url):
        self.suds_client = suds.client.Client(wsdl_url)

        get_all_sites_query = self.suds_client.service.GetSites('')
        self.sites = [util._get_site_from_site_info(site)
                      for site in get_all_sites_query.site]
