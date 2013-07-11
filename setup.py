from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open('README.rst') as f:
    # use README for long description but don't include the link to travis-ci;
    # it seems a bit out of place on pypi since it applies to the development
    # version
    long_description = ''.join([
        line for line in f.readlines()
        if 'travis-ci' not in line])


# this sets __version__
exec(open('ulmo/version.py'))


setup(
    name='ulmo',
    version=__version__,
    license='BSD',
    author='Andy Wilson',
    author_email='wilson.andrew.j@gmail.com',
    description='clean, simple and fast access to public hydrology and climatology data',
    long_description=long_description,
    url='https://github.com/twdb/ulmo/',
    keywords='his pyhis ulmo water waterml cuahsi wateroneflow',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'appdirs>=1.2.0',
        'beautifulsoup4>=4.1.3',
        'isodate>=0.4.6',
        'lxml>=2.3',
        # mock is required for mocking pytables-related functionality when it doesn't exist
        'mock>=1.0.0',
        'numpy>=1.4.0',
        'pandas>=0.10.1',
        'requests>=1.1',
        'suds>=0.4',
    ],
    extras_require={
        'pytables_caching': ['tables>=0.2.3']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=[
        'freezegun>=0.1.4',
        'pytest>=2.3.2',
        'httpretty>=0.5.8',
    ],
    cmdclass={'test': PyTest},
)
