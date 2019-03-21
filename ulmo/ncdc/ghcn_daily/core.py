"""
    ulmo.ncdc.ghcn_daily.core
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides direct access to `National Climatic Data Center`_
    `Global Historical Climate Network - Daily`_ dataset.


    .. _National Climatic Data Center: http://www.ncdc.noaa.gov
    .. _Global Historical Climate Network - Daily: http://www.ncdc.noaa.gov/oa/climate/ghcn-daily/

"""
from builtins import str
from builtins import range
from past.builtins import basestring
import itertools
import os

import numpy as np
import pandas

from ulmo import util


GHCN_DAILY_DIR = os.path.join(util.get_ulmo_dir(), 'ncdc/ghcn_daily')


def get_data(station_id, elements=None, update=True, as_dataframe=False):
    """Retrieves data for a given station.


    Parameters
    ----------
    station_id : str
        Station ID to retrieve data for.
    elements : ``None``, str, or list of str
        If specified, limits the query to given element code(s).
    update : bool
        If ``True`` (default),  new data files will be downloaded if they are
        newer than any previously cached files. If ``False``, then previously
        downloaded files will be used and new files will only be downloaded if
        there is not a previously downloaded file for a given station.
    as_dataframe : bool
        If ``False`` (default), a dict with element codes mapped to value dicts
        is returned. If ``True``, a dict with element codes mapped to equivalent
        pandas.DataFrame objects will be returned. The pandas dataframe is used
        internally, so setting this to ``True`` is a little bit faster as it
        skips a serialization step.


    Returns
    -------
    site_dict : dict
        A dict with element codes as keys, mapped to collections of values. See
        the ``as_dataframe`` parameter for more.
    """
    if isinstance(elements, basestring):
        elements = [elements]

    start_columns = [
        ('year', 11, 15, int),
        ('month', 15, 17, int),
        ('element', 17, 21, str),
    ]
    value_columns = [
        ('value', 0, 5, float),
        ('mflag', 5, 6, str),
        ('qflag', 6, 7, str),
        ('sflag', 7, 8, str),
    ]
    columns = list(itertools.chain(start_columns, *[
        [(name + str(n), start + 13 + (8 * n), end + 13 + (8 * n), converter)
         for name, start, end, converter in value_columns]
        for n in range(1, 32)
    ]))

    station_file_path = _get_ghcn_file(
        station_id + '.dly', check_modified=update)
    station_data = util.parse_fwf(station_file_path, columns, na_values=[-9999])

    dataframes = {}

    for element_name, element_df in station_data.groupby('element'):
        if not elements is None and element_name not in elements:
            continue

        element_df['month_period'] = element_df.apply(
                lambda x: pandas.Period('%s-%s' % (x['year'], x['month'])),
                axis=1)
        element_df = element_df.set_index('month_period')
        monthly_index = element_df.index

        # here we're just using pandas' builtin resample logic to construct a daily
        # index for the timespan
        # 2018/11/27 johanneshorak: hotfix to get ncdc ghcn_daily working again
        # new resample syntax requires resample method to generate resampled index.
        daily_index = element_df.resample('D').sum().index.copy()

        # XXX: hackish; pandas support for this sort of thing will probably be
        # added soon
        month_starts = (monthly_index - 1).asfreq('D') + 1
        dataframe = pandas.DataFrame(
                columns=['value', 'mflag', 'qflag', 'sflag'], index=daily_index)

        for day_of_month in range(1, 32):
            dates = [date for date in (month_starts + day_of_month - 1)
                    if date.day == day_of_month]
            if not len(dates):
                continue
            months = pandas.PeriodIndex([pandas.Period(date, 'M') for date in dates])
            for column_name in dataframe.columns:
                col = column_name + str(day_of_month)
                dataframe[column_name][dates] = element_df[col][months]

        dataframes[element_name] = dataframe

    if as_dataframe:
        return dataframes
    else:
        return dict([
            (key, util.dict_from_dataframe(dataframe))
            for key, dataframe in dataframes.items()
        ])


