"""
ulmo
----

an open source library for clean, simple and fast access to public hydrology and climatology data
"""

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


setup(
    name='ulmo',
    version='0.2.3-dev',
    license='BSD',
    author='Andy Wilson',
    author_email='wilson.andrew.j@gmail.com',
    description='clean, simple and fast access to public hydrology and climatology data',
    long_description=__doc__,
    keywords='his pyhis ulmo water waterml cuahsi wateroneflow',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'appdirs>=1.2.0',
        'isodate>=0.4.6',
        'lxml>=2.3',
        'matplotlib>=1.1.0',
        'numexpr>=2.0.1',
        'numpy>=1.4.0',
        'pandas>=0.9.1',
        'requests>=0.14.0',
        'suds>=0.4',
        'tables>=0.2.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=[
        'pytest>=2.3.2',
        'mock>=1.0.0',
    ],
    cmdclass={'test': PyTest},
)
