from datetime import datetime
import pandas as pd
from pandas.util.testing import assert_frame_equal
import ulmo
import ulmo.usgs.eddn.parsers as parsers
import test_util

fmt = '%y%j%H%M%S'

message_test_sets = [
    {
        'dcp_address': 'C5149430',
        'number_of_lines': 4,
        'parser': 'twdb_stevens',
        'first_row_message_timestamp_utc': datetime.strptime('13305152818', fmt),
    },
    {
        'dcp_address': 'C514D73A',
        'number_of_lines': 4,
        'parser': 'twdb_sutron',
        'first_row_message_timestamp_utc': datetime.strptime('13305072816', fmt),
    },
    {
        'dcp_address': 'C516C1B8',
        'number_of_lines': 28,
        'parser': 'stevens',
        'first_row_message_timestamp_utc': datetime.strptime('13305134352', fmt),
    }
]


def test_parse_dcp_message_number_of_lines():
    for test_set in message_test_sets:
        dcp_data_file = 'usgs/eddn/' + test_set['dcp_address'] + '.txt'
        with test_util.mocked_urls(dcp_data_file):
            data = ulmo.usgs.eddn.get_data(test_set['dcp_address'])
            assert len(data) == test_set['number_of_lines']


def test_parse_dcp_message_timestamp():
    for test_set in message_test_sets:
        dcp_data_file = 'usgs/eddn/' + test_set['dcp_address'] + '.txt'
        with test_util.mocked_urls(dcp_data_file):
            data = ulmo.usgs.eddn.get_data(test_set['dcp_address'])
            assert data['message_timestamp_utc'][-1] == test_set['first_row_message_timestamp_utc']


twdb_stevens_test_sets = [
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '"BV:11.9  193.76$ 193.70$ 193.62$ 193.54$ 193.49$ 193.43$ 193.37$ 199.62$ 200.51$ 200.98$ 195.00$ 194.33$ ',
        'return_value': [
            ['2013-10-30 15:00:00', 11.9, 194.33],
            ['2013-10-30 14:00:00', pd.np.nan, 195.00],
            ['2013-10-30 13:00:00', pd.np.nan, 200.98],
            ['2013-10-30 12:00:00', pd.np.nan, 200.51],
            ['2013-10-30 11:00:00', pd.np.nan, 199.62],
            ['2013-10-30 10:00:00', pd.np.nan, 193.37],
            ['2013-10-30 09:00:00', pd.np.nan, 193.43],
            ['2013-10-30 08:00:00', pd.np.nan, 193.49],
            ['2013-10-30 07:00:00', pd.np.nan, 193.54],
            ['2013-10-30 06:00:00', pd.np.nan, 193.62],
            ['2013-10-30 05:00:00', pd.np.nan, 193.70],
            ['2013-10-30 04:00:00', pd.np.nan, 193.76],
        ],
    },
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '"BV:12.6  Channel:5 Time:28 +304.63 +304.63 +304.63 +304.56 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.63 +304.71 Channel:6 Time:28 +310.51 +310.66 +310.59 +310.51 +310.51 +310.59 +310.59 +310.51 +310.66 +310.51 +310.66 +310.59 ',
        'return_value': [
            ['2013-10-30 15:00:00', '5', '28', 12.6, 304.71],
            ['2013-10-30 14:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 13:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 12:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 11:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 10:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 09:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 08:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 07:00:00', '5', '28', pd.np.nan, 304.56],
            ['2013-10-30 06:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 05:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 04:00:00', '5', '28', pd.np.nan, 304.63],
            ['2013-10-30 15:00:00', '6', '28', 12.6, 310.59],
            ['2013-10-30 14:00:00', '6', '28', pd.np.nan, 310.66],
            ['2013-10-30 13:00:00', '6', '28', pd.np.nan, 310.51],
            ['2013-10-30 12:00:00', '6', '28', pd.np.nan, 310.66],
            ['2013-10-30 11:00:00', '6', '28', pd.np.nan, 310.51],
            ['2013-10-30 10:00:00', '6', '28', pd.np.nan, 310.59],
            ['2013-10-30 09:00:00', '6', '28', pd.np.nan, 310.59],
            ['2013-10-30 08:00:00', '6', '28', pd.np.nan, 310.51],
            ['2013-10-30 07:00:00', '6', '28', pd.np.nan, 310.51],
            ['2013-10-30 06:00:00', '6', '28', pd.np.nan, 310.59],
            ['2013-10-30 05:00:00', '6', '28', pd.np.nan, 310.66],
            ['2013-10-30 04:00:00', '6', '28', pd.np.nan, 310.51],
        ]
    }
]


