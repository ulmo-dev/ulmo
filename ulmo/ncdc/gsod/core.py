"""
    ulmo.ncdc.gsod.core
    ~~~~~~~~~~~~~~~~~~~

    This module provides direct access to `National Climatic Data Center`_
    `Global Summary of the Day`_ dataset.

    .. _National Climatic Data Center: http://www.ncdc.noaa.gov
    .. _Global Summary of the Day: http://www.ncdc.noaa.gov/oa/gsod.html
"""
from builtins import str
from builtins import range
from past.builtins import basestring
from contextlib import contextmanager
import csv
import datetime
import gzip
import itertools
import os
import tarfile

import numpy as np

from ulmo import util

NCDC_GSOD_DIR = os.path.join(util.get_ulmo_dir(), 'ncdc/gsod')
NCDC_GSOD_STATIONS_FILE = os.path.join(NCDC_GSOD_DIR, 'isd-history.csv')
NCDC_GSOD_START_DATE = datetime.date(1929, 1, 1)

def get_parameters():
    """
    retrieve a list of parameter codes available.
    Reference for GSOD parameters : https://www1.ncdc.noaa.gov/pub/data/gsod/readme.txt

    Parameters
    ----------
        None

    Returns
    -------
        dictionary of variables with parameter codes as keys
        and GSOD codes as values.
    """

    VARIABLES = {'mean_temp' : 'TEMP',
                'mean_temp_count' : 'TEMP',
                'dew_point' : 'DEWP',
                'dew_point_count' : 'DEWP',
                'sea_level_pressure' : 'SLP     ',
                'sea_level_pressure_count' : 'SLP     ',
                'station_pressure' : 'STP',
                'station_pressure_count' : 'STP',
                'visibility' : 'VISIB',
                'visibility_count' : 'VISIB',
                'mean_wind_speed' : 'WDSP',
                'mean_wind_speed_count' : 'WDSP',
                'max_wind_speed' : 'MXSPD',
                'max_gust' : 'GUST',
                'max_temp' : 'MAX',
                'max_temp_flag' : 'MAX',
                'min_temp' : 'MIN',
                'min_temp_flag' : 'MIN',
                'precip' : 'PRCP',
                'precip_flag' : 'PRCP',
                'snow_depth' : 'SNDP',
                'FRSHTT' : 'FRSHTT'}
    return VARIABLES

def get_data(station_codes, start=None, end=None, parameters=None):
    """Retrieves data for a set of stations.


    Parameters
    ----------
    station_codes : str or list
        Single station code or iterable of station codes to retrieve data for.
    start : ``None`` or date (see :ref:`dates-and-times`)
        If specified, data are limited to values after this date.
    end : ``None`` or date (see :ref:`dates-and-times`)
        If specified, data are limited to values before this date.
    parameters : ``None``, str or list
        If specified, data are limited to this set of parameter codes.


    Returns
    -------
    data_dict : dict
        Dict with station codes keyed to lists of value dicts.
    """
    if start:
        start_date = util.convert_date(start)
    else:
        start_date = NCDC_GSOD_START_DATE
    if end:
        end_date = util.convert_date(end)
    else:
        end_date = datetime.date.today()
    if isinstance(parameters, basestring):
        parameters = [parameters]
    if parameters and not 'date' in parameters:
        # add date to list of parameters if it's not there already
        parameters.insert(0, 'date')
    if isinstance(station_codes, basestring):
        station_codes = [station_codes]

    # note: opening tar files and parsing the headers and such is a relatively
    # lengthy operation so you don't want to do it too often, hence try to
    # grab all stations at the same time per tarfile
    data_dict = dict([(station_code, None) for station_code in station_codes])

    for year in range(start_date.year, end_date.year + 1):
        tar_path = _get_gsod_file(year)
        with tarfile.open(tar_path, 'r:') as gsod_tar:
            stations_in_file = [
                name.split('./')[-1].rsplit('-', 1)[0]
                for name in gsod_tar.getnames() if len(name) > 1]
            if station_codes:
                stations = list(set(station_codes) & set(stations_in_file))
            else:
                stations = stations_in_file
            for station in stations:
                year_data = _read_gsod_file(gsod_tar, station, year)
                if parameters:
                    year_data = _subset_record_array(year_data, parameters)
                if not year_data is None:
                    # apply date ranges if they exist
                    if start_date or end_date:
                        mask = np.ones(len(year_data), dtype=bool)
                        if start_date:
                            mask = mask & (year_data['date'] >= start_date)
                        if end_date:
                            mask = mask & (year_data['date'] <= end_date)
                        year_data = year_data[mask]

                    if not data_dict[station] is None:
                        # XXX: this could be more efficient for large numbers
                        # of years with a list comprehension or generator
                        data_dict[station] = np.append(data_dict[station], year_data)
                    else:
                        data_dict[station] = year_data
    for station, data_array in data_dict.items():
        if not data_dict[station] is None:
            data_dict[station] = _record_array_to_value_dicts(data_array)
    return data_dict


