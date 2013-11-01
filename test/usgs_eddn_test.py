from datetime import datetime
import pandas as pd
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
            data = ulmo.usgs.eddn.get_data(test_set['dcp_address'], path='/tmp', clear_cache=True)
            assert len(data) == test_set['number_of_lines']


def test_parse_dcp_message_timestamp():
    for test_set in message_test_sets:
        dcp_data_file = 'usgs/eddn/' + test_set['dcp_address'] + '.txt'
        with test_util.mocked_urls(dcp_data_file):
            data = ulmo.usgs.eddn.get_data(test_set['dcp_address'], path='/tmp', clear_cache=True)
            assert data['message_timestamp_utc'][-1] == test_set['first_row_message_timestamp_utc']


stevens_test_sets = [
    {
        'message_timestamp_utc': datetime(2013,10,30,15,28,18),
        'dcp_message': '"BV:11.9  193.76$ 193.70$ 193.62$ 193.54$ 193.49$ 193.43$ 193.37$ 199.62$ 200.51$ 200.98$ 195.00$ 194.33$ ',
        'return_value': [
                            ['2013-10-30 15:00:00', '11.9', '194.33'],
                            ['2013-10-30 14:00:00', '', '195.00'],
                            ['2013-10-30 13:00:00', '', '200.98'],
                            ['2013-10-30 12:00:00', '', '200.51'],
                            ['2013-10-30 11:00:00', '', '199.63'],
                            ['2013-10-30 10:00:00', '', '193.37'],
                            ['2013-10-30 09:00:00', '', '193.43'],
                            ['2013-10-30 08:00:00', '', '193.49'],
                            ['2013-10-30 07:00:00', '', '193.54'],
                            ['2013-10-30 06:00:00', '', '193.62'],
                            ['2013-10-30 05:00:00', '', '193.70'],
                            ['2013-10-30 04:00:00', '', '193.76'],
                        ], 
    }
]


def test_parser_twdb_stevens():
    for test_set in stevens_test_sets:
        df = pd.DataFrame(test_set['return_value'], columns=['timestamp_utc', 'battery_voltage', 'water_level'])
        df.index = pd.to_datetime(df['timestamp_utc'])
        del df['timestamp_utc']
        parser = getattr(parsers, 'twdb_stevens')
        assert df == parser(pd.Series(test_set))


def test_parser_twdb_sutron_linear():
    assert 1==1

