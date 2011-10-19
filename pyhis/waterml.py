"""
    pyhis.waterml
    ~~~~~~~

    Extract data from waterml
"""
from datetime import datetime, timedelta
import logging
import warnings

import numpy as np
import pandas

import pyhis
from pyhis.exceptions import NoDataError

LOG_FORMAT = '%(message)s'
DISREGARD_TIMESERIES_DATE = True
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


#------------------------------------------------------------------------------
# waterml functions
#------------------------------------------------------------------------------
def get_sites_for_source(source):
    """
    return a sites dict for for a given source. The source can be
    either a string representing the url or a pyhis.Source object
    """
    log.info('making GetSites query...')
    get_sites_response = source.suds_client.service.GetSites('')

    log.info('processing %s sites...' % len(get_sites_response.site))
    site_list = [_site_from_wml_siteInfo(site.siteInfo, source)
                 for site in get_sites_response.site]

    return dict([(site.code, site) for site in site_list])


def get_description_for_source(source):
    """
    return string containg the source description for a given source.
    The source can be either a string representing the url or a
    pyhis.Source object
    """
    # Note: A source description isn't returned with the GetSites
    # response but rather is attached only to siteInfo responses and
    # timeseries responses...

    source_description = None

    log.info('looking up source description...')
    try:
        site_info = source.sites.values()[0]
        source_description = site_info.site[0].seriesCatalog[0].series[0].Source.SourceDescription
    except KeyError:
        warnings.warn('unable to determine source description')

    return source_description


def get_timeseries_dict_for_site(site):
    """
    returns a list of pyhis.TimeSeries objects for a given site and
    variable_code
    """
    try:
        series_response_list = site.site_info_response.site[0].seriesCatalog[0].series
    except AttributeError:
        #XXX: if seriesCatalog doesn't have any series... is this a
        #     bug?
        return {}

    timeseries_list = [_timeseries_from_wml_series(series, site)
                       for series in series_response_list]
    return dict([(timeseries.variable.code, timeseries)
                 for timeseries in timeseries_list])


def get_series_and_quantity_for_timeseries(timeseries, begin_date_str=None,
                                           end_date_str=None):
    """returns a tuple where the first element is a pandas.Series
    containing the timeseries data for the timeseries and the second
    element is the python quantity that corresponds the unit for the
    variable. Takes a suds WaterML TimeSeriesResponseType object.
    """
    suds_client = timeseries.site.source.suds_client
    log.info('making timeseries request for "%s:%s:%s (%s - %s)"...' %
                (timeseries.site.network, timeseries.site.code,
                 timeseries.variable.code,
                 begin_date_str, end_date_str))

    # workaround for USGS waterml reflection service hosted at sdsc is
    # returning timeseries begin date that is just a 31 days prior,
    # but USGS data goes back 120 days. Here we must disregard
    # timeseries date, acquire more data
    if not begin_date_str:
        if DISREGARD_TIMESERIES_DATE:
            begin_date_str = '1800-01-01'
        else:
            begin_date_str = timeseries.begin_datetime.strftime('%Y-%m-%d')
    if not end_date_str:
        end_date_str = (timeseries.end_datetime + timedelta(days=1))\
                       .strftime('%Y-%m-%d')

    timeseries_response = suds_client.service.GetValuesObject(
        '%s:%s' % (timeseries.site.network, timeseries.site.code),
        '%s:%s' % (timeseries.variable.vocabulary, timeseries.variable.code),
        begin_date_str,
        end_date_str)

    log.info('processing timeseries request for "%s:%s:%s (%s - %s)"...' %
                (timeseries.site.network, timeseries.site.code,
                 timeseries.variable.code,
                 begin_date_str, end_date_str))

    unit_code = getattr(timeseries_response.timeSeries.variable.units,
                        '_unitsCode', None)
    variable_code = timeseries_response.timeSeries.variable.variableCode[0].value

    # if unit code not in unit_quantities dict, then just use the value string
    try:
        quantity = pyhis.unit_quantities[unit_code]
    except KeyError:
        try:
            quantity = timeseries_response.timeSeries.variable.units.value
        except:
            quantity = 'UNKNOWN'
        warnings.warn("Unit conversion not available for %s: %s [%s]" %
                      (variable_code, quantity, unit_code))

    try:
        values = timeseries_response.timeSeries.values.value
        dates = np.array([value._dateTime for value in values])
        data = np.array([float(value.value) for value in values])
    except AttributeError:
        raise NoDataError(
            'No data values returned by service for "%s:%s:%s  (%s - %s)". '
            'This indicates either a bad date range, or it is possible that '
            ' the service could be misconfigured or broken.' %
            (timeseries.site.network, timeseries.site.code,
             timeseries.variable.code,
             begin_date_str, end_date_str))

    if len(dates) != len(data):
        raise ValueError("Number of dates does not match number of "
                         "data points.")

    if len(dates) != len(np.unique(dates)):
        unique_dates, unique_date_indices = np.unique(dates, return_index=True)
        duplicate_date_indices = np.setdiff1d(np.arange(len(dates)),
                                              unique_date_indices)
        duplicate_dates = dates[duplicate_date_indices]
        warnings.warn("Duplicate data found for variable '%s', only "
                      "the first value will be used. Date(s): %s" %
                      (variable_code, str(duplicate_dates)))
        dates = unique_dates
        data = data[unique_date_indices]

    series = pandas.Series(data, index=dates)
    return series, quantity


