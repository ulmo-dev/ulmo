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
from geojson import Point, Feature, FeatureCollection
#import unicode

from ulmo import util

import dateutil

# import datetime
import os.path as op

LCRA_WATERQUALITY_DIR = op.join(util.get_ulmo_dir(), 'lcra/waterquality')


log = logging.getLogger(__name__)

import requests


import pandas as pd

source_map = {
    'LCRA': 'Lower Colorado River Authority',
    'UCRA': 'Upper Colorado River Authority',
    'CRMWD': 'Colorado River Municipal Water District',
    'COA': 'City of Austin',
    'TCEQ': 'Texas Commission on Environmental Quality',
}

real_time_sites = {
    '6977': 'Matagorda 4SSW',
    '6985': 'Matagorda 7 SW',
    '6990': 'Matagorda 8 SSW',
    '6996': 'Matagorda 9 SW'
}

# try:
#     import cStringIO as StringIO
# except ImportError:
#     import StringIO


def get_sites(source_agency=None):
    """Fetches a list of sites with location and available metadata.
    Parameters
    ----------
    source_agency : LCRA used code of the that collects the data. there
    are sites whose sources are not listed so this filter may not return
    all sites of a certain source. see
    ``source_map``.
    Returns
    -------
    sites_geojson : geojson FeatureCollection
    """
    sites_url = 'http://waterquality.lcra.org/'
    response = requests.get(sites_url)
    lines = response.content.decode('utf-8').split('\n')
    sites_unprocessed = [
        line.strip().strip('createMarker').strip("(").strip(")").split(',')
        for line in lines if 'createMarker' in line]
    sites = [_create_feature(site_info) for site_info in sites_unprocessed]
    if source_agency:
        if not source_agency.upper() in source_map.keys():
            log.info('the source %s is not recognized' % source_agency)
            return {}
        else:
            sites = [site for site in sites if site['properties']['source'] ==
            source_map[source_agency.upper()]]
    sites_geojson = FeatureCollection(sites)

    return sites_geojson


def get_historical_data(site_code, start=None, end=None, as_dataframe=False):
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

    data = _create_dataframe(results)

    if start and not data.empty:
        data = data.ix[util.convert_date(start):]

    if end and not data.empty:
        data = data.ix[:util.convert_date(end)]

    if as_dataframe:
        return data
    else:
        return data.to_dict(orient='records')


def get_recent_data(site_code, as_dataframe=False):
    """fetches near real-time instantaneous water quality data for the LCRA
    bay sites.
    Parameters
    ----------
    site_code : str
        The bay site to fetch data for. see `real_time_sites`
    as_dataframe : bool
        This determines what format values are returned as. If ``False``
        (default), the values will be list of value dicts. If ``True`` then 
        values are returned as pandas.DataFrame.
    Returns
    -------
    list of values or dataframe.
    """
    if site_code not in real_time_sites.keys():
        log.info('%s is not in the list of LCRA real time salinity sites' %
                 site_code)
        return {}
    data_url = 'http://waterquality.lcra.org/salinity.aspx?sNum=%s&name=%s' % (
        site_code, real_time_sites[site_code])
    data = pd.read_html(data_url, header=0)[1]
    data.index = data['Date - Time'].apply(lambda x: util.convert_datetime(
        x))
    data.drop('Date - Time', axis=1, inplace=True)
    data = data.applymap(_nan_values)
    data.dropna(how='all', axis=0, inplace=True)
    data.dropna(how='all', axis=1, inplace=True)
    columns = dict([(column, _beautify_header(column)) for column in
                     data.columns])
    data.rename(columns=columns, inplace=True)
    data = data.astype(float)

    if as_dataframe:
        return data
    else:
        return util.dict_from_dataframe(data)


def _nan_values(value):
    if value == -998. or value == '--':
        return pd.np.nan
    else:
        return value


def _beautify_header(str):
    return str.replace(u'\xb0', 'deg').lower().replace(
        '(', '').replace(')', '').replace(
        u'%', u'percent').replace(' ', '_').replace(u'/', 'per')


def get_site_info(site_code):
    sites = get_sites()
    site = [site for site in sites['features']
            if site_code == site['properties']['site_code']]
    return site


def _create_dataframe(results):
    df = pd.DataFrame.from_records(results)
    df['Date'] = df['Date'].apply(util.convert_date)
    df.set_index(['Date'], inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    return df


def _create_feature(site_info_list):
    geometry = Point((float(site_info_list[0].strip()), float(site_info_list[1].strip())))
    site_type_code = site_info_list[3].replace('"', '').strip()
    site_props = _parse_site_str(site_info_list[2])
    site_props['parameter'] = _get_parameter(site_type_code)
    site_props['source'] = _get_source(site_type_code)
    site_props['water_body'] = _get_water_body(site_type_code)
    site_props['real_time'] = _real_time(site_type_code)
    return Feature(geometry=geometry, properties=site_props)


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


def _get_source(site_type_code):
    internal_source_abbr = {
        'LCLC': 'LCRA',
        'LCUC': 'UCRA',
        'LCCW': 'CRMWD',
        'LCAU': 'COA',
        'WCFO': 'TCEQ'
    }
    if site_type_code not in internal_source_abbr.keys():
        return None
    return source_map.get(internal_source_abbr[site_type_code])


def _get_parameter(site_type_code):
    if site_type_code == 'Salinity' or site_type_code == 'Conductivity':
        return site_type_code
    else:
        return None


def _get_water_body(site_type_code):
    if site_type_code == 'Bay':
        return 'Bay'
    else:
        return None


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


def _parse_site_str(site_str):
    site_code = site_str.split('<br />')[0].replace('"', '')\
        .replace('Site', '').replace('Number', '').replace(':', '').strip()
    site_description = site_str.split('<br />')[1].strip('"')
    return dict(site_code=site_code, site_description=site_description)


def _real_time(site_type_code):
    if site_type_code == 'Salinity' or site_type_code == 'Conductivity':
        return True
    else:
        return False
