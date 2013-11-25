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

import os
import sys
from datetime import datetime
import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import re

from ulmo import util

DEFAULT_START_DATE = '01/01/1901'
DEFAULT_END_DATE   = 'Now'

#SENSOR_NUM = [    5,   20,   41,  100]
#SENSOR_NAM = ['SalinityA','DischargeA','MeanDailyDischarge','SalinityB']

def get_stations():
        # I haven't found a better list of stations, seems pretty janky 
        # to just have them in a file, and not sure if/when it is updated.
    url = 'http://cdec.water.ca.gov/misc/all_stations.csv'
        # the csv is malformed, so some rows think there are 7 fields 
    col_names = ['id','meta_url','name','num','lat','lon','junk']
    df = pd.read_csv(url, names=col_names, header=None, quotechar="'",index_col=0)

    return df

def get_sensors(sensor_id=None):
    """
    Returns a list of sensor ids as a DataFrame indexed on sensor 
    number. Can be limited by a list of numbers. 
    """

    url = 'http://cdec.water.ca.gov/misc/senslist.html'
    df = pd.read_html(url,infer_types=False,header=0,index_col=0)[0]

    if sensor_id is None:
        return df
    else:
        return df.ix[sensor_id]

def get_station_sensors(station_ids=None, sensor_ids=None, resolutions=None):

    station_sensors = {}

    if station_ids is None:
        station_ids = get_stations().index

    for station_id in station_ids:
        url = 'http://cdec.water.ca.gov/cgi-progs/queryCSV?station_id=%s' % (station_id)

        sensor_list = pd.read_html(url)[0]
        sensor_list.columns = ['sensor_id','variable','resolution','timerange']
        v = sensor_list.variable.to_dict().values()

        split = [re.split(r'[\(\)]+',x) for x in v]
        var_names = [x[0] for x in split]
        units = [x[1] for x in split]
        var_resolution = [re.split(r'[\(\)]+',x)[1] for x in sensor_list.resolution]
        
        sensor_list['resolution'] = var_resolution
        sensor_list['variable'] = [x+y for x,y in zip(var_names,var_resolution)]
        sensor_list['units'] = pd.Series(units,index=sensor_list.index)

        station_sensors[station_id] = _limit_sensor_list(sensor_list, sensor_ids, resolutions)

    return station_sensors

def _limit_sensor_list(sensor_list, sensor_ids, resolution):

    if sensor_ids is not None:
        sensor_list = sensor_list[[x in sensor_ids for x in sensor_list.sensor_id]]

    if resolution is not None:
        sensor_list = sensor_list[[x in resolution for x in sensor_list.resolution]]

    return sensor_list


def get_data(station_ids=None, sensor_ids=None, resolutions=None):
    """
    Downloads data for a set of CDEC station and sensor ids. If either is not provided, 
    all available data will be downloaded. Be really careful with choosing hourly  
    resolution as the data sets are big, and CDEC's servers are slow as molasses 
    in winter.
    """

    if station_ids is None:
        station_ids = get_stations().index

    sensors = get_station_sensors(station_ids, sensor_ids, resolutions)

    d = {}

    for station_id, sensor_list in sensors.items():
        station_data = {}
        
        for index, row in sensor_list.iterrows():
            res = row.ix['resolution']
            var = row.ix['variable']
            sensor_id =  row.ix['sensor_id']
            station_data[var] = download_raw(station_id, sensor_id, _res_to_dur_code(res))

        d[station_id] = station_data

    return d

def download_raw(station_id, sensor_num, dur_code):
 
    url = 'http://cdec.water.ca.gov/cgi-progs/queryCSV' + \
          '?station_id=' + station_id    + \
          '&dur_code='   + dur_code   + \
          '&sensor_num=' + str(sensor_num) + \
          '&start_date=' + DEFAULT_START_DATE + \
          '&end_date='   + DEFAULT_END_DATE   

    #tf = tempfile.mktemp()
    #urllib.urlretrieve(url, tf)

    df = pd.read_csv(url, skiprows=2, header=None, parse_dates=[[0,1]], index_col=None, na_values='m')
    df.columns = ['datetime', 'value']
    df.set_index('datetime', inplace=True)

    return df

def _res_to_dur_code(res):
    map = {
        'hourly':'H',
        'daily':'D',
        'monthly':'M',
        'event':'E'}

    return map[res]