#------------------------------------------------------------------------------
# progress bar decorator
#------------------------------------------------------------------------------
def update_progress_bar(func):

    def wrapper(*args, **kwargs):
        if current_progress_bar and not current_progress_bar.finished:
            current_progress_bar.update(current_progress_bar.currval + 1)
        return func(*args, **kwargs)
    return wrapper


#------------------------------------------------------------------------------
# helper functions for parsing waterml responses into pyhis objects
#------------------------------------------------------------------------------
def _lat_long_from_geolocation(geolocation):
    """returns a tuple (lat, long) given a suds WaterML geolocation element"""
    if geolocation.geogLocation.__class__.__name__ == 'LatLonPointType':
        return (geolocation.geogLocation.latitude,
                geolocation.geogLocation.longitude)

    else:
        raise NotImplementedError(
            "Don't know how to convert location type: '%s'" %
            geolocation.geogLocation.__class__.__name__)


def _site_from_wml_siteInfo(siteInfo, source):
    """returns a PyHIS Site instance from a suds WaterML siteInfo element"""
    if not getattr(siteInfo, 'siteCode', None):
        # if siteInfo doesn't have a siteCode something is horribly wrong...
        raise ('siteInfo response does not contain a siteCode')

    if len(siteInfo.siteCode) > 1:
        raise NotImplementedError(
            "Multiple site codes not currently supported")

    site_code = siteInfo.siteCode[0]
    geolocation = getattr(siteInfo, 'geoLocation', None)
    if geolocation:
        latitude, longitude = _lat_long_from_geolocation(geolocation)

    return pyhis.Site(
        name=siteInfo.siteName,
        code=site_code.value,
        id=getattr(site_code, '_siteID', None),
        network=site_code._network,
        latitude=latitude,
        longitude=longitude,
        source=source,
        use_cache=source._use_cache)


def _variable_from_wml_variableInfo(variable_info):
    """returns a PyHIS Variable instance from a suds WaterML variableInfo
    element"""
    if len(variable_info.variableCode) > 1:
        raise NotImplementedError(
            "Multiple variable codes not currently supported")

    id = getattr(variable_info.variableCode[0], '_variableID', None)
    no_data_value = getattr(variable_info, 'NoDataValue', None)

    variable_info_units = getattr(variable_info, "units", None)
    if variable_info_units:
        units = _units_from_wml_units(variable_info_units)
    else:
        units = None

    return pyhis.Variable(
        name=variable_info.variableName,
        code=variable_info.variableCode[0].value,
        id=id,
        vocabulary=variable_info.variableCode[0]._vocabulary,
        units=units,
        no_data_value=no_data_value)


def _timeseries_from_wml_series(series, site):
    """returns a PyHIS series instance from a suds WaterML series element"""
    datetime_fmt = "%Y-%d-%m %H:%M:%S"

    # try to get series.Method.MethodDescription
    method = getattr(getattr(series, 'Method', None),
                     'MethodDescription', None)
    quality_control_level = getattr(series.QualityControlLevel,
                                    '_QualityControlLevelID', None)

    return pyhis.TimeSeries(
        variable=_variable_from_wml_variableInfo(series.variable),
        value_count=series.valueCount,
        method=method,
        quality_control_level=quality_control_level,
        begin_datetime=series.variableTimeInterval.beginDateTime,
        end_datetime=series.variableTimeInterval.endDateTime,
        site=site,
        use_cache=site._use_cache)


def _units_from_wml_units(units):
    """returns a PyHIS Units instance from a suds WaterML units element"""
    try:
        abbreviation=units._unitsAbbreviation
    except AttributeError:
        abbreviation=''
    return pyhis.Units(
        name=units.value,
        abbreviation=abbreviation,
        code=units._unitsCode)
