"""
    PyHIS.core
    ~~~~~~~~~~

    Core data models for PyHIS
"""

import itertools

import numpy as np
import pandas
import shapely
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


class Site(object):
    """
    Contains information about a site
    """
    _timeseries_list = ()
    _dataframe = None
    _site_info = None
    _use_cache = None
    source = None
    name = None
    code = None
    id = None
    network = None
    location = None

    def __init__(self, code=None, name=None, id=None, network=None,
                 latitude=None, longitude=None, source=None, use_cache=True):
        self.code = code
        self.name = name
        self.id = id
        self.network = network
        self.location = shapely.geometry.Point(float(longitude), float(latitude))
        self.source = source
        self._use_cache = use_cache

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    @property
    def dataframe(self):
        if not self._timeseries_list:
            self._update_site_info()
        if not self._dataframe:
            self._update_dataframe()
        return self._dataframe

    @property
    def site_info(self):
        if not self._site_info:
            self._update_site_info()
        return self._site_info

    @property
    def timeseries_list(self):
        if not len(self._timeseries_list):
            self._update_timeseries_list()
        return self._timeseries_list

    @property
    def variables(self):
        return [series.variable for series in self.timeseries_list]

    def _update_dataframe(self):
        ts_dict = dict((ts.variable.code, ts.series)
                       for ts in self.timeseries_list)
        self._dataframe = pandas.DataFrame(ts_dict)

    def _update_site_info(self):
        """makes a GetSiteInfo updates site info and series information"""
        self._site_info = self.source.suds_client.service.GetSiteInfoObject(
            '%s:%s' % (self.network, self.code))

        if len(self._site_info.site) > 1 or \
               len(self._site_info.site[0].seriesCatalog) > 1:
            raise NotImplementedError(
                "Multiple site instances or multiple seriesCatalogs not "
                "currently supported")

    def _update_timeseries_list(self):
        """updates the time series list"""
        cache_enabled = self._use_cache and cache

        if cache_enabled:
            self._timeseries_list = cache.get_timeseries_list_for_site(self)
        else:
            self._timeseries_list = waterml.get_timeseries_list_for_site(self)

    def __repr__(self):
        return "<Site: %s [%s]>" % (self.name, self.code)


class Source(object):
    """Represents a water data source"""
    suds_client = None
    url = None
    _sites = {}
    _use_cache = None

    def __init__(self, wsdl_url, use_cache=True):
        self.suds_client = suds.client.Client(wsdl_url)
        self.url = wsdl_url
        self._use_cache = use_cache

    @property
    def sites(self):
        if not self._sites:
            self._update_sites()
        return self._sites

    def _update_sites(self):
        """update the self._sites dict"""
        cache_enabled = self._use_cache and cache

        if cache_enabled:
            self._sites = cache.get_sites_for_source(self)
        else:
            self._sites = waterml.get_sites_for_source(self)

    def __len__(self):
        len(self._sites)

    def within_shapefile(self, file_name, ):
        

    def within_polygon(self):
        

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
