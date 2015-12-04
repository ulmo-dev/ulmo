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

import dateutil

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


def get_sites():
    """Fetches a list of site codes and descriptions.
    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
    """
    sites_url = 'http://waterquality.lcra.org/sitelist.aspx'

    response = requests.get(sites_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    gridview = soup.find(id="GridView1")

    sites = [
        (row.findAll('td')[0].string, row.findAll('td')[1].string)
        for row in gridview.findAll('tr')
        if len(row.findAll('td'))==2
    ]

    return dict(sites)


def get_site_data(site_code, date=None, as_dataframe=False):
    """Fetches data for a site at a given date.
    Parameters
    ----------
    site_code: str
        The site code to fetch data for. A list of sites can be retrieved with
        ``get_sites()``
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
        A dict containing site information and values.
    """


    if isinstance(site_code, (str)):
        pass
    elif isinstance(site_code, (int)):
        site_code = str(site_code)
    else:
        log.error("Unsure of the site_code parameter type. \
                Try string or int")
        raise

    waterquality_url = "http://waterquality.lcra.org/parameter.aspx?qrySite=%s" % site_code
    waterquality_url2 = 'http://waterquality.lcra.org/events.aspx'

    initial_request = requests.get(waterquality_url)
    initialsoup = BeautifulSoup(initial_request.content, 'html.parser')

    sitevals = [statag.get('value', None)
        for statag in initialsoup.findAll(id="multiple")
        if statag.get('value', None)]

    result = _make_next_request(waterquality_url2, 
                                initial_request, 
                                {'multiple': sitevals,
                                'site': site_code})

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

    if date:
        try:
            datelim = dateutil.parser.parse(date)
        except ValueError:
            log.warn("Could not parse the provided date %s" % date)
            datelim = None
        if datelim:
            df = _create_dataframe(results)
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

