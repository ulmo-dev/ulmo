"""
    PyHIS.core
    ~~~~~~~~~~

    Core data models for PyHIS
"""
import itertools
import logging
import warnings

import numpy as np
from matplotlib.nxutils import points_inside_poly
import pandas
import suds

from . import waterml
from . import shapefile

# default timeout for http requests in seconds
SUDS_TIMEOUT = 600  # 10 minutes

# fancy this up a bit sometime
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)

try:
    from . import cache
    if not cache.USE_CACHE:
        log.info('cache has been disabled, so it will not be available')
        cache = None
except ImportError as error:
    log.info('cache not available due to import error:\n%s' % error)
    cache = None

__all__ = ['Site', 'Service', 'TimeSeries', 'Variable', 'Units']


class Site(object):
    """Contains information about a site"""
    _timeseries_dict = {}
    _dataframe = None
    _site_info_response = None
    _use_cache = None
    service = None
    name = None
    code = None
    id = None
    network = None
    latitude = None
    longitude = None

    def __init__(self, network=None, code=None, name=None, id=None,
                 latitude=None, longitude=None, service=None, use_cache=True):
        self.network = network
        self.code = code
        self.name = name
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.service = service
        self._use_cache = use_cache

        # if we don't have all the info, make a GetSiteInfo request
        # and update site attributes with that information
        if not name or not latitude or not longitude:
            site_info = self.site_info_response.site[0].siteInfo

            if not self.name:
                self.name = site_info.siteName
            if not self.id:
                try:
                    self.id = site_info.siteCode[0]._siteID
                except AttributeError, KeyError:
                    # siteID is optional
                    pass
            if not self.latitude:
                self.latitude = site_info.geoLocation.geogLocation.latitude
            if not self.longitude:
                self.longitude = site_info.geoLocation.geogLocation.longitude

    @property
    def dataframe(self):
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
        log.info('making GetSiteInfo request for "%s:%s"...' %
                 (self.network, self.code))
        self._site_info_response = self.service.suds_client.service.GetSiteInfoObject(
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


class Service(object):
    """Represents a water data service"""
    suds_client = None
    url = None
    default_network = None
    _description = None
    _all_sites = False
    _sites = {}
    _sites_array = []
    _use_cache = None

    def __init__(self, wsdl_url, network=None, description=None,
                 use_cache=True):
        self.suds_client = suds.client.Client(wsdl_url, timeout=SUDS_TIMEOUT)
        self.url = wsdl_url
        self.default_network = network
        self._description = description
        self._use_cache = use_cache

    @property
    def sites(self):
        return self.get_all_sites()

    @property
    def sites_array(self):
        return self.generate_sites_array()

    @property
    def description(self):
        if not self._description:
            self._update_description()
        return self._description

    def get_all_sites(self):
        """returns all the sites available for a given service"""
        if not self._all_sites:
            self._update_all_sites()
        return self._sites

    def generate_sites_array(self):
        """generates numpy array of locations of all sites
        for convenient spatial queries"""
        if not len(self._sites_array):
            self._sites_array = np.zeros(
                len(self.sites), dtype=[('sitecode', '|S100'),
                                        ('longitude', '>f8'),
                                        ('latitude', '>f8')])
            idx = 0
            for code, site in self.sites.iteritems():
                self._sites_array['sitecode'][idx] = code
                self._sites_array['latitude'][idx] = site.latitude
                self._sites_array['longitude'][idx] = site.longitude
                idx += 1

        return self._sites_array

    def get_site(self, site_code, network=None):
        """returns a single site"""
        if not network:
            network = self.default_network

        if (network, site_code) in self._sites:
            return self._sites[(network, site_code)]

        cache_enabled = self._use_cache and cache
        if cache_enabled:
            site = cache.get_site(self, network, site_code)
        else:
            site = Site(network=network, code=site_code, service=self)

        self._sites[(network, site_code)] = site
        return site

    def _update_description(self, force_waterml=False):
        """update self._description"""
        self._description = waterml.get_description_for_service(self)

    def _update_all_sites(self):
        """update the self._sites dict"""
        cache_enabled = self._use_cache and cache
        if cache_enabled:
            self._sites = cache.get_sites_for_service(self)
        else:
            self._sites = waterml.get_sites_for_service(self)
        self._all_sites = True

    def __len__(self):
        len(self._sites)

    def get_sites_within_shapefile(self, shapefile_path):
        """Returns the set of sites contained within the polygons of a
        shapefile. The shapefile is assumed to be in WGS84 coordinate
        system.
        """
        sf = shapefile.Reader(shapefile_path)
        shapes = sf.shapes()
        site_dicts = [self.get_sites_within_polygon(shape.points)
                      for shape in shapes]
        d = dict(itertools.chain(*[site_dict.items()
                                   for site_dict in site_dicts
                                   if site_dict]))

        #remove annoying usgs site for demo
        del d['08158819']

        return d

    def get_sites_within_radius_r(self, latitude, longitude,
                                  radius, npoints=100):
        """Generates circular poly, sends vertices to
        get_sites_within_polygon, returns subset of sites
        """
        print 'not implemented'

    def get_sites_within_polygon(self, verts):
        """returns dict of sites within polygon defined by verts
        """
        self.generate_sites_array()
        points = np.vstack((self.sites_array['longitude'],
                            self.sites_array['latitude'])).T
        idx = points_inside_poly(points, verts)
        return dict([(sitecode, self.sites[sitecode])
                     for sitecode in self.sites_array['sitecode'][idx]])

    def __repr__(self):
        return "<Service: %s>" % (self.url)


class Source(Service):
    def __init__(self, *args, **kwargs):
        warnings.warn("pyhis.core.Source is being deprecated. Use pyhis.core.Service instead")
        super(Source, self).__init__(*args, **kwargs)


class TimeSeries(object):
    """Contains information about a time series"""

    site = None
    variable = None
    value_count = None
    method = None
    quality_control_level = None
    begin_datetime = None
    end_datetime = None
    _series = ()
    _quantity = None
    _use_cache = None

    def __init__(self, variable=None, value_count=None, method=None,
                 quality_control_level=None, begin_datetime=None,
                 end_datetime=None, site=None, use_cache=True):
        self.variable = variable
        self.value_count = value_count
        self.method = method
        self.quality_control_level = quality_control_level
        self.begin_datetime = begin_datetime
        self.end_datetime = end_datetime
        self.site = site
        self._use_cache = use_cache

    @property
    def series(self):
        warnings.warn("timeseries.series is being deprecated. Use timeseries.data instead")
        return self.data

    @property
    def data(self):
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
    """Contains information about units of measurement"""

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
    """Contains information about a variable"""

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
