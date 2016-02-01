"""
    ulmo.lcra.hydromet.core
    ~~~~~~~~~~~~~~~~~~~~~~~
    This module provides access to hydrologic and climate data in the Colorado
    River Basin (Texas) provided by the `Lower Colorado River Authority`_
    `Hydromet`_ web site and web service.
    .. _Lower Colorado River Authority: http://www.lcra.org
    .. _Hydromet: http://hydromet.lcra.org
"""
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
from geojson import Point, Feature, FeatureCollection
import logging
import requests
import pandas

from ulmo import util

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

historical_data_url = 'http://hydromet.lcra.org/chronhist.aspx'
current_data_url = 'http://hydrometdata.lcra.org'
PARAMETERS = {
    'stage': 'the level of water above a benchmark in feet',
    'flow': 'streamflow in cubic feet per second',
    'pc': 'precipitation in inches',
    'temp': 'air temperature in degrees fahrenheit',
    'rhumid': 'air relative humidity as percentage',
    'cndvty': 'water electrical conductivity in micromhos',
    'tds': 'total suspended solids',
    'windsp': 'wind speed, miles per hour',
    'winddir': 'wind direction in degrees azimuth'
}

current_data_services = ['GetLowerBasin', 'GetUpperBasin']

# in the site list by parameter web page, in order to make distinction between
# stage measurements in lake and stream, the LCRA uses 'stage' for stream sites
# and 'lake' for lake sites
site_types = PARAMETERS.copy()
site_types.update({'lake': 'stage measurement in lakes'})

# for this dam sites, stage is named head or tail
dam_sites = ['1995', '1999', '2958', '2999', '3963', '3999']


def get_sites_by_type(site_type):
    """Gets list of the hydromet site codes and description for site.
    Parameters:
    -----------
    site_type : str
        In all but lake sites, this is the parameter code collected at the site.
        For lake sites, it is 'lake'. See ``site_types`` and ``PARAMETERS``
    Returns
    -------
    sites_dict: dict
        A python dict with four char long site codes mapped to site information.
    """
    sites_base_url = 'http://hydromet.lcra.org/navgagelist.asp?Stype=%s'
    # the url doesn't provide list of sites for the following parameters but
    # they are available with the paired parameter. e.g., flow is available
    #at stage sites.
    if site_type == 'winddir':
        site_type = 'windsp'
    if site_type == 'flow':
        site_type = 'stage'
    if site_type == 'tds':
        site_type = 'cndvty'

    if site_type not in site_types.keys():
        return {}

    res = requests.get(sites_base_url % site_type)
    soup = BeautifulSoup(res.content, 'html')
    sites_str = [
        site.text.replace('&nbsp', '').replace(u'\xa0', '') for site
        in soup.findAll('a')]
    sites_dict = dict([(s[:4], s[7:]) for s in sites_str])

    return sites_dict


def get_all_sites():
    """Returns list of all LCRA hydromet sites as geojson featurecollection.
    """
    sites_url = 'http://hydromet.lcra.org/data/datafull.xml'
    res = requests.get(sites_url)
    soup = BeautifulSoup(res.content, 'xml')
    rows = soup.findAll('row')
    features = [_create_feature(row) for row in rows]
    sites = FeatureCollection(features)
    return sites


def get_current_data(service, as_geojson=False):
    """fetches the current (near real-time) river stage and flow values from
    LCRA web service.
    Parameters
    ----------
    service : str
        The web service providing data. see `current_data_services`.
        Currently we have GetUpperBasin and GetLowerBasin.
    as_geojson : 'True' or 'False' (default)
        If True the data is returned as geojson featurecollection and if False
        data is returned as list of dicts.
    Returns
    -------
    current_values_dicts : a list of dicts or
    current_values_geojson : a geojson featurecollection.
    """
    request_body_template = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">\n '
        '  <soap12:Body>\n'
        '    <%s xmlns="http://hydrometdata.lcra.org" />\n'
        '  </soap12:Body> \n'
        '</soap12:Envelope>'
    )
    if service.lower() == 'getupperbasin':
        service = 'GetUpperBasin'
    elif service.lower() == 'getlowerbasin':
        service = 'GetLowerBasin'
    else:
        log.info('service %s not recognized' % service)
        return {}
    request_body = request_body_template % service
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    res = requests.post(current_data_url, data=request_body, headers=headers)
    if res.status_code != 200:
        log.info('http request failed with status code %s' % res.status_code)
        return {}
    soup = BeautifulSoup(res.content)
    sites_els = soup.findAll('cls%s' % service.lower().replace('get', ''))
    current_values_dicts = [_parse_current_values(site_el) for site_el in
                            sites_els]
    if as_geojson:
        features = []
        for value_dict in current_values_dicts:
            feature = _feature_for_values_dict(value_dict)
            if len(feature):
                features.append(feature[0])
        if len(features) != len(current_values_dicts):
            log.warn("some of the sites did not location information")
        if len(features):
            current_values_geojson = FeatureCollection(features)
            return current_values_geojson
        else:
            return {}
    else:
        return current_values_dicts


