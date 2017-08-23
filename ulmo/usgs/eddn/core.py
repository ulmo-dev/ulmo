"""
    ulmo.usgs.eddn.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `United States Geological
    Survey`_ `Emergency Data Distribution Network`_ web site.

    The `DCP message format`_ includes some header information that is parsed and
    the message body, with a variable number of characters. The format of the
    message body varies widely depending on the manufacturer of the transmitter,
    data logger, sensors, and the technician who programmed the DCP. The body can
    be simple ASCII, sometime with parameter codes and time-stamps embedded,
    sometimes not. The body can also be in 'Pseudo-Binary' which is character
    encoding of binary data that uses 6 bits of every byte and guarantees that
    all characters are printable.


    .. _United States Geological Survey: http://www.usgs.gov/
    .. _Emergency Data Distribution Network: http://eddn.usgs.gov/
    .. _http://eddn.usgs.gov/dcpformat.html

"""
from past.builtins import basestring

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import isodate
import logging
import os
import pandas as pd
import re
import requests
import shutil
from ulmo import util

from . import parsers

# eddn query base url
EDDN_URL = 'http://eddn.usgs.gov/cgi-bin/retrieveData.pl?%s'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/eddn/'

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def decode(dataframe, parser, **kwargs):
    """decodes dcp message data in pandas dataframe returned by ulmo.usgs.eddn.get_data().

    Parameters
    ----------
    dataframe : pandas.DataFrame
        pandas.DataFrame returned by ulmo.usgs.eddn.get_data()
    parser : {function, str}
        function that acts on dcp_message each row of the dataframe and returns a new dataframe
        containing several rows of decoded data. This returned dataframe may have different
        (but derived) timestamps than that the original row. If a string is passed then a matching
        parser function is looked up from ulmo.usgs.eddn.parsers

    Returns
    -------
    decoded_data : pandas.DataFrame
        pandas dataframe, the format and parameters in the returned dataframe depend wholly on the parser used

    """
    if isinstance(parser, basestring):
        parser = getattr(parsers, parser)

    df = []
    for timestamp, data in dataframe.iterrows():
        parsed = parser(data, **kwargs)
        parsed.dropna(how='all', inplace=True)
        if not parsed.empty:
            df.append(parsed)

    df = pd.concat(df)
    return df


