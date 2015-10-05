import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand



class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


rootpath = os.path.abspath(os.path.dirname(__file__))
with open('README.rst') as f:
    # use README for long description but don't include the link to travis-ci;
    # it seems a bit out of place on pypi since it applies to the development
    # version
    long_description = ''.join([
        line for line in f.readlines()
        if 'travis-ci' not in line])


# this sets __version__
def version():
    """Get the version number."""
    with open(os.path.join(rootpath, "VERSION.txt")) as v:
        _version = v.read()
    return _version.strip()


__version__ = version()


setup(
    name='ulmo',
    version=__version__,
    license='BSD',
    author='Dharhas Pothina',
    author_email='dharhas@gmail.com',
    description='clean, simple and fast access to public hydrology and climatology data',
    long_description=long_description,
    url='https://github.com/ulmo-dev/ulmo/',
    keywords='his pyhis ulmo water waterml cuahsi wateroneflow usgs ned',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'appdirs>=1.2.0',
        'beautifulsoup4>=4.1.3',
        'geojson',
        'isodate>=0.4.6',
        'lxml>=2.3',
        # mock is required for mocking pytables-related functionality when it doesn't exist
        'mock>=1.0.0',
        'numpy>=1.4.0',
        'pandas>=0.11',
        'requests>=1.1',
        'suds-jurko',
        'future',
    ],
    extras_require={
        'pytables_caching': ['tables<=3.1.1']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=[
        'freezegun>=0.1.4',
        'pytest>=2.3.2',
        'httpretty==0.8.6',
        'html5lib',
    ],
    cmdclass={'test': PyTest},
)
