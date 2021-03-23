from __future__ import print_function
from datetime import datetime
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from ulmo.noaa import goes
import test_util

message_test_sets = [
    {
        'dcp_address': 'C5149430',
        'parser': 'twdb_stevens',
        'message_timestamp': "/Date(1559316497303)/",
    },
    {
        'dcp_address': 'C514D73A',
        'parser': 'twdb_sutron',
        'message_timestamp': "/Date(1559158095000)/",
    },
    {
        'dcp_address': 'C516C1B8',
        'parser': 'stevens',
        'message_timestamp': "/Date(1559569431753)/",
    }
]


def test_parse_dcp_message_timestamp():
    for test_set in message_test_sets:
        dcp_data_file = 'noaa/goes/' + test_set['dcp_address'] + '.txt'
        with test_util.mocked_urls(dcp_data_file, force=True):
            data = goes.get_data(test_set['dcp_address'], hours=12)
            assert data['message_timestamp_utc'][-1] == datetime.fromtimestamp(
                int(test_set['message_timestamp'].strip('/Date()'))/1000
            )
        assert data['message_timestamp_utc'][-1] == datetime.fromtimestamp(
            int(test_set['message_timestamp'].strip('/Date()'))/1000
        )


twdb_stevens_test_sets = [
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': '"BV:11.9  193.76$ 193.70$ 193.62$ 193.54$ 193.49$ 193.43$ 193.37$ 199.62$ 200.51$ 200.98$ 195.00$ 194.33$ ',
        'dcp_address': '',
        'return_value': [
            ['2013-10-30 15:00:00', 'bv', 11.90],
            ['2013-10-30 15:00:00', 'wl', 193.76],
            ['2013-10-30 14:00:00', 'wl', 193.70],
            ['2013-10-30 13:00:00', 'wl', 193.62],
            ['2013-10-30 12:00:00', 'wl', 193.54],
            ['2013-10-30 11:00:00', 'wl', 193.49],
            ['2013-10-30 10:00:00', 'wl', 193.43],
            ['2013-10-30 09:00:00', 'wl', 193.37],
            ['2013-10-30 08:00:00', 'wl', 199.62],
            ['2013-10-30 07:00:00', 'wl', 200.51],
            ['2013-10-30 06:00:00', 'wl', 200.98],
            ['2013-10-30 05:00:00', 'wl', 195.00],
            ['2013-10-30 04:00:00', 'wl', 194.33],
        ],
    },
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': '"BV:12.6  Channel:5 Time:28 +304.63 +304.63 +304.63 +304.56 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.71 Channel:6 Time:28 +310.51 +310.66 +310.59 +310.51 +310.51 +310.59 +310.59 +310.51 +310.66 +310.51 +310.66 +310.59 ',
        'dcp_address': '',
        'return_value': [
            ['2013-10-30 15:00:00', 'bv', 12.60],
            ['2013-10-30 15:00:00', 'time', 28.00],
            ['2013-10-30 15:00:00', 'time', 28.00],
            ['2013-10-30 15:00:00', '5', 304.63],
            ['2013-10-30 14:00:00', '5', 304.63],
            ['2013-10-30 13:00:00', '5', 304.63],
            ['2013-10-30 12:00:00', '5', 304.56],
            ['2013-10-30 11:00:00', '5', 304.63],
            ['2013-10-30 10:00:00', '5', 304.63],
            ['2013-10-30 09:00:00', '5', 304.63],
            ['2013-10-30 08:00:00', '5', 304.63],
            ['2013-10-30 07:00:00', '5', 304.63],
            ['2013-10-30 06:00:00', '5', 304.63],
            ['2013-10-30 05:00:00', '5', 304.63],
            ['2013-10-30 04:00:00', '5', 304.71],
            ['2013-10-30 15:00:00', '6', 310.51],
            ['2013-10-30 14:00:00', '6', 310.66],
            ['2013-10-30 13:00:00', '6', 310.59],
            ['2013-10-30 12:00:00', '6', 310.51],
            ['2013-10-30 11:00:00', '6', 310.51],
            ['2013-10-30 10:00:00', '6', 310.59],
            ['2013-10-30 09:00:00', '6', 310.59],
            ['2013-10-30 08:00:00', '6', 310.51],
            ['2013-10-30 07:00:00', '6', 310.66],
            ['2013-10-30 06:00:00', '6', 310.51],
            ['2013-10-30 05:00:00', '6', 310.66],
            ['2013-10-30 04:00:00', '6', 310.59],
        ]
    },
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': '"BV:12.6 ',
        'dcp_address': '',
        'return_value': [
            ['2013-10-30 15:00:00', 'bv', 12.60],
        ]
    },
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': """79."$}X^pZBF8iB~i>>Xmj[bvr^Zv%JXl,DU=l{uu[ time(|@2q^sjS!""",
        'dcp_address': '',
        'return_value': pd.DataFrame()
    },
]