def get_stations(country=None, state=None, start=None, end=None, update=True):
    """Retrieve information on the set of available stations.


    Parameters
    ----------
    country : {``None``, str, or iterable}
        If specified, results will be limited to stations with matching country
        codes.
    state : {``None``, str, or iterable}
        If specified, results will be limited to stations with matching state
        codes.
    start : ``None`` or date (see :ref:`dates-and-times`)
        If specified, results will be limited to stations which have data after
        this start date.
    end : ``None`` or date (see :ref:`dates-and-times`)
        If specified, results will be limited to stations which have data before
        this end date.
    update : bool
        If ``True`` (default), check for a newer copy of the stations file and
        download if it is newer the previously downloaded copy. If ``False``,
        then a new stations file will only be downloaded if a previously
        downloaded file cannot be found.


    Returns
    -------
    stations_dict : dict
        A dict with USAF-WBAN codes keyed to station information dicts.
    """
    if start:
        start_date = util.convert_date(start)
    else:
        start_date = None
    if end:
        end_date = util.convert_date(end)
    else:
        end_date = None

    if isinstance(country, basestring):
        country = [country]
    if isinstance(state, basestring):
        state = [state]

    stations_url = 'http://www1.ncdc.noaa.gov/pub/data/noaa/isd-history.csv'
    with util.open_file_for_url(stations_url, NCDC_GSOD_STATIONS_FILE) as f:
        reader = csv.DictReader(f)

        if country is None and state is None and start is None and end is None:
            rows = reader
        else:
            if start_date is None:
                start_str = None
            else:
                start_str = start_date.strftime('%Y%m%d')
            if end_date is None:
                end_str = None
            else:
                end_str = end_date.strftime('%Y%m%d')
            rows = [
                row for row in reader
                if _passes_row_filter(row, country=country, state=state,
                    start_str=start_str, end_str=end_str)
            ]

        stations = dict([
            (_station_code(row), _process_station(row))
            for row in rows
        ])
    return stations


def _convert_date_string(date_string):
    if date_string == '':
        return None

    if isinstance(date_string, bytes):
        date_string = date_string.decode('utf-8')

    return datetime.datetime.strptime(date_string, '%Y%m%d').date()


def _get_gsod_file(year):
    url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/%s/gsod_%s.tar' % (year, year)
    filename = url.split('/')[-1]
    path = os.path.join(NCDC_GSOD_DIR, filename)
    util.download_if_new(url, path, check_modified=True)
    return path


def _passes_row_filter(row, country=None, state=None, start_str=None,
        end_str=None):
    if not country is None and row['CTRY'] not in country:
        return False
    if not state is None and row['STATE'] not in state:
        return False
    if not start_str is None and row['END'] != '' and row['END'] <= start_str:
        return False
    if not end_str is None and row['BEGIN'] != '' and end_str <= row['BEGIN']:
        return False
    return True


