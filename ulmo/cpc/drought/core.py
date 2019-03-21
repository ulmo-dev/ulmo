"""
    ulmo.cpc.drought.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides direct access to `Climate Predicition Center`_ `Weekly
    Drought Index`_ dataset.

    .. _Climate Prediction Center: http://www.cpc.ncep.noaa.gov/
    .. _Weekly Drought Index: http://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/palmer_drought/
"""
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div

import datetime
import os
import requests

import numpy as np
import pandas

from ulmo import util

# directory where drought data will be stashed
CPC_DROUGHT_DIR = os.path.join(util.get_ulmo_dir(), 'cpc/drought')

# state codes (note: these are not FIPS codes)
STATE_CODES = {
    'AL': 1,
    'AZ': 2,
    'AR': 3,
    'CA': 4,
    'CO': 5,
    'CT': 6,
    'DE': 7,
    'FL': 8,
    'GA': 9,
    'IA': 13,
    'ID': 10,
    'IL': 11,
    'IN': 12,
    'KS': 14,
    'KY': 15,
    'LA': 16,
    'MA': 19,
    'MD': 18,
    'ME': 17,
    'MI': 20,
    'MN': 21,
    'MO': 23,
    'MS': 22,
    'MT': 24,
    'NC': 31,
    'ND': 32,
    'NE': 25,
    'NH': 27,
    'NJ': 28,
    'NM': 29,
    'NV': 26,
    'NY': 30,
    'OH': 33,
    'OK': 34,
    'OR': 35,
    'PA': 36,
    'PR': 66,
    'RI': 37,
    'SC': 38,
    'SD': 39,
    'TN': 40,
    'TX': 41,
    'UT': 42,
    'VA': 44,
    'VT': 43,
    'WA': 45,
    'WI': 47,
    'WV': 46,
    'WY': 48,
}

def get_data(state=None, climate_division=None, start=None, end=None,
             as_dataframe=False):
    """Retreives data.


    Parameters
    ----------
    state : ``None`` or str
        If specified, results will be limited to the state corresponding to the
        given 2-character state code.
    climate_division : ``None`` or int
        If specified, results will be limited to the climate division.
    start : ``None`` or date (see :ref:`dates-and-times`)
        Results will be limited to those after the given date. Default is the
        start of the current calendar year.
    end : ``None`` or date (see :ref:`dates-and-times`)
        If specified, results will be limited to data before this date.
    as_dataframe: bool
        If ``False`` (default), a dict with a nested set of dicts will be
        returned with data indexed by state, then climate division. If ``True``
        then a pandas.DataFrame object will be returned.  The pandas dataframe
        is used internally, so setting this to ``True`` is a little bit faster
        as it skips a serialization step.


    Returns
    -------
    data : dict or pandas.Dataframe
        A dict or pandas.DataFrame representing the data. See the
        ``as_dataframe`` parameter for more.
    """
    if not start is None:
        start_date = util.convert_date(start)
    else:
        start_date = None
    if not end is None:
        end_date = util.convert_date(end)
    else:
        end_date = None

    if not end_date:
        end_date = datetime.date.today()
    if not start_date:
        start_date = datetime.date(end_date.year, 1, 1)

    start_year, start_week = _week_number(start_date)
    end_year, end_week = _week_number(end_date)

    if state:
        state_code = STATE_CODES.get(state.upper())
    else:
        state_code = None

    data = None
    for year in range(start_year, end_year + 1):
        url, current_year_flag = _get_data_url(year)
        format_type = _get_data_format(year)
        with _open_data_file(url) as data_file:
            year_data = _parse_data_file(data_file, format_type, year, current_year_flag)

        if state_code:
            year_data = year_data[year_data['state_code'] == state_code]
        if climate_division:
            year_data = year_data[year_data['climate_division'] == climate_division]

        year_data = _reindex_data(year_data)

        if data is None:
            data = year_data
        else:
            # some data are duplicated (e.g. final data from 2011 stretches into
            # prelim data of 2012), so just take those that are new
            append_index = year_data.index.difference(data.index)
            if len(append_index):
                data = data.append(year_data.loc[append_index])

    # restrict results to date range
    period_index = pandas.PeriodIndex(data['period'])
    periods_in_range = (period_index >= start_date) & (period_index <= end_date)
    data = data[periods_in_range]

    # this does what data.reset_index() should do, but at least as of 0.10.1, that sets
    # will cast period objects to ints
    data.index = np.arange(len(data))
    if as_dataframe:
        return data
    else:
        return _as_data_dict(data)


def _as_data_dict(dataframe):
    data_dict = {}
    for state in dataframe['state'].unique():
        state_dict = {}
        state_dataframe = dataframe[dataframe['state'] == state]
        for name, group in state_dataframe.groupby(['state', 'climate_division']):
            s, climate_division = name
            climate_division_data = group.T.drop(['state', 'climate_division'])
            values = [
                _value_dict(value)
                for k, value in climate_division_data.iteritems()
            ]
            state_dict[climate_division] = values
        data_dict[state] = state_dict
    return data_dict


def _convert_state_codes(dataframe):
    """adds state abbreviations to a dataframe, based on state codes"""
    state_codes = pandas.DataFrame(
        np.array([i for i in STATE_CODES.items()],
                 dtype=np.dtype([('state', '|U2'), ('code', int)])))
    merged = pandas.merge(dataframe, state_codes,
            left_on='state_code', right_on='code', how='left')
    column_names = dataframe.columns.tolist()
    column_names.remove('state_code')
    column_names.insert(0, 'state')
    return merged[column_names]