def test_parser_twdb_stevens():
    for test_set in twdb_stevens_test_sets:
        print('testing twdb_stevens parser')

        if isinstance(test_set['return_value'], pd.DataFrame):
            parser = getattr(goes.parsers, 'twdb_stevens')
            assert_frame_equal(pd.DataFrame(), parser(test_set))
            return
        else:
            columns = ['timestamp_utc', 'channel', 'channel_data']
        _assert(test_set, columns, 'twdb_stevens')


twdb_sutron_test_sets = [
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': '":Sense01 60 #60 -67.84 -66.15 -67.73 -67.81 -66.42 -68.45 -68.04 -67.87 -71.53 -73.29 -70.55 -72.71 :BL 13.29',
        'return_value': [
            ['2013-10-30 15:00:00', 'sense01', 67.84],
            ['2013-10-30 14:00:00', 'sense01', 66.15],
            ['2013-10-30 13:00:00', 'sense01', 67.73],
            ['2013-10-30 12:00:00', 'sense01', 67.81],
            ['2013-10-30 11:00:00', 'sense01', 66.42],
            ['2013-10-30 10:00:00', 'sense01', 68.45],
            ['2013-10-30 09:00:00', 'sense01', 68.04],
            ['2013-10-30 08:00:00', 'sense01', 67.87],
            ['2013-10-30 07:00:00', 'sense01', 71.53],
            ['2013-10-30 06:00:00', 'sense01', 73.29],
            ['2013-10-30 05:00:00', 'sense01', 70.55],
            ['2013-10-30 04:00:00', 'sense01', 72.71],
            ['2013-10-30 03:00:00', 'sense01', np.nan],
            ['2013-10-30 15:00:00', 'bl', np.nan],
            ['2013-10-30 14:00:00', 'bl', 13.29],
        ],
    },
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': '":OTT 703 60 #60 -231.47 -231.45 -231.44 -231.45 -231.47 -231.50 -231.51 -231.55 -231.56 -231.57 -231.55 -231.53 :6910704 60 #60 -261.85 -261.83 -261.81 -261.80 -261.81 -261.83 -261.85 -261.87 -261.89 -261.88 -261.86 -261.83 :BL 13.21',
        'return_value': [
            ['2013-10-30 15:00:00', 'ott', np.nan],
            ['2013-10-30 14:00:00', 'ott', 231.47],
            ['2013-10-30 13:00:00', 'ott', 231.45],
            ['2013-10-30 12:00:00', 'ott', 231.44],
            ['2013-10-30 11:00:00', 'ott', 231.45],
            ['2013-10-30 10:00:00', 'ott', 231.47],
            ['2013-10-30 09:00:00', 'ott', 231.50],
            ['2013-10-30 08:00:00', 'ott', 231.51],
            ['2013-10-30 07:00:00', 'ott', 231.55],
            ['2013-10-30 06:00:00', 'ott', 231.56],
            ['2013-10-30 05:00:00', 'ott', 231.57],
            ['2013-10-30 04:00:00', 'ott', 231.55],
            ['2013-10-30 03:00:00', 'ott', 231.53],
            ['2013-10-30 02:00:00', 'ott', np.nan],
            ['2013-10-30 15:00:00', '6910704', 261.85],
            ['2013-10-30 14:00:00', '6910704', 261.83],
            ['2013-10-30 13:00:00', '6910704', 261.81],
            ['2013-10-30 12:00:00', '6910704', 261.80],
            ['2013-10-30 11:00:00', '6910704', 261.81],
            ['2013-10-30 10:00:00', '6910704', 261.83],
            ['2013-10-30 09:00:00', '6910704', 261.85],
            ['2013-10-30 08:00:00', '6910704', 261.87],
            ['2013-10-30 07:00:00', '6910704', 261.89],
            ['2013-10-30 06:00:00', '6910704', 261.88],
            ['2013-10-30 05:00:00', '6910704', 261.86],
            ['2013-10-30 04:00:00', '6910704', 261.83],
            ['2013-10-30 03:00:00', '6910704', np.nan],
            ['2013-10-30 15:00:00', 'bl', np.nan],
            ['2013-10-30 14:00:00', 'bl', 13.21],
        ]
    },
]


