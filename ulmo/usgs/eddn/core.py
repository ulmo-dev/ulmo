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

from collections import OrderedDict
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import isodate
import pandas as pd
import re
import requests
from ulmo import util
from . import parsers

# eddn query base url
EDDN_URL = 'http://eddn.usgs.gov/cgi-bin/retrieveData.pl?%s'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/eddn/'


def decode(dataframe, parser, **kwargs):
    if isinstance(parser, basestring):
        parser = getattr(parsers, parser)

    df = []
    for timestamp, data in dataframe.iterrows():
        df.append(parser(data, **kwargs))

    df = pd.concat(df)
    return df
    

def get_data(dcp_address, start=None, end=None, networklist='', channel='', spacecraft='Any', baud='Any', 
        electronic_mail='', dcp_bul='', glob_bul='', timing='', retransmitted='Y', daps_status='N', 
        path=None, update_cache=True):

    dcp_data_path = _get_store_path(path, dcp_address + '.h5')
    
    if os.path.exists(dcp_data_path):
        data = pd.read_hdf(dcp_data_path, dcp_address)
    else:
        data = pd.DataFrame()
        if not update_cache:
            print 'no cached data available for DCP address %s, setting update_cache to True\n' %dcp_address
            update_cache = True

    if update_cache:
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

        r = requests.get(EDDN_URL, params=params)
        print 'new data retrieved using url: %s\n' % r.url
        soup = BeautifulSoup(r.text)
        message = soup.find('pre').contents[0].strip('\n')

        if 'Max data limit reached' in message[-1]:
            print 'Max data limit reached, returning available data, try using a smaller time range\n'

        message = [msg[1].strip() for msg in re.findall('(//START)(.*?)(//END)', message, re.M|re.S)]
        
        new_data = pd.DataFrame([_parse(row) for row in message])
        new_data.index = new_data.message_timestamp_utc

        data = new_data.combine_first(data)

        data.to_hdf(dcp_data_path, dcp_address)

    if start:
        if start.startswith('P'):
            start = data['message_timestamp_utc'][-1] - isodate.parse_duration(start)

        data = data[start:]

    if end:
        if end.startswith('P'):
            end = data['message_timestamp_utc'][-1] - isodate.parse_duration(end)
            
        data = data[:end]

    return data


def _format_period(period):
    days, hours, minutes = period.days, period.seconds//3600, (period.seconds//60)%60

    if minutes:
        return 'now -%s minutes' % period.seconds/60

    if hours:
        return 'now -%s hours' % period.seconds/3600

    if days:
        return 'now -%s days' % days


def _format_time(timestamp):

    if isinstance(timestamp, basestring):
        if timestamp.startswith('P'):
            timestamp = isodate.parse_duration(timestamp)
        else:
            timestamp = isodate.parse_datetime(timestamp)


    if isinstance(timestamp, datetime):
        return datetime.strftime('%Y/%j %H:%M:%S')
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
