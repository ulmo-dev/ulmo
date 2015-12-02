from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
import logging
import requests
import pandas

from ulmo import util

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

data_url = 'http://hydromet.lcra.org/chronhist.aspx'

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


def get_sites(parameter_code):
    """Gets list of the hydromet site codes and description for site that have
    the parameter ``parameter_code``
    Parameters:
    -----------
    parameter_code : str
        LCRA parameter code. see ``PARAMETERS``
    Returns
    -------
    sites_dict: dict
        a python dict with site codes mapped to site information
    """
    sites_base_url = 'http://hydromet.lcra.org/navgagelist.asp?Stype=%s'
    # the url doesn't provide list of sites for the following parameters but
    # they are available with the paired parameter. e.g., flow is available
    #at stage sites.
    if parameter_code == 'winddir':
        parameter_code = 'windsp'
    if parameter_code == 'flow':
        parameter_code = 'stage'
    if parameter_code == 'tds':
        parameter_code = 'cndvty'

    if parameter_code not in PARAMETERS.keys():
        return {}

    res = requests.get(sites_base_url % parameter_code)
    soup = BeautifulSoup(res.content, 'html')
    sites_str = [
        site.text.replace('&nbsp', '').replace(u'\xa0', '') for site
        in soup.findAll('a')]
    sites_dict = dict([(s[:6], s[7:]) for s in sites_str])

    return sites_dict


def get_site_data(site_code, parameter_code, as_dataframe=True,
                  start_date=None, end_date=None):
    """Fetches site's parameter data
    Parameters
    ----------
    site_code : str
        The LCRA site code of the site you want to query data for.
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

    Returns
    -------
    df : pandas.DataFrame
    values_dict : dict or
    """
    parameter_code = parameter_code.upper()
    if parameter_code.lower() not in PARAMETERS.keys():
        log.info('%s is not an LCRA parameter' % parameter_code)
        return None
    initial_request = requests.get(data_url)
    if initial_request.status_code != 200:
        return None
    list_request_headers = {
        '__EVENTTARGET': 'DropDownList1',
        'DropDownList1': site_code[:4],
    }
    list_request = _make_next_request(data_url, initial_request, list_request_headers)
    if list_request.status_code != 200:
        return None

    if parameter_code == 'STAGE':
        if site_code[-2:] == '05':
            parameter_code = 'HEAD'
        elif site_code[-2:] == '07':
            parameter_code = 'TAIL'
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


def _values_dict_to_df(values_dict):
    if not len(values_dict):
        return pandas.DataFrame({})
    df = pandas.DataFrame(values_dict)
    df.index = df['Date - Time'].apply(util.convert_datetime)
    df.drop('Date - Time', axis=1, inplace=True)
    df.sort_index(inplace=True)
    return df


def _get_row_values(row, columns):
    value_els = row.findAll('td')
    values = [value_el.get_text() for value_el in value_els]
    return dict(zip(columns, values))


def _get_data(site_code, parameter_code, list_request, start, end):
    data_request_headers = {
        'Date1': start.strftime('%m/%d/%Y'),
        'Date2': end.strftime('%m/%d/%Y'),
        'DropDownList1': site_code
    }

    data_request_headers['DropDownList2'] = parameter_code
    data_request = _make_next_request(
        data_url, list_request, data_request_headers)

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