def test_parser_twdb_sutron():
    for test_set in twdb_sutron_test_sets:
        print('testing twdb_sutron parser')
        columns = ['timestamp_utc', 'channel', 'channel_data']
        _assert(test_set, columns, 'twdb_sutron')


twdb_texuni_test_sets = [
    {
        'message_timestamp_utc': datetime(2013, 10, 30, 15, 28, 18),
        'dcp_message': ' \r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+340.0,+2013.,+307.0,+1400.,+12.07,+0.000,-109.9,-109.8,-110.1,+30.57,',
        'return_value': [
            ['2013-10-30 15:00:00', 'wl', 109.8],
            ['2013-10-30 14:00:00', 'wl', 109.8],
            ['2013-10-30 13:00:00', 'wl', 109.8],
            ['2013-10-30 12:00:00', 'wl', 109.8],
            ['2013-10-30 11:00:00', 'wl', 109.8],
            ['2013-10-30 10:00:00', 'wl', 109.9],
            ['2013-10-30 09:00:00', 'wl', 109.9],
            ['2013-10-30 08:00:00', 'wl', 109.9],
            ['2013-10-30 07:00:00', 'wl', 109.9],
            ['2013-10-30 06:00:00', 'wl', 109.9],
            ['2013-10-30 05:00:00', 'wl', 110.0],
            ['2013-10-30 04:00:00', 'wl', 110.0],
            ['2013-10-30 03:00:00', 'wl', 109.9],
            ['2013-10-30 02:00:00', 'wl', 109.9],
            ['2013-10-30 01:00:00', 'wl', 109.9],
            ['2013-10-30 00:00:00', 'wl', 109.9],
            ['2013-10-29 23:00:00', 'wl', 110.0],
            ['2013-10-29 22:00:00', 'wl', 110.0],
            ['2013-10-29 21:00:00', 'wl', 110.0],
            ['2013-10-29 20:00:00', 'wl', 110.1],
            ['2013-10-29 19:00:00', 'wl', 110.1],
            ['2013-10-29 18:00:00', 'wl', 110.1],
            ['2013-10-29 17:00:00', 'wl', 110.1],
            ['2013-10-29 16:00:00', 'wl', 110.1],
        ]
    },
]


def test_parser_twdb_texuni():
    for test_set in twdb_texuni_test_sets:
        print('testing twdb_texuni parser')
        columns = ['timestamp_utc', 'channel', 'channel_data']
        _assert(test_set, columns, 'twdb_texuni')