def get_site_data(site_code, parameter_code, as_dataframe=True,
                  start_date=None, end_date=None, dam_site_location='head'):
    """Fetches site's parameter data
    Parameters
    ----------
    site_code : str
        The LCRA site code (four chars long) of the site you want to query data
        for.
    parameter_code : str
        LCRA parameter code. see ``PARAMETERS``
    start_date : ``None`` or datetime
        Start of a date range for a query.
    end_date : ``None`` or datetime
        End of a date range for a query.
    as_dataframe : ``True`` (default) or ``False``
        This determines what format values are returned as. If ``True`` (default)
        then the values will be a pandas.DataFrame object with the values
        timestamp as the index. If ``False``, the format will be Python
        dictionary.
    dam_site_location : 'head' (default) or 'tail'
        The site location relative to the dam.

    Returns
    -------
    df : pandas.DataFrame or
    values_dict : dict
    """
    parameter_code = parameter_code.upper()
    if parameter_code.lower() not in PARAMETERS.keys():
        log.info('%s is not an LCRA parameter' % parameter_code)
        return None
    initial_request = requests.get(historical_data_url)
    if initial_request.status_code != 200:
        return None
    list_request_headers = {
        '__EVENTTARGET': 'DropDownList1',
        'DropDownList1': site_code,
    }
    list_request = _make_next_request(historical_data_url, initial_request, list_request_headers)
    if list_request.status_code != 200:
        return None

    if parameter_code == 'STAGE':
        if site_code in dam_sites:
            parameter_code = dam_site_location.upper()
        else:
            parameter_code = 'STAGE'
    elif parameter_code == 'RHUMID':
        parameter_code = 'Rhumid'
    #the parameter selection dropdown doesn't have flow. the data comes with stage.
    elif parameter_code == 'FLOW':
        parameter_code = 'STAGE'
    else:
        pass

    if start_date is None:
        start_date = datetime.date.today()
    if end_date is None:
        end_date = datetime.date.today() + relativedelta(days=1)
    if (end_date - start_date).days < 180:
        values_dict = _get_data(
            site_code[:4], parameter_code, list_request, start_date, end_date)
        if not values_dict:
            return None
    else:
        values_dict = []
        chunks = pandas.np.ceil((end_date - start_date).days / 180.)
        for chunk in (pandas.np.arange(chunks) + 1):
            request_start_date = start_date + relativedelta(
                days=180 * (chunk - 1))
            chunk_end_date = start_date + relativedelta(days=180 * chunk)
            if chunk_end_date >= end_date:
                request_end_date = end_date
            else:
                request_end_date = chunk_end_date
            log.info("getting chunk: %i, start: %s, end: %s, parameter: %s" % (
                chunk, request_start_date, request_end_date, parameter_code))
            values_chunk = _get_data(
                site_code[:4], parameter_code, list_request, request_start_date,
                request_end_date)
            values_dict += values_chunk

    df = _values_dict_to_df(values_dict).astype(float)

    if not as_dataframe:
        return df.to_dict('records')
    else:
        return df


def _create_feature(row):
    geometry = Point((float(row['e']), float(row['d'])))
    site_props = dict(site_code=row['a'], site_description=row['c'])
    site = Feature(geometry=geometry, properties=site_props)
    return site


def _feature_for_values_dict(site_values_dict):
    sites = get_all_sites()['features']
    site = [_update_feature_props(site, site_values_dict) for site in sites if
        site['properties']['site_description'].lower() ==
        site_values_dict['location'].lower()]
    return site


def _parse_current_values(site_el):
    site_value_els = site_el.findChildren()
    site_values = dict()
    for value_el in site_value_els:
        if value_el.name.lower() == 'datetime':
            if value_el.get_text().strip() == '':
                site_values[value_el.name.lower()] = None
            else:
                site_values[value_el.name.lower()] = util.convert_datetime(
                    value_el.get_text())
        elif value_el.name.lower() == 'location':
            site_values[value_el.name.lower()] = value_el.get_text().strip()
        else:
            if value_el.get_text().strip() == '':
                site_values[value_el.name.lower()] = None
            else:
                site_values[value_el.name.lower()] = float(value_el.get_text())
    return site_values


def _values_dict_to_df(values_dict):
    if not len(values_dict):
        return pandas.DataFrame({})
    df = pandas.DataFrame(values_dict)
    df.index = df['Date - Time'].apply(util.convert_datetime)
    df.drop('Date - Time', axis=1, inplace=True)
    df.sort_index(inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    return df


def _get_row_values(row, columns):
    value_els = row.findAll('td')
    values = [_parse_val(value_el.get_text()) for value_el in value_els]
    return dict(zip(columns, values))


def _get_data(site_code, parameter_code, list_request, start, end):
    data_request_headers = {
        'Date1': start.strftime('%m/%d/%Y'),
        'Date2': end.strftime('%m/%d/%Y'),
        'DropDownList1': site_code
    }

    data_request_headers['DropDownList2'] = parameter_code
    data_request = _make_next_request(
        historical_data_url, list_request, data_request_headers)

    if data_request.status_code != 200:
        return None

    soup = BeautifulSoup(data_request.content, 'html.parser')
    columns = [col.get_text() for col in soup.findAll('th')]
    values_dict = [_get_row_values(row, columns) for row in soup.findAll('tr')[1:]]
    return values_dict


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


def _update_feature_props(feature, props):
    if 'datetime' in props.keys():
        props['datetime'] = props['datetime'].strftime('%Y-%m-%d %H:%M:%S')
    feature_props = feature['properties']
    feature_props.update(props)
    feature['properties'] = feature_props
    return feature
