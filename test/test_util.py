import contextlib
import os
import os.path

import mock
import requests


@contextlib.contextmanager
def mocked_requests(path):
    """mocks the requests library to return a given file's content"""
    # if environment variable is set, then don't mock the tests just grab files
    # over the network. Example:
    #    env ULMO_DONT_MOCK_TESTS=1 py.test
    if os.environ.get('ULMO_DONT_MOCK_TESTS', False):
        yield

    else:
        test_path = get_test_file_path(path)

        with open(test_path, 'rb') as f:
            mock_response = requests.Response()
            mock_response.status_code = 200
            mock_response.raw = f

            with mock.patch('requests.get', return_value=mock_response):
                yield


def get_test_file_path(file_path):
    """translates a file path to be relative to the test files directory"""
    return os.path.join(os.path.dirname(__file__), 'files', file_path)
