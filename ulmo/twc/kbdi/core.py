"""
    ulmo.twc.kbdi.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides direct access to `Texas Weather Connection`_ `Daily
    Keetch-Byram Drought Index (KBDI)`_ dataset.

    .. _Texas Weather Connection: http://twc.tamu.edu/
    .. _Daily Keetch-Byram Drought Index (KBDI): http://twc.tamu.edu/drought/kbdi
"""

import datetime
import os

import numpy as np
import pandas

from ulmo import util

# directory where drought data will be stashed
TWC_KBDI_DIR = os.path.join(util.get_ulmo_dir(), 'twc/kbdi')

# fips codes from http://www.census.gov/geo/www/ansi/national.txt
# adjust names to match twc kbdi
data = np.genfromtxt('national.txt', delimiter=',', names=True, dtype=['S2', 'S2','S3','S35','S2'])
data = data[data['State_ANSI']=='48']
FIPS = dict((row['County_Name'].split('County')[0].strip().upper(), row['State_ANSI']+row['County_ANSI']) for row in data)
FIPS['DE WITT'] = FIPS['DEWITT']


def get_data(county_fips=None, start=None, end=None,
             as_dataframe=False):
    """Retreives data.


    Parameters
    ----------
    county_fips : ``None`` or str
        If specified, results will be limited to the county corresponding to the
        given 5-character texas county fips code i.e. 48???.
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

    data = None
    for date in _daterange(start_date, end_date):
        url = _get_data_url(date)
        with _open_data_file(url) as data_file:
            day_data = _parse_data_file(data_file)

        day_data['date'] = pandas.Period(date, freq='D')
        day_data['fips'] = day_data['county'].map(lambda county:FIPS[county])
        day_data = day_data.set_index('date')

        if county_fips:
            day_data = day_data[day_data['fips'] == county_fips]

        if data is None:
            data = day_data
        else:
            data = data.append(day_data)

    if as_dataframe:
        return data
    else:
        return _as_data_dict(data)


def _as_data_dict(dataframe):
    county_dict = {}
    for county in dataframe['fips'].unique():
        county_dataframe = dataframe[dataframe['fips'] == county]
        county_data = county_dataframe.reset_index().T.drop(['fips'])
        values = [
            _value_dict(value)
            	for k, value in county_data.iteritems()
            ]
        county_dict[county] = values

    return county_dict


def _daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def _get_data_url(date):
	return 'http://twc.tamu.edu/weather_images/summ/summ%s.txt' % date.strftime('%Y%m%d')


def _parse_data_file(data_file):
    """
    example:
    	COUNTY                        KBDI_AVG   KBDI_MAX    KBDI_MIN
		----------------------------------------------------------------
		ANDERSON                         262       485        47
		ANDREWS                          485       614       357
		...
    """


    dtype = [
        ('county', '|S15'),
        ('kbdi_avg', 'i4'),
        ('kbdi_min', 'i4'),
        ('kbdi_max', 'i4'),
    ]

    data_array = np.genfromtxt(data_file, delimiter=[31,11,11,11], dtype=dtype, skip_header=2, skip_footer=1, autostrip=True)
    dataframe = pandas.DataFrame(data_array)
    return dataframe


def _open_data_file(url):
    """returns an open file handle for a data file; downloading if necessary or otherwise using a previously downloaded file"""
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(TWC_KBDI_DIR, file_name)
    return util.open_file_for_url(url, file_path, check_modified=True)


def _value_dict(value):
    value_dict = value.to_dict()
    value_dict['date'] = str(value_dict['date'])
    return value_dict