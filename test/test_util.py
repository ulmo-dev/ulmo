import contextlib
import os
import os.path

import mock
import requests


@contextlib.contextmanager
def mocked_requests(mocked_urls):
    """mocks the requests library to return a given file's content"""
    # if environment variable is set, then don't mock the tests just grab files
    # over the network. Example:
    #    env ULMO_DONT_MOCK_TESTS=1 py.test
    if os.environ.get('ULMO_DONT_MOCK_TESTS', False):
        yield

    else:
        if isinstance(mocked_urls, basestring):
            file_paths = [mocked_urls]
        else:
            file_paths = mocked_urls.values()

        with _open_multiple(file_paths) as open_files:
            if isinstance(mocked_urls, basestring):
                url_files = open_files.values()[0]
            else:
                url_files = {
                    url: open_files.get(file_path)
                    for url, file_path in mocked_urls.iteritems()
                }
            side_effect = _mock_side_effect(url_files)

            with mock.patch('requests.get', side_effect=side_effect):
                yield


def get_test_file_path(file_path):
    """translates a file path to be relative to the test files directory"""
    return os.path.join(os.path.dirname(__file__), 'files', file_path)


def _mock_side_effect(url_files):
    def _side_effect(url, *args, **kwargs):
        mock_response = requests.Response()
        mock_response.request = requests.Request(url, *args, **kwargs)
        mock_response.status_code = 200
        mock_response.url = url
        mock_response.mocked = True
        if isinstance(url_files, dict):
            mock_response.raw = url_files.get(mock_response.request.full_url)
        elif hasattr(url_files, 'read'):
            mock_response.raw = url_files

        # seek to beginning in case this handle has been used before
        mock_response.raw.seek(0)

        return mock_response
    return _side_effect


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
