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

    _series = None
    _site_info = None

    def __init__(self, name=None, code=None, id=None, network=None,
                 location=None, suds_client=None):
        self.name = name
        self.code = code
        self.id = id
        self.network = network
        self.location = util._get_shapely_from_geolocation(location)
        self.suds_client = suds_client

    @property
    def site_info(self):
        if not self._site_info:
            self._update_site_info()
        return self._site_info

    @property
    def variables(self):
        if not self._series:
            self._update_site_info()
        return [series.variable for series in self._series]

    def _update_site_info(self):
        """makes a GetSiteInfo updates site info and series information"""
        self._site_info = self.suds_client.service.GetSiteInfoObject(
            '%s:%s' % (self.network, self.code))

        if len(self._site_info.site) > 1 or \
               len(self._site_info.site[0].seriesCatalog) > 1:
            raise NotImplementedError(
                "Multiple site instances or multiple seriesCatalogs not "
                "currently supported")

        series_list = self._site_info.site[0].seriesCatalog[0].series
        self._series = [util._get_series_from_waterml(series)
                        for series in series_list]

    def __repr__(self):
        return "<Site: %s [%s]>" % (self.name, self.code)


class Series(object):
    """
    Contains information about a time series
    """

    def __init__(self, variable=None, count=None, method=None,
                 quality_control_level=None, begin_datetime=None,
                 end_datetime=None):
        self.variable = variable
        self.count = count
        self.method = method
        self.quality_control_level = quality_control_level
        self.begin_datetime = begin_datetime
        self.end_datetime = end_datetime


class Variable(object):
    """
    Contains information about a variable
    """

    def __init__(self, name=None, code=None, id=None, vocabulary=None,
                 units=None, no_data_value=None):
        self.name = name
        self.code = code
        self.id = id
        self.vocabulary = vocabulary
        self.units = units
        self.no_data_value = no_data_value

    def __repr__(self):
        return "<Variable: %s [%s]>" % (self.name, self.code)


class Units(object):
    """
    Contains information about units of measurement
    """

    def __init__(self, name=None, abbreviation=None, code=None):
        self.name = name
        self.abbreviation = abbreviation
        self.code = code


class Client(object):
    """Main client object"""

    suds_client = None

    def __init__(self, wsdl_url):
        self.suds_client = suds.client.Client(wsdl_url)

        get_all_sites_query = self.suds_client.service.GetSites('')
        self.sites = [util._get_site_from_site_info(site, self.suds_client)
                      for site in get_all_sites_query.site]