def get_data(
        dcp_address, start=None, end=None, networklist='', channel='', spacecraft='Any', baud='Any',
        electronic_mail='', dcp_bul='', glob_bul='', timing='', retransmitted='Y', daps_status='N',
        use_cache=False, cache_path=None, as_dataframe=True):
    """Fetches GOES Satellite DCP messages from USGS Emergency Data Distribution Network.

    Parameters
    ----------
    dcp_address : str, iterable of strings
        DCP address or list of DCP addresses to be fetched; lists will be joined by a ','.
    start : {``None``, str, datetime, datetime.timedelta}
        If ``None`` (default) then the start time is 2 days prior (or date of last data if cache is used)
        If a datetime or datetime like string is specified it will be used as the start date.
        If a timedelta or string in ISO 8601 period format (e.g 'P2D' for a period of 2 days) then
        'now' minus the timedelta will be used as the start.
        NOTE: The EDDN service does not specify how far back data is available. The service also imposes
        a maximum data limit of 25000 character. If this is limit reached multiple requests will be made 
        until all available data is downloaded. 
    end : {``None``, str, datetime, datetime.timedelta}
        If ``None`` (default) then the end time is 'now'
        If a datetime or datetime like string is specified it will be used as the end date.
        If a timedelta or string in ISO 8601 period format (e.g 'P2D' for a period of 2 days) then
        'now' minus the timedelta will be used as the end.
        NOTE: The EDDN service does not specify how far back data is available. The service also imposes
        a maximum data limit of 25000 character.
    networklist : str,
        '' (default). Filter by network.
    channel : str,
        '' (default). Filter by channel.
    spacecraft : str,
        East, West, Any (default). Filter by GOES East/West Satellite
    baud : str,
        'Any' (default). Filter by baud rate. See http://eddn.usgs.gov/msgaccess.html for options
    electronic_mail : str,
        '' (default) or 'Y'
    dcp_bul : str,
        '' (default) or 'Y'
    glob_bul : str,
        '' (default) or 'Y'
    timing : str,
        '' (default) or 'Y'
    retransmitted : str,
        'Y' (default) or 'N'
    daps_status : str,
        'N' (default) or 'Y'
    use_cache : bool,
        If True (default) use hdf file to cache data and retrieve new data on subsequent requests
    cache_path : {``None``, str},
        If ``None`` use default ulmo location for cached files otherwise use specified path. files are named
        using dcp_address.
    as_dataframe : bool
        If True (default) return data in a pandas dataframe otherwise return a dict.

    Returns
    -------
    message_data : {pandas.DataFrame, dict}
        Either a pandas dataframe or a dict indexed by dcp message times
    """

    if isinstance(dcp_address, list):
        dcp_address = ','.join(dcp_address)

    data = pd.DataFrame()

    if use_cache:
        dcp_data_path = _get_store_path(cache_path, dcp_address + '.h5')
        if os.path.exists(dcp_data_path):
            data = pd.read_hdf(dcp_data_path, dcp_address)

    if start:
        drs_since = _format_time(start)
    else:
        try:
            drs_since = _format_time(data['message_timestamp_utc'][-1])
        except:
            drs_since = 'now -2 days'

    if end:
        drs_until = _format_time(end)
    else:
        drs_until = 'now'

    params = {}
    params['DCP_ADDRESS'] = dcp_address
    params['DRS_SINCE'] = drs_since
    params['DRS_UNTIL'] = drs_until
    params['NETWORKLIST'] = networklist
    params['CHANNEL'] = channel
    params['BEFORE'] = '//START\n',
    params['AFTER'] = '\n//END\n',
    params['SPACECRAFT'] = spacecraft
    params['BAUD'] = baud
    params['ELECTRONIC_MAIL'] = electronic_mail
    params['DCP_BUL'] = dcp_bul
    params['GLOB_BUL'] = glob_bul
    params['TIMING'] = timing
    params['RETRANSMITTED'] = retransmitted
    params['DAPS_STATUS'] = daps_status

    data_limit_reached = True
    messages = []
    while data_limit_reached:
        new_message, data_limit_reached =  _fetch_url(params)
        messages += new_message
        if data_limit_reached:
            params['DRS_UNTIL'] = _format_time(_parse(new_message[-1])['message_timestamp_utc'])

    new_data = pd.DataFrame([_parse(row) for row in messages])

    if not new_data.empty:
        new_data.index = new_data.message_timestamp_utc
        data = new_data.combine_first(data)
        data.sort_index(inplace=True)

        if use_cache:
            #write to a tmp file and move to avoid ballooning h5 file
            tmp = dcp_data_path + '.tmp'
            data.to_hdf(tmp, dcp_address)
            shutil.move(tmp, dcp_data_path)

    if data.empty:
        if as_dataframe:
            return data
        else:
            return {}

    if start:
        if start.startswith('P'):
            start = data['message_timestamp_utc'][-1] - isodate.parse_duration(start)

        data = data[start:]

    if end:
        if end.startswith('P'):
            end = data['message_timestamp_utc'][-1] - isodate.parse_duration(end)

        data = data[:end]

    if not as_dataframe:
        data = data.T.to_dict()

    return data


def _fetch_url(params):
    r = requests.get(EDDN_URL, params=params)
    log.info('data requested using url: %s\n' % r.url)
    soup = BeautifulSoup(r.text)
    message = soup.find('pre').contents[0].replace('\n', '').replace('\r', ' ')

    data_limit_reached = False
    if 'Max data limit reached' in message:
        data_limit_reached = True
        log.info('Max data limit reached, making new request for older data\n')

    if not message:
        log.info('No data found\n')
        message = []
    else:
        message = [msg[1].strip() for msg in re.findall('(//START)(.*?)(//END)', message, re.M | re.S)]

    return message, data_limit_reached


def _format_period(period):
    days, hours, minutes = period.days, period.seconds // 3600, (period.seconds // 60) % 60

    if minutes:
        return 'now -%s minutes' % period.seconds / 60

    if hours:
        return 'now -%s hours' % period.seconds / 3600

    if days:
        return 'now -%s days' % days


def _format_time(timestamp):

    if isinstance(timestamp, basestring):
        if timestamp.startswith('P'):
            timestamp = isodate.parse_duration(timestamp)
        else:
            timestamp = isodate.parse_datetime(timestamp)

    if isinstance(timestamp, datetime):
        return timestamp.strftime('%Y/%j %H:%M:%S')
    elif isinstance(timestamp, timedelta):
        return _format_period(timestamp)


def _get_store_path(path, default_file_name):
    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, default_file_name)


def _parse(line):
    return {
        'dcp_address': line[:8],
        'message_timestamp_utc': datetime.strptime(line[8:19], '%y%j%H%M%S'),
        'failure_code': line[19:20],
        'signal_strength': line[20:22],
        'frequency_offset': line[22:24],
        'modulation_index': line[24:25],
        'data_quality_indicator': line[25:26],
        'goes_receive_channel': line[26:29],
        'goes_spacecraft_indicator': line[29:30],
        'uplink_carrier_status': line[30:32],
        'message_data_length': line[32:37],
        'dcp_message': line[37:],
    }