def _convert_week_numbers(dataframe):
    """convert a dataframe's week numbers to period objects"""
    weeks = [key for key, group in dataframe.groupby(['year', 'week'])]
    periods = [(week[0], week[1], _period_for_week(*week)) for week in weeks]
    period_dataframe = pandas.DataFrame(periods, columns=['year', 'week', 'period'])
    merged = pandas.merge(dataframe, period_dataframe,
            left_on=['year', 'week'], right_on=['year', 'week'])
    column_names = dataframe.columns.tolist()
    column_names.remove('week')
    column_names.remove('year')
    column_names.insert(2, 'period')
    return merged[column_names]


def _first_sunday(year):
    """returns the first Sunday of a growing season, which is the first Sunday
    after the first Wednesday in March
    """
    first_day = datetime.date(year, 3, 1)
    if first_day.weekday() == 6:
        return first_day
    elif first_day.weekday() <= 2:
        return first_day - pandas.tseries.offsets.Week(weekday=6)
    else:
        return first_day + pandas.tseries.offsets.Week(weekday=6)


def _get_data_format(year):
    if year >= 2001:
        return 'format5'
    elif 1997 <= year <= 2000:
        return 'format4'
    else:
        return 'format2'


def _get_data_url(year):
    current_year, current_week = _week_number(datetime.date.today())
    if year == current_year:
        return ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp4/current.data', True)
    elif year == current_year - 1:
        url = ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer%s-PRELIM' % str(year)[-2:],
                False)
        if not _url_exists(url[0]):
            url = ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp4/current.data', True)
        return url
    elif year <= 1985:
        return ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer73-85', False)
    else:
        url = ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer%s' % str(year)[-2:], False)
        if not _url_exists(url[0]):
            url = ('http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer%s-PRELIM' % str(year)[-2:],
                    False)
        return url


def _open_data_file(url):
    """returns an open file handle for a data file; downloading if necessary or otherwise using a previously downloaded file"""
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(CPC_DROUGHT_DIR, file_name)
    return util.open_file_for_url(url, file_path, check_modified=True, use_bytes=True)


def _parse_data_file(data_file, palmer_format, year, current_year_flag):
    """
    based on the fortran format strings:
        format2: FORMAT(I4,3I2,F4.1,F4.0,10F6.2,4F6.4,F6.3,10F6.2,F4.0,12F6.2)
        format4: FORMAT(2I4,I2,F4.1,F4.0,10F6.2,4F6.4,F6.3,10F6.2,F4.0,12F6.2)
        format5: FORMAT(2I4,I2,F5.2,F5.1,10F6.2,4F6.4,F6.3,10F6.2,F4.0,12F6.2)
    """
    if palmer_format == 'format5':
        delim_sequence = (2, 2, 4, 2, 5, 5) + 10*(6,) + 4*(6,) + (6,) + 10*(6,) + (4,) + 12*(6,)
        use_columns = (0, 1, 2, 3, 4, 5, 9, 15, 28, 29, 37, 40, 41)
    elif palmer_format == 'format4':
        delim_sequence = (2, 2, 4, 2, 4, 4) + 10*(6,) + 4*(6,) + (6,) + 10*(6,) + (4,) + 12*(6,)
        use_columns = (0, 1, 2, 3, 4, 5, 9, 15, 28, 29, 37, 40, 41)
    elif palmer_format == 'format2':
        delim_sequence = (2, 2, 2, 2, 2, 4, 4) + 10*(6,) + 4*(6,) + (6,) + 10*(6,) + (4,) + 12*(6,)
        use_columns = (0, 1, 2, 3, 5, 6, 10, 16, 29, 30, 38, 41, 42)
    else:
        raise NotImplementedError("we have not implemented the format for given date range")

    dtype = [
        ('state_code', 'i1'),
        ('climate_division', 'i1'),
        ('year', 'i4'),
        ('week', 'i4'),
        ('precipitation', 'f8'),
        ('temperature', 'f8'),
        ('potential_evap', 'f8'),
        ('runoff', 'f8'),
        ('soil_moisture_upper', 'f8'),
        ('soil_moisture_lower', 'f8'),
        ('pdsi', 'f8'),
        ('cmi', 'f8')
    ]

    decodef = lambda x: x.decode("utf-8")
    data_array = np.genfromtxt(data_file, dtype=dtype, delimiter=delim_sequence, usecols=use_columns)
    if not current_year_flag:
        data_array['year'] = year
    dataframe = pandas.DataFrame(data_array)
    return dataframe


def _periods_for_range(start_date, end_date):
    return pandas.period_range(start_date, end_date, freq='W-SAT')


def _period_for_week(year, week_number):
    """returns a pandas.Period for a given growing season year and week number"""
    first_sunday = _first_sunday(year)
    return pandas.Period(first_sunday, freq='W-SAT') + week_number - 1


def _reindex_data(dataframe):
    dataframe = _convert_week_numbers(dataframe)
    dataframe = _convert_state_codes(dataframe)
    return dataframe.set_index(
        ['state', 'climate_division', 'period'], drop=False)


def _url_exists(url):
    return requests.head(url).status_code == 200


def _value_dict(value):
    value_dict = value.to_dict()
    value_dict['period'] = str(value_dict['period'])
    return value_dict


def _week_number(date):
    """returns the growing season week number for a given datetime.date"""
    first_sunday = _first_sunday(date.year)
    date_ts = pandas.Timestamp(date)
    first_sunday_ts = pandas.Timestamp(first_sunday)
    if date_ts < first_sunday_ts:
        first_sunday_ts = pandas.Timestamp(_first_sunday(date.year - 1))
    days_since_first_sunday = (date_ts - first_sunday_ts).days
    return (first_sunday_ts.year, (old_div(days_since_first_sunday, 7)) + 1)
