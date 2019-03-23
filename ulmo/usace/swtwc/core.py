"""
    ulmo.usace.swtwc.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `United States Army
    Corps of Engineers`_ `Tulsa District Water Control`_ web site.

    .. _United States Army Corps of Engineers: http://www.usace.army.mil/
    .. _Tulsa District Water Control: http://www.swt-wc.usace.army.mil/

"""
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import zip
from builtins import range
import datetime
import os.path

from bs4 import BeautifulSoup
import numpy as np
import requests
import pandas

from ulmo import util

try:
    import io as StringIO
except ImportError:
    from cStringIO import StringIO

USACE_SWTWC_DIR = os.path.join(util.get_ulmo_dir(), 'usace/swtwc')


def get_station_data(station_code, date=None, as_dataframe=False):
    """Fetches data for a station at a given date.


    Parameters
    ----------
    station_code: str
        The station code to fetch data for. A list of stations can be retrieved with
        ``get_stations()``
    date : ``None`` or date (see :ref:`dates-and-times`)
        The date of the data to be queried. If date is ``None`` (default), then
        data for the current day is retreived.
    as_dataframe : bool
        This determines what format values are returned as. If ``False``
        (default), the values dict will be a dict with timestamps as keys mapped
        to a dict of gauge variables and values. If ``True`` then the values
        dict will be a pandas.DataFrame object containing the equivalent
        information.


    Returns
    -------
    data_dict : dict
        A dict containing station information and values.
    """

    station_dict = {}
    if date is None:
        date_str = 'current'
        year = datetime.date.today().year
    else:
        date = util.convert_date(date)
        date_str = date.strftime('%Y%m%d')
        year = date.year

    filename = '{}.{}.html'.format(station_code, date_str)
    data_url = 'http://www.swt-wc.usace.army.mil/webdata/gagedata/' + filename

    # requests without User-Agent header get rejected
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    resp = requests.get(data_url, headers=headers)
    soup = BeautifulSoup(resp.content)
    pre = soup.find('pre')
    if pre is None:
        error_msg = 'no data could be found for station code %(station_code)s and date %(date)s (url: %(data_url)s)' % {
            'date': date,
            'data_url': data_url,
            'station_code': station_code,
        }
        raise ValueError(error_msg)
    sio = StringIO.StringIO(str(pre.text.strip()))

    first_line = sio.readline()
    split = first_line[8:].strip().split()

    station_dict['code'] = split[0]
    station_dict['description'] = ' '.join(split[1:])

    second_line = sio.readline()
    station_dict['station_type'] = second_line.strip().split(':')[1].strip()

    notes = []

    while 1:
        next_line = sio.readline()
        if ':' in next_line:
            notes.append(next_line.strip())
        else:
            break

    if len(notes):
        station_dict['notes'] = '\n'.join(notes)

    variable_names = _split_line(sio.readline()[11:], 10)
    variable_units = _split_line(sio.readline()[11:], 10)
    variable_sources = _split_line(sio.readline()[11:], 10)

    station_dict['variables'] = dict([
        (name, {'unit': unit, 'source': source})
        for name, unit, source in zip(
            variable_names, variable_units, variable_sources)
    ])

    station_dict['timezone'] = sio.readline().strip().strip('()')
    column_names = ['datetime'] + variable_names
    widths = [14] + ([10] * len(variable_names))
    converters = dict([
        (variable_name, lambda x: float(x) if x != '----' else np.nan)
        for variable_name in variable_names
    ])
    date_parser = lambda x: _convert_datetime(x, year)
    dataframe = pandas.read_fwf(
        sio, names=column_names, widths=widths, index_col=['datetime'],
        na_values=['----'], converters=converters, parse_dates=True,
        date_parser=date_parser)

    # parse out rows that are all nans (e.g. end of "current" page)
    dataframe = dataframe[~np.isnan(dataframe.T.sum())]

    if as_dataframe:
        station_dict['values'] = dataframe
    else:
        station_dict['values'] = util.dict_from_dataframe(dataframe)

    return station_dict


def get_stations():
    """Fetches a list of station codes and descriptions.

    Returns
    -------
    stations_dict : dict
        a python dict with station codes mapped to station information
    """
    stations_url = 'http://www.swt-wc.usace.army.mil/shefids.htm'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    resp = requests.get(stations_url, headers=headers)
    soup = BeautifulSoup(resp.content)
    pre = soup.find('pre')
    links = pre.find_all('a')
    stations = [
        _parse_station_link(link) for link in links
    ]

    return dict([
        (station['code'], station)
        for station in stations
    ])


def _convert_datetime(s, year):
    fmt = '%m/%d %H:%M'
    return datetime.datetime.strptime(s, fmt).replace(year=year)


def _split_line(line, n):
    return [line[i:i + n].strip() for i in range(0, len(line), n)][:-1]


def _parse_station_link(link):
    return {
        'code': link.text,
        'description': link.next_sibling.strip(),
    }


def _to_underscore(spaced):
    return spaced.sub(' ', '_').sub('(', '').sub(')', '').lower()
