"""
    ulmo.cdec.historical.core
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `California Department
    of Water Resources`_ `California Data Exchange Center`_ web site.

    .. _California Department of Water Resources: http://www.water.ca.gov/
    .. _California Data Exchange Center: http://cdec.water.ca.gov


    SELECTED CDEC SENSOR NUMBERS (these are not be available for all sites):

    1    river stage [ft]
    2    precipitation, accumulated [in]
    3    SWE [in]
    4    air temperature [F]
    5    EC [ms/cm]
    6    reservoir elevation [ft]
    7    reservoir scheduled release [cfs]
    8    full natural flow [cfs]
    15   reservoir storage [af]
    20   flow -- river discharge [cfs]
    22   reservoir storage change [af]
    23   reservoir outflow [cfs]
    24   Evapotranspiration [in]
    25   water temperature [F]
    27   water turbidity [ntu]
    28   chlorophyll [ug/l]
    41   flow -- mean daily [cfs]
    45   precipitation, incremental [in]
    46   runoff volume [af]
    61   water dissolved oxygen [mg/l]
    62   water pH value [pH]
    64   pan evaporation (incremental) [in]
    65   full natural flow [af]
    66   flow -- monthly volume [af]
    67   accretions (estimated) [af]
    71   spillway discharge [cfs]
    74   lake evaporation (computed) [cfs]
    76   reservoir inflow [cfs]
    85   control regulating discharge [cfs]
    94   top conservation storage (reservoir) [af]
    100  water EC [us/cm]

    CDEC DURATION CODES:

    E    event
    H    hourly
    D    daily
    M    monthly

"""
from builtins import str
from builtins import zip

import pandas as pd
import re

from ulmo import util

DEFAULT_START_DATE = '01/01/1901'
DEFAULT_END_DATE = 'Now'


def get_stations():
    """Fetches information on all CDEC sites.

    Returns
    -------
    df : pandas DataFrame
        a pandas DataFrame (indexed on site id) with station information.
    """
        # I haven't found a better list of stations, seems pretty janky
        # to just have them in a file, and not sure if/when it is updated.
    url = 'http://cdec.water.ca.gov/misc/all_stations.csv'
        # the csv is malformed, so some rows think there are 7 fields
    col_names = ['id','meta_url','name','num','lat','lon','junk']
    df = pd.read_csv(url, names=col_names, header=None, quotechar="'",index_col=0)

    return df


def get_sensors(sensor_id=None):
    """
    Gets a list of sensor ids as a DataFrame indexed on sensor
    number. Can be limited by a list of numbers.

    Usage example::

        from ulmo import cdec
        # to get all available sensor info
        sensors = cdec.historical.get_sensors()
        # or to get just one sensor
        sensor = cdec.historical.get_sensors([1])

    Parameters
    ----------
    sites : iterable of integers or ``None``

    Returns
    -------
    df : pandas DataFrame
        a python dict with site codes mapped to site information
    """

    url = 'http://cdec.water.ca.gov/misc/senslist.html'
    df = pd.read_html(url, header=0)[0]
    df.set_index('Sensor No')

    if sensor_id is None:
        return df
    else:
        return df.loc[sensor_id]


