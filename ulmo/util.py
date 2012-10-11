"""
   ulmo.util
   ~~~~~~~~~~

   Collection of useful functions for common use cases
"""
from contextlib import contextmanager
import datetime
import email.utils
import os
import warnings

import appdirs
import requests
import tables


def get_default_h5file_path():
    default_dir = get_ulmo_dir()
    return os.path.join(default_dir, 'ulmo.h5')


def get_ulmo_dir():
    return_dir = appdirs.user_data_dir('ulmo', 'ulmo')
    mkdir_if_doesnt_exist(return_dir)
    return return_dir


def get_or_create_group(h5file, path, title):
    return _get_or_create_node('createGroup', h5file, path, title)


def get_or_create_table(h5file, path, table_definition, title):
    return _get_or_create_node('createTable', h5file, path, table_definition,
            title)


def mkdir_if_doesnt_exist(dir_path):
    """makes a directory if it doesn't exist"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


@contextmanager
def open_file_for_url(url, path, check_modified=True):
    """returns an open file handle for a data file; downloading if necessary or
    otherwise using a previously downloaded file
    """
    request = requests.get(url)
    if not os.path.exists(path):
        _save_request_to_file(request, path)
    elif check_modified and _request_is_newer_than_file(request, path):
        _save_request_to_file(request, path)
    open_file = open(path, 'rb')
    yield open_file
    open_file.close()


def parse_datestr(date_string):
    """returns a datetime.date given a string of the format `YYYY-MM-DD`"""
    if date_string:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()


def update_or_append_sortable(table, update_values, sortby):
    """updates table with dict representations of rows, appending new rows if
    need be; sortby should be a completly sortable column (with a CSIndex)
    """
    value_row = table.row
    update_values.sort(key=lambda v: v[sortby])
    table_iterator = table.itersorted(sortby)
    try:
        current_row = table_iterator.next()
    except StopIteration:
        current_row = None

    for i, update_value in enumerate(update_values):
        if not current_row or update_value[sortby] < current_row[sortby]:
            update_value['__flag_for_append'] = True

        elif current_row:
            # advance the table iterator until you are >= update_value
            while current_row and current_row[sortby] < update_value[sortby]:
                try:
                    current_row = table_iterator.next()
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


@contextmanager
def open_h5file(path, mode):
    """returns an open h5file, creating a new one if it doesn't
    already exist
    """
    # create file if it doesn't exist
    mkdir_if_doesnt_exist(os.path.dirname(path))
    if not os.path.exists(path):
        new_file = tables.openFile(path, mode='w', title='ulmo data')
        new_file.close()

    open_file = tables.openFile(path, mode=mode)
    yield open_file
    open_file.close()


def _parse_rfc_1123_timestamp(timestamp_str):
    return datetime.datetime(*email.utils.parsedate(timestamp_str)[:6])


def _request_is_newer_than_file(request, path):
    """returns true if a request's last-modified header is more recent than a
    file's last modified timestamp
    """
    if not os.path.exists(path):
        return True

    if not request.headers.get('last-modified'):
        warnings.warn('no last-modified date for request: %s, downloading file again' % request.url)
        return True

    request_last_modified = _parse_rfc_1123_timestamp(request.headers.get('last-modified'))
    path_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if request_last_modified > path_last_modified:
        return True
    else:
        return False


def _save_request_to_file(request, path):
    mkdir_if_doesnt_exist(os.path.dirname(path))
    with open(path, 'wb') as f:
        f.write(request.content)


def _update_row_with_dict(row, dict):
    """sets the values of row to be the values found in dict"""
    for k, v in dict.iteritems():
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

