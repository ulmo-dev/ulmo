"""
    PyHIS.core
    ~~~~~~~~~~

    Core data models for PyHIS
"""

import itertools
import logging

import numpy as np
import pandas
import suds

import pyhis
from . import waterml
from . import shapefile

try:
    from . import cache
    if not cache.USE_CACHE:
        cache = None
except ImportError:
    cache = None

__all__ = ['Site', 'Source', 'TimeSeries', 'Variable', 'Units']


# fancy this up a bit sometime
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class Site(object):
    """
    Contains information about a site
    """
    _timeseries_dict = {}
    _dataframe = None
    _site_info_response = None
    _use_cache = None
    source = None
    name = None
    code = None
    id = None
    network = None
    latitude = None
    longitude = None

    def __init__(self, network=None, code=None, name=None, id=None,
                 latitude=None, longitude=None, source=None, use_cache=True):
        self.network = network
        self.code = code
        self.name = name
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.source = source
        self._use_cache = use_cache

        # if we don't have all the info, make a GetSiteInfo request
        # and update site attributes with that information
        if not name or not id or not latitude or not longitude:
            site_info = self.site_info_response.site[0].siteInfo

            if not self.name:
                self.name = site_info.siteName
            if not self.id:
                try:
                    self.id = site_info.siteName.siteCode[0]._siteID
                except AttributeError, KeyError:
                    # siteID is optional
                    pass
            if not self.latitude:
                self.latitude = site_info.geolocation.geogLocation.latitude
            if not self.longitude:
                self.longitude = site_info.geolocation.geogLocation.longitude

    @property
    def dataframe(self):
        if not self._timeseries_dict:
            self._update_site_info_response()
        if not self._dataframe:
            self._update_dataframe()
        return self._dataframe

    @property
    def site_info_response(self):
        if not self._site_info_response:
            self._update_site_info_response()
        return self._site_info_response

    @property
    def timeseries(self):
        if not len(self._timeseries_dict):
            self._update_timeseries_dict()
        return self._timeseries_dict

    def _update_dataframe(self):
        series_dict = dict((ts.variable.code, ts.series)
                       for ts in self.timeseries.values())
        self._dataframe = pandas.DataFrame(series_dict)

    def _update_site_info_response(self):
        """makes a GetSiteInfo updates site info and series information"""
        self._site_info_response = self.source.suds_client.service.GetSiteInfoObject(
            '%s:%s' % (self.network, self.code))

        if len(self._site_info_response.site) > 1 or \
               len(self._site_info_response.site[0].seriesCatalog) > 1:
            raise NotImplementedError(
                "Multiple site instances or multiple seriesCatalogs not "
                "currently supported")

    def _update_timeseries_dict(self):
        """updates the time series dict"""
        cache_enabled = self._use_cache and cache

        if cache_enabled:
            self._timeseries_dict = cache.get_timeseries_dict_for_site(self)
        else:
            self._timeseries_dict = waterml.get_timeseries_dict_for_site(self)

    def __repr__(self):
        return "<Site: %s [%s]>" % (self.name, self.code)


class Source(object):
    """Represents a water data source"""
    suds_client = None
    url = None
    _description = None
    _all_sites = False
    _sites = {}
    _use_cache = None

    def __init__(self, wsdl_url, use_cache=True):
        self.suds_client = suds.client.Client(wsdl_url)
        self.url = wsdl_url
        self._use_cache = use_cache

    @property
    def sites(self):
        return self.get_all_sites()

    @property
    def description(self):
        if not self._description:
            self._update_description()
        return self._description

    def get_all_sites(self):
        """returns all the sites available for a given source"""
        if not self._all_sites:
            self._update_all_sites()
        return self._sites

    def get_site(self, network, site_code):
        """returns a single site"""
        if (network, site_code) in self._sites:
            return _sites[(network, site_code)]

        cache_enabled = self._use_cache and cache
        if cache_enabled:
            return cache.get_site(self, network, site_code)
        else:
            return Site(self, network=network, code=site_code)

    def _update_description(self):
        """update self._description"""
        cache_enabled = self._use_cache and cache

        if cache_enabled:
            self._description = cache.get_description_for_source(self)
        else:
            self._description = waterml.get_description_for_source(self)

    def _update_all_sites(self):
        """update the self._sites dict"""
        cache_enabled = self._use_cache and cache
        if cache_enabled:
            self._sites = cache.get_sites_for_source(self)
        else:
            self._sites = waterml.get_sites_for_source(self)
        self._all_sites = True

    def __len__(self):
        len(self._sites)

    def within_shapefile(self, file_name, ):
        pass

    def within_polygon(self):
        pass

    def __repr__(self):
        return "<Source: %s>" % (self.url)


class TimeSeries(object):
    """
    Contains information about a time series
    """

    site = None
    variable = None
    count = None
    method = None
    quality_control_level = None
    begin_datetime = None
    end_datetime = None
    _series = ()
    _quantity = None
    _use_cache = None

    def __init__(self, variable=None, count=None, method=None,
                 quality_control_level=None, begin_datetime=None,
                 end_datetime=None, site=None, use_cache=True):
        self.variable = variable
        self.count = count
        self.method = method
        self.quality_control_level = quality_control_level
        self.begin_datetime = begin_datetime
        self.end_datetime = end_datetime
        self.site = site
        self._use_cache = use_cache

    @property
    def series(self):
        if not len(self._series):
            self._update_series()
        return self._series

    @property
    def quantity(self):
        if not self._quantity:
            self._update_series()
        return self._quantity

    def _update_series(self):
        cache_enabled = self._use_cache and cache
        if cache_enabled:
            self._series, self._quantity = \
                          cache.get_series_and_quantity_for_timeseries(self)
        else:
            self._series, self._quantity = \
                          waterml.get_series_and_quantity_for_timeseries(self)

    def __repr__(self):
        return "<TimeSeries: %s (%s - %s)>" % (
            self.variable.name, self.begin_datetime, self.end_datetime)


class Units(object):
    """
    Contains information about units of measurement
    """

    name = None
    abbreviation = None
    code = None

    def __init__(self, name=None, abbreviation=None, code=None):
        self.name = name
        self.abbreviation = abbreviation
        self.code = code

    def __repr__(self):
        return "<Units: %s [%s]>" % (self.name, self.abbreviation)


class Variable(object):
    """
    Contains information about a variable
    """

    name = None
    code = None
    id = None
    vocabulary = None
    units = None
    no_data_value = None

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
