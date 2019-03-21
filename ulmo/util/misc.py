from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import str
from past.builtins import basestring
from builtins import object
from contextlib import contextmanager
import datetime
import email.utils
import ftplib
import functools
import os
import re
import urllib.parse
import warnings

import appdirs
from lxml import etree
import numpy as np
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


def convert_date(date):
    """returns a datetime.date object from either a string representation or
    date-like object (datetime.date, datetime.datetime, or pandas.Timestamp)
    """
    return pandas.Timestamp(date).date()


def convert_datetime(datetime):
    """returns a datetime.date object from either a string representation or
    datetime-like object (datetime.date, datetime.datetime, or pandas.Timestamp)
    """
    return pandas.Timestamp(datetime).to_pydatetime()


def dir_list(url):
    """given a path to a ftp directory, returns a list of files in that
    directory
    """
    parsed = urllib.parse.urlparse(url)
    ftp = ftplib.FTP(parsed.netloc, "anonymous")
    ftp.cwd(parsed.path)
    return ftp.nlst()


def dict_from_dataframe(dataframe):
    if isinstance(dataframe.index, pandas.PeriodIndex):
        dataframe.index = dataframe.index.to_timestamp().astype('str')
    if isinstance(dataframe.index, pandas.DatetimeIndex):
        dataframe.index = [str(i) for i in dataframe.index]

    # convert np.nan objects to None objects; prior to pandas 0.13.0 this could
    # be done in a vectorized way, but as of 0.13, assigning None into a
    # dataframe, it gets converted to a nan object so this has to be done
    # rather inefficiently in a post-processing step
    if pandas.__version__ < '0.13.0':
        for column_name in dataframe.columns:
            dataframe[column_name][pandas.isnull(dataframe[column_name])] = None
        df_dict = dataframe.T.to_dict()
    else:
        df_dict = dataframe.where((pandas.notnull(dataframe)), None).to_dict(orient='index')

    return df_dict


def download_if_new(url, path, check_modified=True):
    """downloads the file located at `url` to `path`, if check_modified is True
    it will only download if the url's last-modified header has a more recent
    date than the filesystem's last modified date for the file
    """
    parsed = urllib.parse.urlparse(url)

    if os.path.exists(path) and not check_modified:
        return

    if parsed.scheme.startswith('ftp'):
        _ftp_download_if_new(url, path, check_modified)
    elif parsed.scheme.startswith('http'):
        _http_download_if_new(url, path, check_modified)
    else:
        raise NotImplementedError("only ftp and http urls are currently implemented")


def get_ulmo_dir(sub_dir=None):
    return_dir = appdirs.user_data_dir('ulmo', 'ulmo')
    if sub_dir:
        return_dir = os.path.join(return_dir, sub_dir)
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
        def f(*args, **kwargs):
            raise_dependency_error()
        f.__name__ = method_name
        setattr(fake_module, method_name, f)
    return fake_module


def module_with_deprecation_warnings(functions, warning_message):
    warnings.filterwarnings("always", warning_message, DeprecationWarning)

    class DeprecatedModule(object):
        pass
    deprecated_module = DeprecatedModule()

    def warning_decorator(f):
        @functools.wraps(f)
        def warning_wrapper(*args, **kwargs):
            warnings.warn(warning_message, DeprecationWarning)
            return f(*args, **kwargs)
        return warning_wrapper

    for function in functions:
        wrapped_function = warning_decorator(function)
        setattr(deprecated_module, function.__name__, wrapped_function)
    return deprecated_module


@contextmanager
def open_file_for_url(url, path, check_modified=True, use_file=None, use_bytes=None):
    """Context manager that returns an open file handle for a data file;
    downloading if necessary or otherwise using a previously downloaded file.
    File downloading will be short-circuited if use_file is either a file path
    or an open file-like object (i.e. file handler or StringIO obj), in which
    case the file handler pointing to use_file is returned - if use_file is a
    file handler then the handler won't be closed upon exit.
    """
    leave_open = False

    if use_file is not None:
        if hasattr(use_file, 'read'):
            leave_open = True
            yield use_file
        else:
            open_path = use_file
    else:
        download_if_new(url, path, check_modified)
        open_path = path

    if use_bytes is None:
        open_file = open(open_path, 'r')
    else:
        open_file = open(open_path, 'rb')

    yield open_file

    if not leave_open:
        open_file.close()