def test_parser_twdb_stevens():
    for test_set in twdb_stevens_test_sets:
        print 'testing twdb_stevens parser'
        if len(test_set['return_value'][0]) == 3:
            columns = ['timestamp_utc', 'battery_voltage', 'water_level']
        else:
            columns = ['timestamp_utc', 'channel', 'time', 'battery_voltage', 'water_level']

        _assert(test_set, columns, 'twdb_stevens')


twdb_sutron_test_sets = [
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '":Sense01 60 #60 -67.84 -66.15 -67.73 -67.81 -66.42 -68.45 -68.04 -67.87 -71.53 -73.29 -70.55 -72.71 :BL 13.29',
        'return_value': [
            ['2013-10-30 15:00:00', 'sense01', 13.29, 72.71],
            ['2013-10-30 14:00:00', 'sense01', pd.np.nan, 70.55],
            ['2013-10-30 13:00:00', 'sense01', pd.np.nan, 73.29],
            ['2013-10-30 12:00:00', 'sense01', pd.np.nan, 71.53],
            ['2013-10-30 11:00:00', 'sense01', pd.np.nan, 67.87],
            ['2013-10-30 10:00:00', 'sense01', pd.np.nan, 68.04],
            ['2013-10-30 09:00:00', 'sense01', pd.np.nan, 68.45],
            ['2013-10-30 08:00:00', 'sense01', pd.np.nan, 66.42],
            ['2013-10-30 07:00:00', 'sense01', pd.np.nan, 67.81],
            ['2013-10-30 06:00:00', 'sense01', pd.np.nan, 67.73],
            ['2013-10-30 05:00:00', 'sense01', pd.np.nan, 66.15],
            ['2013-10-30 04:00:00', 'sense01', pd.np.nan, 67.84],
        ],
    },
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '":OTT 703 60 #60 -231.47 -231.45 -231.44 -231.45 -231.47 -231.50 -231.51 -231.55 -231.56 -231.57 -231.55 -231.53 :6910704 60 #60 -261.85 -261.83 -261.81 -261.80 -261.81 -261.83 -261.85 -261.87 -261.89 -261.88 -261.86 -261.83 :BL 13.21',
        'return_value': [
            ['2013-10-30 15:00:00', 'ott 703', 13.21, 231.53],
            ['2013-10-30 14:00:00', 'ott 703', pd.np.nan, 231.55],
            ['2013-10-30 13:00:00', 'ott 703', pd.np.nan, 231.57],
            ['2013-10-30 12:00:00', 'ott 703', pd.np.nan, 231.56],
            ['2013-10-30 11:00:00', 'ott 703', pd.np.nan, 231.55],
            ['2013-10-30 10:00:00', 'ott 703', pd.np.nan, 231.51],
            ['2013-10-30 09:00:00', 'ott 703', pd.np.nan, 231.50],
            ['2013-10-30 08:00:00', 'ott 703', pd.np.nan, 231.47],
            ['2013-10-30 07:00:00', 'ott 703', pd.np.nan, 231.45],
            ['2013-10-30 06:00:00', 'ott 703', pd.np.nan, 231.44],
            ['2013-10-30 05:00:00', 'ott 703', pd.np.nan, 231.45],
            ['2013-10-30 04:00:00', 'ott 703', pd.np.nan, 231.47],
            ['2013-10-30 15:00:00', '6910704', 13.21, 261.83],
            ['2013-10-30 14:00:00', '6910704', pd.np.nan, 261.86],
            ['2013-10-30 13:00:00', '6910704', pd.np.nan, 261.88],
            ['2013-10-30 12:00:00', '6910704', pd.np.nan, 261.89],
            ['2013-10-30 11:00:00', '6910704', pd.np.nan, 261.87],
            ['2013-10-30 10:00:00', '6910704', pd.np.nan, 261.85],
            ['2013-10-30 09:00:00', '6910704', pd.np.nan, 261.83],
            ['2013-10-30 08:00:00', '6910704', pd.np.nan, 261.81],
            ['2013-10-30 07:00:00', '6910704', pd.np.nan, 261.80],
            ['2013-10-30 06:00:00', '6910704', pd.np.nan, 261.81],
            ['2013-10-30 05:00:00', '6910704', pd.np.nan, 261.83],
            ['2013-10-30 04:00:00', '6910704', pd.np.nan, 261.85],
        ]
    },
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '"\r\n// \r\n// \r\n// \r\n// \r\n// \r\n-199.88 \r\n-199.92 \r\n-199.96 \r\n-199.98 \r\n-200.05 \r\n-200.09 \r\n-200.15',
        'return_value': [
            ['2013-10-30 15:00:00', pd.np.nan, 200.15],
            ['2013-10-30 14:00:00', pd.np.nan, 200.09],
            ['2013-10-30 13:00:00', pd.np.nan, 200.05],
            ['2013-10-30 12:00:00', pd.np.nan, 199.98],
            ['2013-10-30 11:00:00', pd.np.nan, 199.96],
            ['2013-10-30 10:00:00', pd.np.nan, 199.92],
            ['2013-10-30 09:00:00', pd.np.nan, 199.88],
            ['2013-10-30 08:00:00', pd.np.nan, pd.np.nan],
            ['2013-10-30 07:00:00', pd.np.nan, pd.np.nan],
            ['2013-10-30 06:00:00', pd.np.nan, pd.np.nan],
            ['2013-10-30 05:00:00', pd.np.nan, pd.np.nan],
            ['2013-10-30 04:00:00', pd.np.nan, pd.np.nan],
        ],
    },
]


