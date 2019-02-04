"""
    ulmo.nasa.daymet.core
    ~~~~~~~~~~~~~~

    This module provides direct access to `NASA EARTHDATA ORNL DAAC 
    Daymet`_ web services.


    .. .. _NASA EARTHDATA ORNL DAAC Daymet: https://daymet.ornl.gov/dataaccess.html

"""
from future import standard_library
standard_library.install_aliases()
from builtins import str
from past.builtins import basestring
import contextlib
import io
import datetime
import time
import logging

import requests
import pandas as pd

from ulmo import util

VARIABLES = {"tmax":"maximum temperature",
            "tmin":"minimum temperature",
            "srad":"shortwave radiation",
            "vp":"vapor pressure",
            "swe":"snow-water equivalent",
            "prcp":"precipitation",
            "dayl":"daylength"}
MIN_YEAR = 1980
MAX_Year = int(time.strftime("%Y"))-1
MIN_LAT = 14.5
MAX_LAT = 52.0
MIN_LON = -131.0
MAX_LON = -53.0


DAYMET_SINGLEPIXEL_URL = "https://daymet.ornl.gov/data/send/saveData?lat={lat}&lon={lon}&measuredParams={vars}"

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_variables():
    """retrieve a list of variables available

    Parameters
    ----------
    None

    Returns
    -------
        dictionary of variables with variable abreviations as keys 
        and description as values
    """
    return VARIABLES

def get_daymet_singlepixel(latitude, longitude, 
                           variables=['tmax', 'tmin', 'prcp'], years=None,
                           as_dataframe=True):
    """Fetches a time series of climate variables from the DAYMET single pixel extraction


    Parameters
    ----------
    latitude: float
        The latitude (WGS84), value between 52.0 and 14.5.
    longitude: float
        The longitude (WGS84), value between -131.0 and -53.0.
    variables : List of str
        Daymet parameters to fetch. 
        Available options:
            ``tmax`` - maximum temperature
            ``tmin`` - minimum temperature
            ``srad`` - shortwave radiation
            ``vp`` - vapor pressure
            ``swe`` - snow-water equivalent
            ``prcp`` - precipitation
            ``dayl`` - daylength
        default = ['tmax', 'tmin', 'prcp']
    years: list of int
        List of years to return. 
        Daymet version 2 available 1980 to the latest full calendar year.
        If ``None`` (default), all years will be returned
    as_dataframe : ``True`` (default) or ``False``
        if ``True`` return pandas dataframe
        if ``False`` return open file with contents in csv format

    
    Returns
    -------
    single_pixel_timeseries : pandas dataframe or csv filename
    """
    _check_coordinates(latitude, longitude)
    _check_variables(variables)
    if not years is None:
        _check_years(years)

    url_params = {'lat': latitude,
                  'lon': longitude,
                  'vars': _as_str(variables)}
    if years:
        url_params['years'] = _as_str(years)

    url = _get_service_url(url_params)
    log.info("making request for latitude, longitude: {}, {}".format(latitude, longitude))
    df = pd.read_csv(url, header=6)
    df.year, df.yday = df.year.astype('int'), df.yday.astype('int')
    df.index = pd.to_datetime(df.year.astype('str') + '-' + df.yday.astype('str'), format="%Y-%j")
    df.columns = [c[:c.index('(')].strip() if '(' in c else c for c in df.columns ]
    if as_dataframe:
        return df
    else:
        results = {}
        for key in df.columns:
            if key not in ['yday', 'year']:
                results[key] = dict(zip(df[key].index.format(), df[key]))
        return results

def _check_variables(variables):
    """make sure all variables are in list
    """
    bad_variables = [v for v in variables if v not in VARIABLES.keys()]
    if bad_variables:
        
        raise ValueError("the variable(s) provided ('{}') not\none of available options: '{}'".format(
            "', '".join(bad_variables), str(VARIABLES.keys())[2:-2]))

def _check_years(years):
    """make sure all years are in available year range
    """
    bad_years = [str(year) for year in years if not MIN_YEAR <= year <= MAX_Year]
    if bad_years:
        raise ValueError("the year(s) provided ({}) \nnot in available timerange ({}-{})".format(
            ", ".join(bad_years), MIN_YEAR, MAX_Year))

def _check_coordinates(lat, lon):
    """make sure the passed coordinates are in the available data range
    """
    bad_lat = not MIN_LAT <= lat <= MAX_LAT
    bad_lon = not MIN_LON <= lon <= MAX_LON
    
    if bad_lat or bad_lon:
        err_msg = "The specified latitude, longitude pair ({}, {})".format(lat, lon)
        err_msg += "\nis not in the available range of data:\n"
        err_msg += "\tLatitude = [{} - {}]".format(MIN_LAT, MAX_LAT)
        err_msg += "\n\tLongitude = [{} - {}]".format(MIN_LON, MAX_LON)
        raise ValueError(err_msg)

def _as_str(arg):
    """if arg is a list, convert to comma delimited string
    """
    if isinstance(arg, basestring):
        return arg
    else:
        return ','.join([str(a) for a in arg])

def _get_service_url(url_params):
    """return formatted url
    """
    url = DAYMET_SINGLEPIXEL_URL.format(**url_params)

    if 'years' in url_params:
        url += "&year={}".format(url_params['years'])
    return url