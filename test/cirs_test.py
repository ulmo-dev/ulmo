import copy

import numpy as np
import pandas

import ulmo
import test_util


test_sets = [
    {
        'element': 'pdsi',
        'by_state': False,
        'values': [
            {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 1,
                'pdsi': 2.35,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 2,
                'pdsi': 2.31,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 3,
                'pdsi': 2.33,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 11,
                'pdsi': 3.11,
            }, {
                'state': 'WY',
                'state_code': 48,
                'division': 8,
                'year': 1998,
                'month': 12,
                'pdsi': 2.96,
            }, {
                'state': 'TX',
                'state_code': 41,
                'division': 10,
                'year': 1895,
                'month': 1,
                'pdsi': -0.1,
            }, {
                'state': 'TX',
                'state_code': 41,
                'division': 10,
                'year': 1895,
                'month': 12,
                'pdsi': 1.94,
            },
        ]
    }, {
        'element': 'tmp',
        'by_state': True,
        'values': [
            {
                'location': 'ME',
                'location_code': 17,
                'year': 1895,
                'month': 1,
                'tmp': 14.00,
            }, {
                'location': 'ME',
                'location_code': 17,
                'year': 1895,
                'month': 12,
                'tmp': 22.70,
            }, {
                'location': 'national',
                'location_code': 110,
                'year': 2013,
                'month': 1,
                'tmp': 31.91,
            }, {
                'location': 'national',
                'location_code': 110,
                'year': 2013,
                'month': 2,
                'tmp': 34.77,
            },
        ]
    }, {
        'element': 'tmp',
        'by_state': True,
        'location_names': 'full',
        'values': [
            {
                'location': 'Maine',
                'location_code': 17,
                'year': 1895,
                'month': 1,
                'tmp': 14.00,
            },
        ]
    }, {
        'element': 'sp01',
        'by_state': True,
        'values': [
            {
                'location': 'AL',
                'location_code': 1,
                'year': 1895,
                'month': 1,
                'sp01': 0.84,
            },
        ]
    }, {
        'element': ['sp01', 'tmp', 'pdsi'],
        'by_state': True,
        'values': [
            {
                'location': 'AL',
                'location_code': 1,
                'year': 1895,
                'month': 1,
                'sp01': 0.84,
                'tmp': 43.70,
                'pdsi': 0.44,
            },
            {
                'location': None,
                'location_code': 113,
                'year': 1895,
                'month': 1,
                'sp01': None,
                'tmp': 17.20,
                'pdsi': None,
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


def test_doesnt_have_locations_if_location_names_is_none():
    element = 'pdsi'
    use_file = _test_use_file(element, False)
    data = ulmo.ncdc.cirs.get_data(
        element, location_names=None, use_file=use_file, as_dataframe=True)
    assert 'location' not in data.columns


def _run_test_sets(test_sets):
    for test_set in test_sets:
        test_args = copy.copy(test_set)
        element = test_args.pop('element')
        test_values = test_args.pop('values')
        by_state = test_args['by_state']

        use_file = _test_use_file(element, by_state)
        data = ulmo.ncdc.cirs.get_data(
            element, use_file=use_file, as_dataframe=True, **test_args)
        if isinstance(element, basestring) or len(element) == 1:
            not_nulls = data[element].notnull()
        else:
            not_nulls = pandas.notnull(data[element]).any(axis=1)
        assert np.all(not_nulls)
        for test_value in test_values:
            _assert_inclusion(test_value, data)


def _assert_inclusion(value_dict, dataframe):
    "tests that a value_dict is in a dataframe"
    sub_df = dataframe.copy()
    for k, v in value_dict.iteritems():
        if pandas.isnull(v):
            sub_df = sub_df[pandas.isnull(sub_df[k])]
        else:
            sub_df = sub_df[sub_df[k] == v]

    assert len(sub_df) == 1


def _test_use_file(elements, by_state):
    if test_util.use_test_files():
        if isinstance(elements, basestring):
            if by_state:
                path = 'ncdc/cirs/drd964x.%sst.txt' % elements
            else:
                path = 'ncdc/cirs/drd964x.%s.txt' % elements
        else:
            path = 'ncdc/cirs/'
        return test_util.get_test_file_path(path)
    else:
        return None
