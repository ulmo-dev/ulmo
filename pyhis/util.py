"""
    pyhis.util
    ~~~~~~~

    Set of utility functions that help pyhis do its thing.

"""
from datetime import datetime

from shapely.geometry import Point, Polygon

import pyhis


def _get_shapely_from_geolocation(geolocation):
    """returns a shapely object given a suds WaterML geolocation element"""

    if geolocation.geogLocation.__class__.__name__ == 'LatLonPointType':
        return Point(geolocation.geogLocation.longitude,
                     geolocation.geogLocation.latitude)

    else:
        raise NotImplementedError(
            "Don't know how to convert location type: '%s'" %
            geolocation.geogLocation.__class__.__name__)


def _get_site_from_site_info(site, suds_client):
    """returns a PyHIS Site instance from a suds WaterML siteInfo element"""
    if len(site.siteInfo.siteCode) > 1:
        raise NotImplementedError(
            "Multiple site codes not currently supported")

    site_code = site.siteInfo.siteCode[0]

    return pyhis.Site(
        name=site.siteInfo.siteName,
        code=site_code.value,
        id=site_code._siteID,
        network=site_code._network,
        location=site.siteInfo.geoLocation,
        suds_client=suds_client)


def _get_variable_from_variable_info(variable_info):
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
        units=_get_units_from_waterml(variable_info.units),
        no_data_value=variable_info.NoDataValue)


def _get_units_from_waterml(units):
    """returns a PyHIS Units instance from a suds WaterML units element"""
    return pyhis.Units(
        name=units.value,
        abbreviation=units._unitsAbbreviation,
        code=units._unitsCode)


def _get_series_from_waterml(series):
    """returns a PyHIS series instance from a suds WaterML series element"""
    datetime_fmt = "%Y-%d-%m %H:%M:%S"

    return pyhis.Series(
        variable=_get_variable_from_variable_info(series.variable),
        count=series.valueCount,
        method=series.Method.MethodDescription,
        quality_control_level=series.QualityControlLevel._QualityControlLevelID,
        begin_datetime=series.variableTimeInterval.beginDateTime,
        end_datetime=series.variableTimeInterval.endDateTime)
