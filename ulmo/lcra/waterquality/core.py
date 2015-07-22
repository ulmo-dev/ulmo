"""
    ulmo.lcra.waterquality.core
    ~~~~~~~~~~~~~~~~~~~~~
    This module provides access to data provided by the `Lower Colorado 
    River Authority`_ `Water Quality`_ web site.
    .. _Lower Colorado River Authority: http://www.lcra.org
    .. _Water Quality: http://waterquality.lcra.org/
"""
from bs4 import BeautifulSoup
import logging

from ulmo import util



import pickle
import dateutil
import os

# import datetime
import os.path as op

LCRA_WATERQUALITY_DIR = op.join(util.get_ulmo_dir(), 'lcra/waterquality')


log = logging.getLogger(__name__)

from bs4 import BeautifulSoup
import requests


import pandas as pd 



# try:
#     import cStringIO as StringIO
# except ImportError:
#     import StringIO


def get_stations():
    """Fetches a list of station codes and descriptions.
    Returns
    -------
    stations_dict : dict
        a python dict with station codes mapped to station information
    """
    stations_url = 'http://waterquality.lcra.org/sitelist.aspx'
    path = op.join(LCRA_WATERQUALITY_DIR, 'stationids.htm')

    response = requests.get(stations_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    gridview = soup.find(id="GridView1")

    stations = [
        (row.findAll('td')[0].string, row.findAll('td')[1].string)
        for row in gridview.findAll('tr')
        if len(row.findAll('td'))==2
    ]

    return dict(stations)


def get_station_data(station_code, date=None, as_dataframe=False):
    """Fetches data for a station at a given date.
    Parameters
    ----------
    station_code: str
        The station code to fetch data for. A list of stations can be retrieved with
        ``get_stations()``
    date : ``None`` or date (see :ref:`dates-and-times`)
        The date of the data to be queried. If date is ``None`` (default), then
        all data will be returned.
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


    if isinstance(station_code, (str)):
        pass
    elif isinstance(station_code, (int)):
        station_code = str(station_code)
    else:
        log.error("Unsure of the station_code parameter type. \
                Try string or int")
        raise

    waterquality_url = "http://waterquality.lcra.org/parameter.aspx?qrySite=%s" %station_code
    waterquality_url2 = 'http://waterquality.lcra.org/events.aspx'

    dir_path = op.join(LCRA_WATERQUALITY_DIR, str(station_code))

    resp_path = op.join(dir_path, "resp.html")

    pickle_path = op.join(dir_path, "data.pickle")

    util.mkdir_if_doesnt_exist(dir_path)



    initial_request = requests.get(waterquality_url)
    initialsoup = BeautifulSoup(initial_request.content, 'html.parser')

    stationvals = [ statag.get('value', None)
        for statag in initialsoup.findAll(id="multiple")
        if statag.get('value', None)
    ]

    result = _make_next_request(waterquality_url2, 
                                initial_request, 
                                {'multiple': stationvals,
                                'site': station_code})

    if op.exists(resp_path) and \
        util.misc._request_file_size_matches(result, resp_path)\
        and not os.environ.get('ULMO_TESTING', None):
        #means nothing has changed return cached pickle
        log.info("%s was not processed because it is the same size"%station_code)
        try:
            with open(pickle_path, 'rb') as f:
                return pickle.load(f)
        except IOError:
            log.info("Couldn't find the pickle that should be there for \
                    %s" %station_code)
            pass


    if not os.environ.get('ULMO_TESTING', None):
        with open(resp_path, 'wb') as wf:
            wf.write(result.content)


    soup = BeautifulSoup(result.content, 'html.parser')

    gridview = soup.find(id="GridView1")


    results = []

    headers = [head.text for head in gridview.findAll('th')]

    #uses \xa0 for blank

    for row in gridview.findAll('tr'):
        vals = [_parse_val(aux.text) for aux in row.findAll('td')]
        if len(vals) == 0:
            continue

        results.append(dict(zip(headers, vals)))

    if not os.environ.get('ULMO_TESTING', None):
        with open(pickle_path, 'wb') as mf:
            pickle.dump(results, mf)

    if date:
        try:
            datelim = dateutil.parser.parse(date)
        except ValueError:
            log.warn("Could not parse the provided date %s" %date)
            datelim = None
        if datelim:
            df= _create_dataframe(results)
            cut_df = df[df['Date'] > datelim]
            if as_dataframe:
                return cut_df
            else:
                return cut_df.to_dict('records')

    if as_dataframe:
        return _create_dataframe(results)
    else:
        return results

def _create_dataframe(results):
    df = pd.DataFrame.from_records(results)
    df['Date'] = df['Date'].apply(dateutil.parser.parse)
    df.set_index(['Date'])
    return df

def _extract_headers_for_next_request(request):
    payload = dict()
    for tag in BeautifulSoup(request.content, 'html.parser').findAll('input'):
        tag_dict = dict(tag.attrs)
        if tag_dict.get('value', None) == 'tabular':
            #
            continue
        #some tags don't have a value and are used w/ JS to toggle a set of checkboxes
        payload[tag_dict['name']] = tag_dict.get('value')
    return payload


def _make_next_request(url, previous_request, data):
    data_headers = _extract_headers_for_next_request(previous_request)
    data_headers.update(data)
    return requests.post(url, cookies=previous_request.cookies, data=data_headers)


def _parse_val(val):
    #the &nsbp translates to the following unicode
    if val == u'\xa0':
        return None
    else:
        return val


