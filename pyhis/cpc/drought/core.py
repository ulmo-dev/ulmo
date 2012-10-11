"""
drought index data from the National Weather Service Climatic Predicition Center
"""
import datetime
import os

import numpy as np
import pandas

from pyhis import util

# directory where drought data will be stashed
CPC_DROUGHT_DIR = os.path.join(util.get_pyhis_dir(), 'cpc/drought')

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


def get_data(state=None, climate_division=None, start_date=None, end_date=None):
    start_date = util.parse_datestr(start_date)
    end_date = util.parse_datestr(end_date)
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
        url =_get_data_url(year)
        format_type =_get_data_format(year)
        with _open_data_file(url) as data_file:
            year_data = _parse_data_file(data_file, format_type)

        if state_code:
            year_data = year_data[year_data['state_code'] == state_code]
        if climate_division:
            year_data = year_data[year_data['climate_division'] == climate_division]

        if start_year == year:
            year_data = year_data[year_data['week'] >= start_week]
        if end_year == year:
            year_data = year_data[year_data['week'] <= end_week]

        if data is None:
            data = year_data
        else:
            data = data.append(year_data, ignore_index=True)

    data = _convert_state_codes(data)
    return data


def _convert_state_codes(dataframe):
    """adds state abbreviations to a dataframe, based on state codes"""
    state_codes = pandas.DataFrame(
        np.array([i for i in STATE_CODES.iteritems()],
                 dtype=np.dtype([('state', '|S2'), ('code', int)])))
    merged = pandas.merge(dataframe, state_codes, left_on='state_code', right_on='code', how='left')
    return merged[['state', 'climate_division', 'year', 'week', 'cmi', 'pdsi']]


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
    if year >= 1997:
        return 'format5'
    elif 1988 <= year <= 1996:
        return 'format2'
    else:
        return 'unknown'


def _get_data_url(year):
    current_year = datetime.date.today().year
    if year == current_year:
        return 'http://ftp.cpc.ncep.noaa.gov/htdocs/temp4/current.data'
    elif year == 2011:
        return 'http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer11-PRELIM'
    elif 1985 < year <= 2010:
        return 'http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer%s' % str(year)[-2:]
    elif year <= 1985:
        return 'http://ftp.cpc.ncep.noaa.gov/htdocs/temp2/palmer73-85'


def _open_data_file(url):
    """returns an open file handle for a data file; downloading if necessary or otherwise using a previously downloaded file"""
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(CPC_DROUGHT_DIR, file_name)
    return util.open_file_for_url(url, file_path, check_modified=True)


def _parse_data_file(data_file, palmer_format):
    if palmer_format == 'format5':
        delim_sequence = (2, 2, 4, 2, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6)
        use_columns = (0, 1, 2, 3, 37, 40)
    else:
        raise NotImplementedError("we have not implemented the format for given date range")

    dtype = [('state_code', 'i1'), ('climate_division', 'i1'), ('year', 'i4'), ('week', 'i4'), ('pdsi', 'f8'), ('cmi', 'f8')]
    data_array = np.genfromtxt(data_file, dtype=dtype, delimiter=delim_sequence, usecols=use_columns)
    dataframe = pandas.DataFrame(data_array)
    return dataframe


def _periods_for_range(start_date, end_date):
    return pandas.period_range(start_date, end_date, freq='W-SAT')


def _period_for_week_number(year, week_number):
    """returns a pandas.Period for a given growing season year and week number"""
    first_sunday = _first_sunday(year)
    return pandas.Period(first_sunday, freq='W-SAT') + week_number - 1


def _separate_by_climate_divisions(dataframe):
    dataframe.groupby(['state', 'climate_division'])
    import pdb; pdb.set_trace()


def _week_number(date):
    """returns the growing season week number for a given datetime.date"""
    first_sunday = _first_sunday(date.year)
    if date < first_sunday:
        first_sunday = _first_sunday(date.year - 1)
    days_since_first_sunday = (date - first_sunday).days
    return (first_sunday.year, (days_since_first_sunday / 7) + 1)


if __name__ == '__main__':
    data = get_data(state='tx', start_date='2011-01-01')
    import pdb; pdb.set_trace()