def get_stations(country=None, state=None, elements=None, start_year=None,
        end_year=None, update=True, as_dataframe=False):
    """Retrieves station information, optionally limited to specific parameters.


    Parameters
    ----------
    country : str
        The country code to use to limit station results. If set to ``None``
        (default), then stations from all countries are returned.
    state : str
        The state code to use to limit station results. If set to ``None``
        (default), then stations from all states are returned.
    elements : ``None``, str, or list of str
        If specified, station results will be limited to the given element codes
        and only stations that have data for any these elements will be
        returned.
    start_year : int
        If specified, station results will be limited to contain only stations
        that have data after this year. Can be combined with the ``end_year``
        argument to get stations with data within a range of years.
    end_year : int
        If specified, station results will be limited to contain only stations
        that have data before this year. Can be combined with the ``start_year``
        argument to get stations with data within a range of years.
    update : bool
        If ``True`` (default),  new data files will be downloaded if they are
        newer than any previously cached files. If ``False``, then previously
        downloaded files will be used and new files will only be downloaded if
        there is not a previously downloaded file for a given station.
    as_dataframe : bool
        If ``False`` (default), a dict with station IDs keyed to station dicts
        is returned. If ``True``, a single pandas.DataFrame object will be
        returned. The pandas dataframe is used internally, so setting this to
        ``True`` is a little bit faster as it skips a serialization step.


    Returns
    -------
    stations_dict : dict or pandas.DataFrame
        A dict or pandas.DataFrame representing station information for stations
        matching the arguments. See the ``as_dataframe`` parameter for more.
    """

    columns = [
        ('country', 0, 2, None),
        ('network', 2, 3, None),
        ('network_id', 3, 11, None),
        ('latitude', 12, 20, None),
        ('longitude', 21, 30, None),
        ('elevation', 31, 37, None),
        ('state', 38, 40, None),
        ('name', 41, 71, None),
        ('gsn_flag', 72, 75, None),
        ('hcn_flag', 76, 79, None),
        ('wm_oid', 80, 85, None),
    ]

    stations_file = _get_ghcn_file('ghcnd-stations.txt', check_modified=update)
    stations = util.parse_fwf(stations_file, columns)

    if not country is None:
        stations = stations[stations['country'] == country]
    if not state is None:
        stations = stations[stations['state'] == state]

    # set station id and index by it
    stations['id'] = stations[['country', 'network', 'network_id']].T.apply(''.join)

    if not elements is None or not start_year is None or not end_year is None:
        inventory = _get_inventory(update=update)
        if not elements is None:
            if isinstance(elements, basestring):
                elements = [elements]

            mask = np.zeros(len(inventory), dtype=bool)
            for element in elements:
                mask += inventory['element'] == element
            inventory = inventory[mask]
        if not start_year is None:
            inventory = inventory[inventory['last_year'] >= start_year]
        if not end_year is None:
            inventory = inventory[inventory['first_year'] <= end_year]

        uniques = inventory['id'].unique()
        ids = pandas.DataFrame(uniques, index=uniques, columns=['id'])
        stations = pandas.merge(stations, ids).set_index('id', drop=False)

    stations = stations.set_index('id', drop=False)
    # wm_oid gets convertidsed as a float, so cast it to str manually
    # pandas versions prior to 0.13.0 could use numpy's fix-width string type
    # to do this but that stopped working in pandas 0.13.0 - fortunately a
    # regex-based helper method was added then, too
    if pandas.__version__ < '0.13.0':
        stations['wm_oid'] = stations['wm_oid'].astype('|U5')
        stations['wm_oid'][stations['wm_oid'] == 'nan'] = np.nan
    else:
        stations['wm_oid'] = stations['wm_oid'].astype('|U5').map(lambda x: x[:-2])
        is_nan = stations['wm_oid'] == 'n'
        is_empty = stations['wm_oid'] == ''
        is_invalid = is_nan | is_empty
        stations.loc[is_invalid, 'wm_oid'] = np.nan

    if as_dataframe:
        return stations
    else:
        return util.dict_from_dataframe(stations)


def _get_ghcn_file(filename, check_modified=True):
    base_url = 'http://www1.ncdc.noaa.gov/pub/data/ghcn/daily/'
    if 'ghcnd-' in filename:
        url = base_url + filename
    else:
        url = base_url + 'all/' + filename

    path = os.path.join(GHCN_DAILY_DIR, url.split('/')[-1])
    util.download_if_new(url, path, check_modified=check_modified)
    return path


def _get_inventory(update=True):
    columns = [
        ('id', 0, 11, None),
        ('latitude', 12, 20, None),
        ('longitude', 21, 30, None),
        ('element', 31, 35, None),
        ('first_year', 36, 40, None),
        ('last_year', 41, 45, None),
    ]

    inventory_file = _get_ghcn_file('ghcnd-inventory.txt',
            check_modified=update)
    return util.parse_fwf(inventory_file, columns)