def get_station_sensors(station_ids=None, sensor_ids=None, resolutions=None):
    """
    Gets available sensors for the given stations, sensor ids and time
    resolutions. If no station ids are provided, all available stations will
    be used (this is not recommended, and will probably take a really long
    time).

    The list can be limited by a list of sensor numbers, or time resolutions
    if you already know what you want. If none of the provided sensors or
    resolutions are available, an empty DataFrame will be returned for that
    station.

    Usage example::

        from ulmo import cdec
        # to get all available sensors
        available_sensors = cdec.historical.get_station_sensors(['NEW'])


    Parameters
    ----------
    station_ids : iterable of strings or ``None``

    sensor_ids : iterable of integers or ``None``
        check out  or use the ``get_sensors()`` function to see a list of
        available sensor numbers

    resolutions : iterable of strings or ``None``
        Possible values are 'event', 'hourly', 'daily', and 'monthly' but not
        all of these time resolutions are available at every station.


    Returns
    -------
    dict : a python dict
        a python dict with site codes as keys with values containing pandas
        DataFrames of available sensor numbers and metadata.
    """
    # PRA&SensorNums=76&dur_code=H&Start=2019-02-02&End=2019-02-04
    station_sensors = {}

    if station_ids is None:
        station_ids = get_stations().index

    for station_id in station_ids:
        url = 'http://cdec.water.ca.gov/dynamicapp/staMeta?station_id=%s' % (station_id)

        try:
            sensor_list = pd.read_html(url, match='Sensor Description')[0]
        except:
            sensor_list = pd.read_html(url)[0]
    
        try:
            sensor_list.columns = ['sensor_id', 'variable', 'resolution','timerange']
        except:
            sensor_list.columns = ['variable', 'sensor_id', 'resolution', 'varcode', 'method', 'timerange']
        sensor_list[['variable', 'units']] = sensor_list.variable.str.split(',', 1, expand=True)
        sensor_list.resolution = sensor_list.resolution.str.strip('()')
        
        station_sensors[station_id] = _limit_sensor_list(sensor_list, sensor_ids, resolutions)

    return station_sensors


def get_data(station_ids=None, sensor_ids=None, resolutions=None, start=None, end=None):
    """
    Downloads data for a set of CDEC station and sensor ids. If either is not
    provided, all available data will be downloaded. Be really careful with
    choosing hourly resolution as the data sets are big, and CDEC's servers
    are slow as molasses in winter.


    Usage example::

        from ulmo import cdec
        dat = cdec.historical.get_data(['PRA'],resolutions=['daily'])

    Parameters
    ----------
    station_ids : iterable of strings or ``None``

    sensor_ids : iterable of integers or ``None``
        check out  or use the ``get_sensors()`` function to see a list of
        available sensor numbers

    resolutions : iterable of strings or ``None``
        Possible values are 'event', 'hourly', 'daily', and 'monthly' but not
        all of these time resolutions are available at every station.


    Returns
    -------
    dict : a python dict
        a python dict with site codes as keys. Values will be nested dicts
        containing all of the sensor/resolution combinations.
    """

    if start is None:
        start_date = util.convert_date(DEFAULT_START_DATE)
    else:
        start_date = util.convert_date(start)
    if end is None:
        end_date = util.convert_date(DEFAULT_END_DATE)
    else:
        end_date = util.convert_date(end)

    start_date_str = _format_date(start_date)
    end_date_str = _format_date(end_date)

    if station_ids is None:
        station_ids = get_stations().index

    sensors = get_station_sensors(station_ids, sensor_ids, resolutions)

    d = {}

    for station_id, sensor_list in list(sensors.items()):
        station_data = {}

        for index, row in sensor_list.iterrows():
            res = row.loc['resolution']
            var = row.loc['variable']
            sensor_id = row.loc['sensor_id']
            station_data[var] = _download_raw(station_id, sensor_id, _res_to_dur_code(res), start_date_str, end_date_str)
        d[station_id] = station_data

    return d


def _limit_sensor_list(sensor_list, sensor_ids, resolution):

    if sensor_ids is not None:
        sensor_list = sensor_list[[x in sensor_ids for x in sensor_list.sensor_id]]

    if resolution is not None:
        sensor_list = sensor_list[[x in resolution for x in sensor_list.resolution]]

    return sensor_list


def _download_raw(station_id, sensor_num, dur_code, start_date, end_date):

    url = 'http://cdec.water.ca.gov/dynamicapp/req/CSVDataServlet' + \
          '?Stations=' + station_id + \
          '&dur_code=' + dur_code + \
          '&SensorNums=' + str(sensor_num) + \
          '&Start=' + start_date + \
          '&End=' + end_date

    df = pd.read_csv(url, parse_dates=[4,5], index_col='DATE TIME', na_values='---')
    df.columns = ['station_id', 'duration', 'sensor_number', 'sensor_type', 'obs_date', 'value', 'data_flag', 'units']

    return df


def _res_to_dur_code(res):
    map = {
        'hourly':'H',
        'daily':'D',
        'monthly':'M',
        'event':'E'}

    return map[res]


def _format_date(date):
    return '%s/%s/%s' % (date.month, date.day, date.year)
