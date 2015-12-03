import datetime
import pandas

import ulmo

import test_util


def test_get_sites():
    sites_file = 'lcra/hydromet/stream_stage_and_flow_sites_list.html'
    with test_util.mocked_urls(sites_file):
        sites = ulmo.lcra.hydromet.get_sites('stage')
        assert 60 <= len(sites) <= 70
        assert '5499' in sites


def test_get_site_data():
    test_values = pandas.DataFrame(
        [{'Stage(feet)': 6.20, 'Flow(cfs)': 74},
         {'Stage(feet)': 6.01, 'Flow(cfs)': 58}],
        index=[datetime.datetime(2015, 11, 28, 2, 55, 0),
               datetime.datetime(2015, 12, 3, 10, 10, 0)])
    data_file = 'lcra/hydromet/4598_stage_flow_data.html'
    with test_util.mocked_urls(data_file):
        site_data = ulmo.lcra.hydromet.get_site_data(
            '4598', 'stage', start_date=datetime.date(2015, 11, 3),
            end_date=datetime.date(2015, 12, 4))

    assert site_data.shape[0] == 2932
    are_equal = test_values == site_data.ix[test_values.index]
    assert are_equal.sum().sum() == 4
