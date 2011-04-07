"""
PyHIS
-------

PyHIS is a python library for querying CUAHSI*-HIS** web services.


* CUAHSI is the Consortium of Universities for the
  Advancement of Hydrologic Science, Inc.
** HIS stands for Hydrlogic Information System

"""

from setuptools import Command, setup, find_packages

setup(
    name='PyHIS',
    version='0.1-alpha',
    license='BSD',
    author='Andy Wilson',
    author_email='wilson.andrew.j+pyhis@gmail.com',
    description='a python library for querying data via CUAHSI-HIS '
                'web services',
    long_description=__doc__,
    keywords='his pyhis water waterml cuahsi wateroneflow',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'suds>=0.4',
        'shapely>=1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
