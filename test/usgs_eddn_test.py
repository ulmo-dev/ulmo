import pandas as pd
import ulmo
import test_util


test_sets = [
    {
        'dcp_address': 'C5149430',
        'number_of_lines': 4,
        'parser': 'twdb_stevens',
    },
    {
        'dcp_address': 'C514D73A',
        'number_of_lines': 4,
        'parser': 'twdb_sutron',
    },
#    {
#    'dcp_address': 'C5149430',
#    'number_of_lines': 4,
#    }
]


def test_parse_dcp_message_header():
    assert 1==1


def test_parse_dcp_message():
    for test_set in test_sets:
        dcp_data_file = 'usgs/eddn/' + test_set['dcp_address'] + '.txt'
        with test_util.mocked_urls(dcp_data_file):
            data = ulmo.usgs.eddn.get_data(test_set['dcp_address'], path='/tmp')
            assert len(data) == test_set['number_of_lines']


def test_parser_twdb_stevens():
    assert 1==1


def test_parser_twdb_sutron_linear():
    assert 1==1

