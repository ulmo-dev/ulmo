import itertools
import os

import numpy as np
import pandas

from ulmo import util


GHCN_DAILY_DIR = os.path.join(util.get_ulmo_dir(), 'ncdc/ghcn_daily')


def get_data(station_id, elements=None, update=True, as_dataframe=False):
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
        for n in xrange(1, 32)
    ]))

    station_file_path = _get_ghcn_file(station_id + '.dly',
            check_modified=update)
    station_data = _parse_fwf(station_file_path, columns, na_values=[-9999])

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
        daily_index = element_df.resample('D').index.copy()

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
            months = [pandas.Period(date, 'M') for date in dates]
            for column_name in dataframe.columns:
                col = column_name + str(day_of_month)
                dataframe[column_name][dates] = element_df[col][months]

        dataframes[element_name] = dataframe

    if as_dataframe:
        return dataframes
    else:
        return {
            key: util.dict_from_dataframe(dataframe)
            for key, dataframe in dataframes.iteritems()
        }


def get_stations(country=None, state=None, elements=None, start_year=None,
        end_year=None, update=True, as_dataframe=False):
    """returns a collection of stations

    The stations can be represented as dict of station dicts keyed to their station ID
    or a pandas.dataframe (see the as_dataframe parameter)

    Parameters
    ----------
    country : The country code to use to limit station results. If set to None
            (default), then stations from all countries are returned.
    state : The state code to use to limit station results. If set to None
            (default), then stations from all states are returned.
    elements : List of elements to use to limit the station results. If set,
            only stations that have data for any these elements will be returned.
    start_year : Start year to use to limit the station results. If set, only
            stations that have data after start year will be returned. Can be
            combined with end_year to get stations with data within a range of
            years.
    end_year : End year to use to limit the station results. If set, only
            stations that have data before the end year will be returned. Can be
            combined with start_year to get stations with data within a range of
            years.
    update : If False, tries to use a cached copy of the stations file. If one
             can't be found or if update is True, then a new copy of the
             stations file is pulled from the web. If update is True, but the
             cached stations file is still good then a new file won't be pulled.
             Default is True.
    as_dataframe : If True, a pandas.DataFrame object will be returned,
            otherwise a dict is of stations dicts is returned. The pandas
            dataframe is used internally, so setting this to True is a little
            bit faster as it skips a serialization step. Default is False.,
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
    stations = _parse_fwf(stations_file, columns)

    if not country is None:
        stations = stations[stations['country'] == country]
    if not state is None:
        stations = stations[stations['state'] == state]

    # set station id and index by it
    stations['id'] = stations[['country', 'network', 'network_id']].T.apply(''.join)
    stations = stations.set_index('id', drop=False)

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
            inventory = inventory[start_year <= inventory['last_year']]
        if not end_year is None:
            inventory = inventory[inventory['first_year'] <= end_year]

        uniques = inventory['id'].unique()
        ids = pandas.DataFrame(uniques, index=uniques, columns=['id'])
        stations = pandas.merge(stations, ids).set_index('id', drop=False)

    # wm_oid gets converted as a float, so cast it to str manually
    stations['wm_oid'] = stations['wm_oid'].astype('|S5')
    stations['wm_oid'][stations['wm_oid'] == 'nan'] = np.nan

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
    util.download_if_new(url, path)
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
    return _parse_fwf(inventory_file, columns)


def _parse_fwf(file_path, columns, na_values=None):
    colspecs = [(start, end) for name, start, end, converter in columns]
    names = [name for name, start, end, converter in columns]
    converters = {
        name: converter
        for name, start, end, converter in columns
        if not converter is None
    }

    return pandas.io.parsers.read_fwf(file_path,
        colspecs=colspecs, header=None, na_values=na_values, names=names,
        converters=converters)
