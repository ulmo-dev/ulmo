import contextlib
import os
import os.path
import re
import shutil
import tempfile

from httpretty import HTTPretty
import mock


def get_test_file_path(file_path):
    """translates a file path to be relative to the test files directory"""
    return os.path.join(os.path.dirname(__file__), 'files', file_path)


@contextlib.contextmanager
def mocked_suds_client(waterml_version, mocked_service_calls):
    """mocks the suds library to return a given file's content"""
    # if environment variable is set, then don't mock the tests just grab files
    # over the network. Example:
    #    env ULMO_DONT_MOCK_TESTS=1 py.test
    if os.environ.get('ULMO_DONT_MOCK_TESTS', False):
        yield

    else:
        tns_str = 'http://www.cuahsi.org/his/%s/ws/' % waterml_version
        with _open_multiple(mocked_service_calls.values()) as open_files:
            client = mock.MagicMock()
            client.wsdl.tns = ('tns', tns_str)

            for service_call, filename in mocked_service_calls.iteritems():
                open_file = open_files[filename]

                def _func(*args, **kwargs):
                    return open_file.read()
                setattr(client.service, service_call, _func)

            with mock.patch('suds.client.Client', return_value=client):
                yield


@contextlib.contextmanager
def mocked_urls(url_files, methods=None):
    """mocks the underlying python sockets library to return a given file's
    content
    """
    # if environment variable is set, then don't mock the tests just grab files
    # over the network. Example:
    #    env ULMO_DONT_MOCK_TESTS=1 py.test
    if os.environ.get('ULMO_DONT_MOCK_TESTS', False):
        yield

    else:
        if isinstance(url_files, basestring):
            url_files = {'.*': url_files}

        HTTPretty.enable()
        for url_match, url_file in url_files.iteritems():
            if not isinstance(url_match, basestring) and len(url_match) == 2:
                url_match, methods = url_match

            if not os.path.isabs(url_file):
                url_file = get_test_file_path(url_file)

            callback = _build_request_callback(url_file)
            url_re = re.compile(url_match)

            if methods is None:
                methods = ['GET', 'POST', 'HEAD']

            for method in methods:
                request_class = getattr(HTTPretty, method)
                HTTPretty.register_uri(request_class, url_re, body=callback)
        yield
        HTTPretty.disable()
        HTTPretty.reset()


@contextlib.contextmanager
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def use_test_files():
    """Returns true if tests should be run using test files, false otherwise."""
    return os.environ.get('ULMO_DONT_MOCK_TESTS', True)


def _build_request_callback(response_file):
    def request_callback(method, uri, headers):
        if method == 'HEAD':
            response_text = ''
        else:
            with open(response_file, 'rb') as f:
                response_text = f.read()
        return [200, headers, response_text]
    return request_callback


@contextlib.contextmanager
def _open_multiple(paths, handlers=None, new_paths=None):
    """context manager that yields a dict containing file paths as keys mapped
    to their corresponding open file handles
    """
    # note: recursion is the pattern here
    if not handlers and not new_paths:
        with _open_multiple([], [], paths) as return_dict:
            yield return_dict
    elif len(new_paths) == 0:
        yield dict(zip(paths, handlers))
    else:
        next_path = new_paths.pop(0)
        test_path = get_test_file_path(next_path)
        with open(test_path, 'rb') as f:
            paths.append(next_path)
            handlers.append(f)
            with _open_multiple(paths, handlers, new_paths) as return_dict:
                yield return_dict