twdb_fts_test_sets = [
    {
        'message_timestamp_utc': datetime(2018, 2, 6, 13, 36, 14),
        'dcp_message': ':WL 31 #60 -72.90 -72.88 -72.87 -72.87 -72.87 ' +
                       '-72.87 -72.88 -72.88 -72.87 -72.87 -72.87 -72.85 ',
        'return_value': [
            ['2018-02-06 13:00:00', 'wl', 72.90],
            ['2018-02-06 12:00:00', 'wl', 72.88],
            ['2018-02-06 11:00:00', 'wl', 72.87],
            ['2018-02-06 10:00:00', 'wl', 72.87],
            ['2018-02-06 09:00:00', 'wl', 72.87],
            ['2018-02-06 08:00:00', 'wl', 72.87],
            ['2018-02-06 07:00:00', 'wl', 72.88],
            ['2018-02-06 06:00:00', 'wl', 72.88],
            ['2018-02-06 05:00:00', 'wl', 72.87],
            ['2018-02-06 04:00:00', 'wl', 72.87],
            ['2018-02-06 03:00:00', 'wl', 72.87],
            ['2018-02-06 02:00:00', 'wl', 72.85],
        ]
    },
    {
        'message_timestamp_utc': datetime(2020, 1, 14, 13, 36, 14),
        'dcp_message': '":vb 119 #72 13.00 :wl 59 #60 -217.66 -217.66 ' +
                       '-217.64 -217.60 -217.56 -217.51 -217.45 -217.40 ' +
                       '-217.38 -217.39 -217.41 -217.47',
        'return_value': [
            ['2020-01-14 13:00:00', 'vb', 13.0],
            ['2020-01-14 13:00:00', 'wl', 217.66],
            ['2020-01-14 12:00:00', 'wl', 217.66],
            ['2020-01-14 11:00:00', 'wl', 217.64],
            ['2020-01-14 10:00:00', 'wl', 217.60],
            ['2020-01-14 09:00:00', 'wl', 217.56],
            ['2020-01-14 08:00:00', 'wl', 217.51],
            ['2020-01-14 07:00:00', 'wl', 217.45],
            ['2020-01-14 06:00:00', 'wl', 217.40],
            ['2020-01-14 05:00:00', 'wl', 217.38],
            ['2020-01-14 04:00:00', 'wl', 217.39],
            ['2020-01-14 03:00:00', 'wl', 217.41],
            ['2020-01-14 02:00:00', 'wl', 217.47],
        ]
    },
    {
        'message_timestamp_utc': datetime(2019, 12, 6, 1, 0, 0),
        'dcp_message': '"Operator Initiated Test Transmission: Operator' +
                       'Initiated Test Transmission: Operator Initiated Test' +
                       'Transmission: Operator Initiated Test Transmission: ' +
                       'Operator Initiated Test Transmission: Operator ' +
                       'Initiated Test Transmission: Operator Initiated ' +
                       'Test Transmission: Operator Initiated Test ' +
                       'Transmission: Operator Initiated Test Transmission: ' +
                       'Operator Initiated Test Transmission:',
        'return_value': [
            ['2019-12-06 01:00:00', np.nan, np.nan],
        ]
    },
]


def test_parser_twdb_fts():
    for test_set in twdb_fts_test_sets:
        print('testing twdb_fts parser')
        columns = ['timestamp_utc', 'channel', 'channel_data']
        _assert(test_set, columns, 'twdb_fts')


def _assert(test_set, columns, parser):
    expected = pd.DataFrame(test_set['return_value'], columns=columns)
    expected.index = pd.to_datetime(expected['timestamp_utc'])
    del expected['timestamp_utc']
    parser = getattr(goes.parsers, parser)
    df = parser(test_set)
    print('Expected:')
    print(expected)
    print('Actual:')
    print(df)
    # to compare pandas dataframes, columns must be in same order
    if 'channel' in df.columns:
        for channel in np.unique(df['channel']):
            df_c = df[df['channel'] == channel]
            expected_c = expected[expected['channel'] == channel]
            assert_frame_equal(
                df_c.sort_index(axis=1).sort_index(axis=0),
                expected_c.sort_index(axis=1).sort_index(axis=0)
            )
    else:
        assert_frame_equal(
            df.sort_index(axis=1).sort_index(axis=0),
            expected.sort_index(axis=1).sort_index(axis=0)
        )
