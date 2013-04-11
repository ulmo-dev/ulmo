import ulmo
import test_util


test_sets = [
    {
        'index': 'pdsi',
        'by_state': False,
        'values': [
            {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 1,
                'value': 2.35,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 2,
                'value': 2.31,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 3,
                'value': 2.33,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 11,
                'value': 3.11,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 12,
                'value': 2.96,
            }, {
                'state': 'TX',
                'state_code': 41,
                'division': 10,
                'year': 1895,
                'month': 1,
                'value': -0.1,
            }, {
                'state': 'TX',
                'state_code': 41,
                'division': 10,
                'year': 1895,
                'month': 12,
                'value': 1.94,
            },
        ]
    }, {
        'index': 'tmp',
        'by_state': True,
        'values': [
            {
                'location': 'ME',
                'location_code': 17,
                'year': 1895,
                'month': 1,
                'value': 14.00,
            }, {
                'location': 'ME',
                'location_code': 17,
                'year': 1895,
                'month': 12,
                'value': 22.70,
            }, {
                'location': 'national',
                'location_code': 110,
                'year': 2013,
                'month': 1,
                'value': 31.90,
            }, {
                'location': 'national',
                'location_code': 110,
                'year': 2013,
                'month': 2,
                'value': 34.78,
            },
        ]
    },
]


def test_get_data_by_state():
    state_tests = [s for s in test_sets if s['by_state']]
    _run_test_sets(state_tests)


def test_get_data_by_climate_division():
    division_tests = [s for s in test_sets if not s['by_state']]
    _run_test_sets(division_tests)


def _run_test_sets(test_sets):
    for test_set in test_sets:
        index = test_set['index']
        by_state = test_set['by_state']

        use_file = _test_use_file(index)
        data = ulmo.ncdc.cirs.get_data(index, by_state=by_state,
                use_file=use_file, as_dataframe=True)
        for test_value in test_set['values']:
            _assert_inclusion(test_value, data)


def _assert_inclusion(value_dict, dataframe):
    "tests that a value_dict is in a dataframe"
    sub_df = dataframe.copy()
    for k, v in value_dict.iteritems():
        sub_df = sub_df[sub_df[k] == v]

    assert len(sub_df) == 1


def _test_use_file(index):
    if test_util.use_test_files():
        path = 'ncdc/cirs/drd964x.%s.txt' % index
        return test_util.get_test_file_path(path)
    else:
        return None
