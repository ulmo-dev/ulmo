from datetime import datetime, timedelta
import requests
import pandas as pd
from . import parsers
import os
from ulmo import util
import isodate
import shutil
import logging


dcs_url = 'https://dcs1.noaa.gov/Account/FieldTestData'

DEFAULT_FILE_PATH = 'noaa/goes/'

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def decode(dataframe, parser, **kwargs):
    """decodes goes message data in pandas dataframe returned by
    ulmo.noaa.goes.get_data().

    Parameters
    ----------
    dataframe : pandas.DataFrame
        pandas.DataFrame returned by ulmo.noaa.goes.get_data()
    parser : {function, str}
        function that acts on dcp_message each row of the dataframe and returns
        a new dataframe containing several rows of decoded data. This returned
        dataframe may have different (but derived) timestamps than that the
        original row. If a string is passed then a matching parser function is
        looked up from ulmo.noaa.goes.parsers

    Returns
    -------
    decoded_data : pandas.DataFrame
        pandas dataframe, the format and parameters in the returned dataframe
        depend wholly on the parser used

    """
    if isinstance(parser, str):
        parser = getattr(parsers, parser)

    if dataframe.empty:
        return dataframe

    df = []
    for timestamp, data in dataframe.iterrows():
        parsed = parser(data, **kwargs)
        parsed.dropna(how='all', inplace=True)
        if parsed.empty:
            empty_df = pd.DataFrame()
            df.append(empty_df)
        df.append(parsed)

    df = pd.concat(df)
    # preserve metadata in df if it exists, since pivot will lose it
    df_save = df.drop(['channel', 'channel_data'], axis=1)
    df = df.pivot_table(
        index=df.index, columns='channel', values='channel_data'
    ).join(df_save)

    # to properly drop duplicate rows, need to include index; unfortunately,
    df['idx'] = df.index.values
    df = df.drop_duplicates().drop('idx', axis=1)
    return df


def get_data(dcp_address, hours, use_cache=False, cache_path=None,
             as_dataframe=True):
    """Fetches GOES Satellite DCP messages from NOAA Data Collection System
    (DCS) field test.

    Parameters
    ----------
    dcp_address : str, iterable of strings
        DCP address or list of DCP addresses to be fetched; lists will be
        joined by a ','.
    use_cache : bool,
        If True (default) use hdf file to cache data and retrieve new data on
        subsequent requests
    cache_path : {``None``, str},
        If ``None`` use default ulmo location for cached files otherwise use
        specified path. files are named using dcp_address.
    as_dataframe : bool
        If True (default) return data in a pandas dataframe otherwise return a
        dict.

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
    params = {}
    params['addr'] = dcp_address,
    params['hours'] = hours,

    messages = _fetch_url(params)
    new_data = pd.DataFrame([_parse(row) for row in messages])

    if not new_data.empty:
        new_data.index = new_data.message_timestamp_utc
        data = new_data.combine_first(data)
        data.sort_index(inplace=True)
        if use_cache:
            # write to a tmp file and move to avoid ballooning h5 file
            tmp = dcp_data_path + '.tmp'
            data.to_hdf(tmp, dcp_address)
            shutil.move(tmp, dcp_data_path)

    if data.empty:
        if as_dataframe:
            return data
        else:
            return {}

    if not as_dataframe:
        data = data.T.to_dict()
    return data


def _fetch_url(params):
    r = requests.post(dcs_url, params=params, timeout=60)
    messages = r.json()
    return messages


def _format_period(period):
    days, hours, minutes = period.days, period.seconds // 3600, \
                           (period.seconds // 60) % 60

    if minutes:
        return 'now -%s minutes' % period.seconds / 60

    if hours:
        return 'now -%s hours' % period.seconds / 3600

    if days:
        return 'now -%s days' % days


def _format_time(timestamp):

    if isinstance(timestamp, str):
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


def _parse(entry):
    return {
        'dcp_address': entry['TblDcpDataAddrCorr'],
        'message_timestamp_utc': datetime.fromtimestamp(
            int(entry['TblDcpDataDtMsgCar'].strip('/Date()'))/1000
        ),
        'failure_code': entry['TblDcpDataProcessInfo'],
        'signal_strength': entry['TblDcpDataSigStrength'],
        'goes_receive_channel': entry['TblDcpDataChan'],
        'message_data_length': entry['TblDcpDataDataLen'],
        'dcp_message': entry['TblDcpDataData'],
    }