def test_parser_twdb_sutron():
    for test_set in twdb_sutron_test_sets:
        print 'testing twdb_sutron parser'
        if len(test_set['return_value'][0]) == 3:
            columns = ['timestamp_utc', 'battery_voltage', 'water_level']
        else:
            columns = ['timestamp_utc', 'channel', 'battery_voltage', 'water_level']

        _assert(test_set, columns, 'twdb_sutron')


twdb_texuni_test_sets = [
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': ' \r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.8,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-109.9,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.0,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+0.000,-110.1,\r\n+340.0,+2013.,+307.0,+1400.,+12.07,+0.000,-109.9,-109.8,-110.1,+30.57,',
        'return_value': [
            ['2013-10-30 15:00:00', pd.np.nan, 110.1],
            ['2013-10-30 14:00:00', pd.np.nan, 110.1],
            ['2013-10-30 13:00:00', pd.np.nan, 110.1],
            ['2013-10-30 12:00:00', pd.np.nan, 110.1],
            ['2013-10-30 11:00:00', pd.np.nan, 110.1],
            ['2013-10-30 10:00:00', pd.np.nan, 110.0],
            ['2013-10-30 09:00:00', pd.np.nan, 110.0],
            ['2013-10-30 08:00:00', pd.np.nan, 110.0],
            ['2013-10-30 07:00:00', pd.np.nan, 109.9],
            ['2013-10-30 06:00:00', pd.np.nan, 109.9],
            ['2013-10-30 05:00:00', pd.np.nan, 109.9],
            ['2013-10-30 04:00:00', pd.np.nan, 109.9],
            ['2013-10-30 03:00:00', pd.np.nan, 110.0],
            ['2013-10-30 02:00:00', pd.np.nan, 110.0],
            ['2013-10-30 01:00:00', pd.np.nan, 109.9],
            ['2013-10-30 00:00:00', pd.np.nan, 109.9],
            ['2013-10-29 23:00:00', pd.np.nan, 109.9],
            ['2013-10-29 22:00:00', pd.np.nan, 109.9],
            ['2013-10-29 21:00:00', pd.np.nan, 109.9],
            ['2013-10-29 20:00:00', pd.np.nan, 109.8],
            ['2013-10-29 19:00:00', pd.np.nan, 109.8],
            ['2013-10-29 18:00:00', pd.np.nan, 109.8],
            ['2013-10-29 17:00:00', pd.np.nan, 109.8],
            ['2013-10-29 16:00:00', pd.np.nan, 109.8],
        ]
    },
]


def test_parser_twdb_texuni():
    for test_set in twdb_texuni_test_sets:
        print 'testing twdb_texuni parser'
        columns = ['timestamp_utc', 'battery_voltage', 'water_level']
        _assert(test_set, columns, 'twdb_texuni')


def _assert(test_set, columns, parser):
    expected = pd.DataFrame(test_set['return_value'], columns=columns)
    expected.index = pd.to_datetime(expected['timestamp_utc'])
    del expected['timestamp_utc']
    parser = getattr(parsers, parser)
    df = parser(test_set)
    # to compare pandas dataframes, columns must be in same order
    assert_frame_equal(df.sort(axis=1).sort(axis=0), expected.sort(axis=1).sort(axis=0))
