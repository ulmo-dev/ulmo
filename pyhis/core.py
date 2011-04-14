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

import util

__all__ = ['Site', 'Source', 'TimeSeries', 'Variable', 'Units']


class Site(object):
    """
    Contains information about a site
    """
    _timeseries_list = None
    _dataframe = None
    _site_info = None
    _client = None

    name = None
    code = None
    id = None
    network = None
    location = None

    def __init__(self, name=None, code=None, id=None, network=None,
                 location=None, client=None):
        self.name = name
        self.code = code
        self.id = id
        self.network = network
        if location:
            self.location = util._shapely_geometry_from_geolocation(location)
        self._client = client

    @property
    def dataframe(self):
        if not self._timeseries_list:
            self._update_site_info()
        if not self._dataframe:
            self._update_dataframe()
        return self._dataframe

    # @property
    # def data(self):
    #     if not self._timeseries_list:
    #         self._update_site_info()
    #     if not self._dataframe:
    #         self._update_dataframe()
    #     return self._dataframe

    # @property
    # def dates(self):
    #     """"""

    #     if not self._timeseries_list:
    #         self._update_site_info()
    #     if not self._dataframe:
    #         self._update_dataframe()
    #     return 0

    @property
    def site_info(self):
        if not self._site_info:
            self._update_site_info()
        return self._site_info

    @property
    def variables(self):
        if not self._timeseries_list:
            self._update_site_info()
        return [series.variable for series in self._timeseries_list]

    @property
    def variables(self):
        if not self._timeseries_list:
            self._update_site_info()
        return [series.variable for series in self._timeseries_list]

    def _update_dataframe(self):
        ts_dict = dict((ts.variable.code, ts.series)
                       for ts in self._timeseries_list)
        self._dataframe = pandas.DataFrame(ts_dict)

    def _update_site_info(self):
        """makes a GetSiteInfo updates site info and series information"""
        self._site_info = self._client.suds_client.service.GetSiteInfoObject(
            '%s:%s' % (self.network, self.code))

        if len(self._site_info.site) > 1 or \
               len(self._site_info.site[0].seriesCatalog) > 1:
            raise NotImplementedError(
                "Multiple site instances or multiple seriesCatalogs not "
                "currently supported")

        series_list = self._site_info.site[0].seriesCatalog[0].series
        self._timeseries_list = [util._timeseries_from_wml_series(series,
                                                                      self)
                                 for series in series_list]

    def __repr__(self):
        return '<Site: %s [%s]>' % (self.name, self.code)


class Source(object):
    """Represents a water data source"""
    suds_client = None

    def __init__(self, wsdl_url):
        self.suds_client = suds.client.Client(wsdl_url)

        get_all_sites_query = self.suds_client.service.GetSites('')
        self.sites = [util._site_from_wml_siteInfo(site, self)
                      for site in get_all_sites_query.site]


class TimeSeries(object):
    """
    Contains information about a time series
    """

    site = None
    _series = ()
    _quantity = None

    def __init__(self, variable=None, count=None, method=None,
                 quality_control_level=None, begin_datetime=None,
                 end_datetime=None, site=None):
        self.variable = variable
        self.count = count
        self.method = method
        self.quality_control_level = quality_control_level
        self.begin_datetime = begin_datetime
        self.end_datetime = end_datetime
        self.site = site

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
        suds_client = self.site._client.suds_client
        timeseries_resp = suds_client.service.GetValuesObject(
            '%s:%s' % (self.site.network, self.site.code),
            '%s:%s' % (self.variable.vocabulary, self.variable.code),
            self.begin_datetime.strftime('%Y-%m-%d'),
            self.end_datetime.strftime('%Y-%m-%d'))
        self._series, self._quantity = \
                     util._pandas_series_from_wml_TimeSeriesResponseType(timeseries_resp)

    def __repr__(self):
        return "<TimeSeries: %s (%s - %s)>" % (
            self.variable.name, self.begin_datetime, self.end_datetime)


class Variable(object):
    """
    Contains information about a variable
    """

    _series = None

    def __init__(self, name=None, code=None, id=None, vocabulary=None,
                 units=None, no_data_value=None, series=None):
        self.name = name
        self.code = code
        self.id = id
        self.vocabulary = vocabulary
        self.units = units
        self.no_data_value = no_data_value
        self._series = None

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
