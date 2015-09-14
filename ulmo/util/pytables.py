"""
   ulmo.util
   ~~~~~~~~~~

   Collection of useful functions for common use cases
"""
from contextlib import contextmanager
import os
import warnings

import tables

from . import misc as util_misc


def get_default_h5file_path(dataset):
    default_dir = util_misc.get_ulmo_dir()
    return os.path.join(default_dir, 'ulmo_%s.h5' % dataset)


def get_or_create_group(h5file, path, title, *args, **kwargs):
    return _get_or_create_node('createGroup', h5file, path, title, *args,
            **kwargs)


def get_or_create_table(h5file, path, table_definition, title):
    return _get_or_create_node('createTable', h5file, path, table_definition,
            title)


@contextmanager
def open_h5file(path, mode, filters=None):
    """returns an open h5file, creating a new one if it doesn't
    already exist
    """
    if filters is None:
        filters = _best_available_filters(['blosc', 'zlib'])

    # create file if it doesn't exist
    util_misc.mkdir_if_doesnt_exist(os.path.dirname(path))
    if not os.path.exists(path):
        new_file = tables.openFile(path, mode='w', title='ulmo data', filters=filters)
        new_file.close()

    open_file = tables.openFile(path, mode=mode)
    yield open_file
    open_file.close()


def update_or_append_sortable(table, update_values, sortby):
    """updates table with dict representations of rows, appending new rows if
    need be; sortby should be a completly sortable column (with a CSIndex)
    """
    value_row = table.row
    update_values.sort(key=lambda v: v[sortby])
    table_iterator = table.itersorted(sortby)
    try:
        current_row = next(table_iterator)
    except StopIteration:
        current_row = None

    for i, update_value in enumerate(update_values):
        if not current_row or update_value[sortby] < current_row[sortby]:
            update_value['__flag_for_append'] = True

        elif current_row:
            # advance the table iterator until you are >= update_value
            while current_row and current_row[sortby] < update_value[sortby]:
                try:
                    current_row = next(table_iterator)
                except StopIteration:
                    current_row = None

            # if we match, then update
            if current_row and current_row[sortby] == update_value[sortby]:
                _update_row_with_dict(current_row, update_value)
                current_row.update()

            # else flag for append
            else:
                update_value['__flag_for_append'] = True

    for update_value in update_values:
        if '__flag_for_append' in update_value:
            del update_value['__flag_for_append']
            _update_row_with_dict(value_row, update_value)
            value_row.append()
    table.flush()


def _best_available_filters(possible_compressions):
    """returns the best available filters to use"""
    for possible_compression in possible_compressions:
        try:
            return tables.Filters(complevel=1, complib=possible_compression)
        except tables.FiltersWarning:
            pass

    return tables.Filters()


def _update_row_with_dict(row, dict):
    """sets the values of row to be the values found in dict"""
    for k, v in dict.items():
        row.__setitem__(k, v)


def _get_or_create_node(method_name, h5file, path, *args, **kwargs):
    try:
        node = h5file.getNode(path)
    except tables.exceptions.NoSuchNodeError:
        where, name = path.rsplit('/', 1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            create_method = getattr(h5file, method_name)
            node = create_method(where, name, *args, **kwargs)
    return node