def parse_fwf(file_path, columns, na_values=None):
    """Convenience function for parsing fixed width formats. Wraps the pandas
    read_fwf parser but allows all column information to be kept together.
    Columns should be an iterable of lists/tuples with the format (column_name,
    start_value, end_value, converter). Returns a pandas dataframe.
    """
    names, colspecs = list(zip(*[(name, (start, end))
        for name, start, end, converter in columns]))

    converters = dict([
        (name, converter)
        for name, start, end, converter in columns
        if not converter is None
    ])

    return pandas.io.parsers.read_fwf(file_path,
        colspecs=colspecs, header=None, na_values=na_values, names=names,
        converters=converters)


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


def to_bytes(s):
    """convert str to bytes for py 2/3 compat
    """

    if isinstance(s, bytes):
        return s

    return s.encode('utf-8', 'ignore')


def _ftp_download_if_new(url, path, check_modified=True):
    parsed = urllib.parse.urlparse(url)
    ftp = ftplib.FTP(parsed.netloc, "anonymous")
    directory, filename = parsed.path.rsplit('/', 1)
    ftp_last_modified = _ftp_last_modified(ftp, parsed.path)
    ftp_file_size = _ftp_file_size(ftp, parsed.path)

    if not os.path.exists(path) or os.path.getsize(path) != ftp_file_size:
        _ftp_download_file(ftp, parsed.path, path)
    elif check_modified and _path_last_modified(path) < ftp_last_modified:
        _ftp_download_file(ftp, parsed.path, path)


def _ftp_download_file(ftp, ftp_path, local_path):
    with open(local_path, 'wb') as f:
        ftp.retrbinary("RETR " + ftp_path, f.write)


def _ftp_file_size(ftp, file_path):
    ftp.sendcmd('TYPE I')
    return ftp.size(file_path)


def _ftp_last_modified(ftp, file_path):
    timestamp = ftp.sendcmd("MDTM " + file_path).split()[-1]
    return datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S')


def _http_download_file(url, path):
    request = requests.get(url)
    mkdir_if_doesnt_exist(os.path.dirname(path))
    chunk_size = 64 * 1024
    with open(path, 'wb') as f:
        for content in request.iter_content(chunk_size):
            f.write(content)


def _http_download_if_new(url, path, check_modified):
    head = requests.head(url)
    if not os.path.exists(path) or not _request_file_size_matches(head, path):
        _http_download_file(url, path)
    elif check_modified and _request_is_newer_than_file(head, path):
        _http_download_file(url, path)


def _nans_to_nones(nan_dict):
    """takes a dict and if any values are np.nan then it will replace them with
    None"""
    return dict([
        (k, v) if v is not np.nan else (k, None)
        for k, v in nan_dict.items()
    ])


def _parse_rfc_1123_timestamp(timestamp_str):
    return datetime.datetime(*email.utils.parsedate(timestamp_str)[:6])


def _path_last_modified(path):
    """returns a datetime.datetime object representing the last time the file at
    a given path was last modified
    """
    if not os.path.exists(path):
        return None

    return datetime.datetime.utcfromtimestamp(os.path.getmtime(path))


def _request_file_size_matches(request, path):
    """returns True if request content-length header matches file size"""
    content_length = request.headers.get('content-length')
    if content_length and int(content_length) == os.path.getsize(path):
        return True
    else:
        return False


def _request_is_newer_than_file(request, path):
    """returns true if a request's last-modified header is more recent than a
    file's last modified timestamp
    """
    path_last_modified = _path_last_modified(path)

    if path_last_modified is None:
        return True

    if not request.headers.get('last-modified'):
        warnings.warn('no last-modified date for request: %s, downloading file again' % request.url)
        return True

    request_last_modified = _parse_rfc_1123_timestamp(request.headers.get('last-modified'))
    if request_last_modified > path_last_modified:
        return True
    else:
        return False
