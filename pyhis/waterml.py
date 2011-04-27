"""
    pyhis.waterml
    ~~~~~~~

    Extract data from waterml
"""
from datetime import datetime
import warnings

import numpy as np
import pandas

import pyhis


#------------------------------------------------------------------------------
# waterml functions
#------------------------------------------------------------------------------
def get_sites_for_source(source):
    """
    return a sites dict for for a given source.  The source can be
    either a string representing the url or a pyhis.Source object
    """
    get_all_sites_query = source.suds_client.service.GetSites('')
    site_list = [_site_from_wml_siteInfo(site, source)
                 for site in get_all_sites_query.site]
    return dict([(site.code, site) for site in site_list])


def get_timeseries_list_for_site(site):
    """
    returns a list of pyhis.TimeSeries objects for a given site and
    variable_code
    """
    series_response_list = site.site_info.site[0].seriesCatalog[0].series
    timeseries_list = [_timeseries_from_wml_series(series, site)
                       for series in series_response_list]
    return timeseries_list


def get_series_and_quantity_for_timeseries(timeseries):
    """returns a tuple where the first element is a pandas.Series
    containing the timeseries data for the timeseries and the second
    element is the python quantity that corresponds the unit for the
    variable. Takes a suds WaterML TimeSeriesResponseType object.
    """
    suds_client = timeseries.site.source.suds_client
    timeseries_response = suds_client.service.GetValuesObject(
        '%s:%s' % (timeseries.site.network, timeseries.site.code),
        '%s:%s' % (timeseries.variable.vocabulary, timeseries.variable.code),
        timeseries.begin_datetime.strftime('%Y-%m-%d'),
        timeseries.end_datetime.strftime('%Y-%m-%d'))

    unit_code = timeseries_response.timeSeries.variable.units._unitsCode
    variable_code = timeseries_response.timeSeries.variable.variableCode[0].value

    # if unit code not in unit_quantities dict, then just use the value string
    try:
        quantity = pyhis.unit_quantities[unit_code]
    except KeyError:
        quantity = timeseries_response.timeSeries.variable.units.value
        warnings.warn("Unit conversion not available for %s: %s [%s]" %
                      (variable_code, quantity, unit_code))

    values = timeseries_response.timeSeries.values.value
    dates = np.array([value._dateTime for value in values])
    data = np.array([float(value.value) for value in values])

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


def _site_from_wml_siteInfo(site, source):
    """returns a PyHIS Site instance from a suds WaterML siteInfo element"""
    if len(site.siteInfo.siteCode) > 1:
        raise NotImplementedError(
            "Multiple site codes not currently supported")

    site_code = site.siteInfo.siteCode[0]
    geolocation = getattr(site.siteInfo, 'geoLocation', None)
    if geolocation:
        latitude, longitude = _lat_long_from_geolocation(geolocation)

    return pyhis.Site(
        name=site.siteInfo.siteName,
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

    return pyhis.Variable(
        name=variable_info.variableName,
        code=variable_info.variableCode[0].value,
        id=variable_info.variableCode[0]._variableID,
        vocabulary=variable_info.variableCode[0]._vocabulary,
        units=_units_from_wml_units(variable_info.units),
        no_data_value=variable_info.NoDataValue)


def _timeseries_from_wml_series(series, site):
    """returns a PyHIS series instance from a suds WaterML series element"""
    datetime_fmt = "%Y-%d-%m %H:%M:%S"

    return pyhis.TimeSeries(
        variable=_variable_from_wml_variableInfo(series.variable),
        count=series.valueCount,
        method=series.Method.MethodDescription,
        quality_control_level=series.QualityControlLevel._QualityControlLevelID,
        begin_datetime=series.variableTimeInterval.beginDateTime,
        end_datetime=series.variableTimeInterval.endDateTime,
        site=site,
        use_cache=site._use_cache)


def _units_from_wml_units(units):
    """returns a PyHIS Units instance from a suds WaterML units element"""
    return pyhis.Units(
        name=units.value,
        abbreviation=units._unitsAbbreviation,
        code=units._unitsCode)