def _process_station(station_row):
    """converts a csv row to a more human-friendly version"""
    station_dict = {
        'begin': _convert_date_string(station_row['BEGIN']),
        'icao': station_row['ICAO'],
        'country': station_row['CTRY'],
        'elevation': round(float(station_row['ELEV(M)']), 1) \
                if station_row['ELEV(M)'] not in ('', '-99999') else None,
        'end': _convert_date_string(station_row['END']),
        'latitude': round(float(station_row['LAT']), 3) \
                if station_row['LAT'] not in ('', '-99999') else None,
        'longitude': round(float(station_row['LON']), 3) \
                if station_row['LON'] not in ('', '-999999') else None,
        'name': station_row['STATION NAME'],
        'state': station_row['STATE'],
        'USAF': station_row['USAF'],
        'WBAN': station_row['WBAN'],
    }
    return station_dict


def _read_gsod_file(gsod_tar, station, year):
    tar_station_filename = station + '-' + str(year) + '.op.gz'
    try:
        gsod_tar.getmember('./' + tar_station_filename)
    except KeyError:
        return None

    ncdc_temp_dir = os.path.join(NCDC_GSOD_DIR, 'temp')
    util.mkdir_if_doesnt_exist(ncdc_temp_dir)
    temp_path = os.path.join(ncdc_temp_dir, tar_station_filename)

    gsod_tar.extract('./' + tar_station_filename, ncdc_temp_dir)
    with gzip.open(temp_path, 'rb') as gunzip_f:
        columns = [
            # name, length, # of spaces separating previous column, dtype
            ('USAF', 6, 0, 'U6'),
            ('WBAN', 5, 1, 'U5'),
            ('date', 8, 2, object),
            ('mean_temp', 6, 2, float),
            ('mean_temp_count', 2, 1, int),
            ('dew_point', 6, 2, float),
            ('dew_point_count', 2, 1, int),
            ('sea_level_pressure', 6, 2, float),
            ('sea_level_pressure_count', 2, 1, int),
            ('station_pressure', 6, 2, float),
            ('station_pressure_count', 2, 1, int),
            ('visibility', 5, 2, float),
            ('visibility_count', 2, 1, int),
            ('mean_wind_speed', 5, 2, float),
            ('mean_wind_speed_count', 2, 1, int),
            ('max_wind_speed', 5, 2, float),
            ('max_gust', 5, 2, float),
            ('max_temp', 6, 2, float),
            ('max_temp_flag', 1, 0, 'U1'),
            ('min_temp', 6, 1, float),
            ('min_temp_flag', 1, 0, 'U1'),
            ('precip', 5, 1, float),
            ('precip_flag', 1, 0, 'U1'),
            ('snow_depth', 5, 1, float),
            ('FRSHTT', 6, 2, 'U6'),
        ]

        dtype = np.dtype([
            (column[0], column[3])
            for column in columns])

        # note: ignore initial 0
        delimiter = itertools.chain(*[column[1:3][::-1] for column in columns])
        usecols = list(range(1, len(columns) * 2, 2))

        data = np.genfromtxt(gunzip_f, skip_header=1, delimiter=delimiter,
                usecols=usecols, dtype=dtype, converters={5: _convert_date_string})
    os.remove(temp_path)

    # somehow we can end up with single-element arrays that are 0-dimensional??
    # (occurs on tyler's machine but is hard to reproduce)
    if data.ndim == 0:
        data = data.flatten()

    return data


def _record_array_to_value_dicts(record_array):
    names = record_array.dtype.names
    value_dicts = [
        dict([(name, value[name_index])
                for name_index, name in enumerate(names)])
        for value in record_array]
    return value_dicts


def _station_code(station):
    """returns station code from a station dict"""
    return '-'.join([station['USAF'], station['WBAN']])


def _subset_record_array(record_array, parameters):
    dtype = np.dtype([
        (parameter, record_array[parameter].dtype)
        for parameter in parameters
    ])
    return np.array([
        tuple(i) for i in np.array([
            record_array[parameter] for parameter in parameters
        ]).T.tolist()
    ], dtype=dtype)
