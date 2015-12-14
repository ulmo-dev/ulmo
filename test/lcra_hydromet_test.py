import datetime
import pandas

import ulmo

import test_util


def test_get_sites_by_type():
    sites_file = 'lcra/hydromet/stream_stage_and_flow_sites_list.html'
    with test_util.mocked_urls(sites_file):
        sites = ulmo.lcra.hydromet.get_sites_by_type('stage')
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


def test_get_current_data():
    test_values = pandas.DataFrame(
        [{'datetime': datetime.datetime(2015, 12, 10, 14, 10),
          'location': 'Barton Creek at Loop 360, Austin',
          'stageft': 3.33,
          'flowcfs': 60.00,
          'floodstageft': 8.00,
          'bankfullstageft': 8.00
          },
          {'datetime': datetime.datetime(2015, 12, 10, 14, 10),
           'location': 'Colorado River at Columbus',
           'stageft': 10.32,
           'flowcfs': 975.00,
           'bankfullstageft': 30.00,
           'floodstageft': 34.00}])
    test_values.set_index('location', inplace=True)
    data_file = 'lcra/hydromet/current_data_2015-12-10-14-10.xml'
    with test_util.mocked_urls(data_file):
        current_data = ulmo.lcra.hydromet.get_current_data('getlowerbasin')
        current_data_df = pandas.DataFrame(current_data)
        current_data_df.set_index('location', inplace=True)
    are_equal = test_values == current_data_df.ix[test_values.index][test_values.columns]
    assert pandas.np.all(are_equal)
    assert len(current_data) == 33
