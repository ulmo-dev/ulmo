from contextlib import contextmanager
import datetime
import email.utils
import os
import re
import warnings

import appdirs
from lxml import etree
import pandas
import requests


# pre-compiled regexes for underscore conversion
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


class DependencyError(Exception):
    pass


def camel_to_underscore(s):
    """converts camelCase to underscore, originally from
    http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    first_sub = first_cap_re.sub(r'\1_\2', s)
    return all_cap_re.sub(r'\1_\2', first_sub).lower()


def dict_from_dataframe(dataframe):
    for column_name in dataframe.columns:
        dataframe[column_name][pandas.isnull(dataframe[column_name])] = None
    if isinstance(dataframe.index, pandas.PeriodIndex):
        dataframe.index = [str(i) for i in dataframe.index]

    return dataframe.T.to_dict()


def download_if_new(url, path, check_modified=True):
    """downloads the file located at `url` to `path`, if check_modified is True
    it will only download if the url's last-modified header has a more recent
    date than the filesystem's last modified date for the file
    """
    head = requests.head(url)
    if not os.path.exists(path) or not _file_size_matches(head, path):
        _download_file(url, path)
    elif check_modified and _request_is_newer_than_file(head, path):
        _download_file(url, path)


def get_ulmo_dir():
    return_dir = appdirs.user_data_dir('ulmo', 'ulmo')
    mkdir_if_doesnt_exist(return_dir)
    return return_dir


def mkdir_if_doesnt_exist(dir_path):
    """makes a directory if it doesn't exist"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def module_with_dependency_errors(method_names):
    class FakeModule(object):
        pass
    fake_module = FakeModule()
    for method_name in method_names:
        setattr(fake_module, method_name, raise_dependency_error)
    return fake_module


@contextmanager
def open_file_for_url(url, path, check_modified=True):
    """returns an open file handle for a data file; downloading if necessary or
    otherwise using a previously downloaded file
    """
    download_if_new(url, path, check_modified)
    open_file = open(path, 'rb')
    yield open_file
    open_file.close()


def parse_datestr(date_string):
    """returns a datetime.date given a string of the format `YYYY-MM-DD`"""
    if date_string:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()


def raise_dependency_error(*args, **kwargs):
    raise DependencyError("Trying to do something that depends on pytables, "
            "but pytables has not been installed.")


def save_pretty_printed_xml(filename, response_buffer):
    """saves a nicely indented version of the xml contained in response_buffer
    to filename; handy for debugging or saving responses for to include in tests"""
    with open(filename, 'w') as f:
        response_buffer.seek(0)
        parsed = etree.parse(response_buffer)
        f.write(etree.tostring(parsed, pretty_print=True))
        response_buffer.seek(0)


def _download_file(url, path):
    request = requests.get(url)
    mkdir_if_doesnt_exist(os.path.dirname(path))
    chunk_size = 64 * 1024
    with open(path, 'wb') as f:
        for content in request.iter_content(chunk_size):
            f.write(content)


def _file_size_matches(request, path):
    """returns True if request content-length header matches file size"""
    content_length = request.headers.get('content-length')
    if content_length and int(content_length) == os.path.getsize(path):
        return True
    else:
        return False


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
