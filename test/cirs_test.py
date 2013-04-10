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
            },
        ]
    },
]


def test_get_data_by_climate_division():
    for test_set in test_sets:
        index = test_set['index']
        by_state = test_set['by_state']

        use_file = _test_use_file(index)
        data = ulmo.ncdc.cirs.get_data(index, by_state=by_state,
                use_file=use_file, as_dataframe=False)
        for test_value in test_set['values']:
            assert test_value in data


def _test_use_file(index):
    if test_util.use_test_files():
        path = 'ncdc/cirs/drd964x.%s.txt' % index
        return test_util.get_test_file_path(path)
    else:
        return None

