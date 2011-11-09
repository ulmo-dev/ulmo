"""
PyHIS
-------

PyHIS is a python library for querying CUAHSI*-HIS** web services.


* CUAHSI is the Consortium of Universities for the
  Advancement of Hydrologic Science, Inc.
** HIS stands for Hydrologic Information System

"""

from setuptools import Command, setup, find_packages

setup(
    name='pyhis',
    version='0.1-alpha',
    license='BSD',
    author='Andy Wilson',
    author_email='wilson.andrew.j@gmail.com',
    description='a python library for querying data via CUAHSI-HIS '
                'web services',
    long_description=__doc__,
    keywords='his pyhis water waterml cuahsi wateroneflow',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'numpy>=1.4.0',
        'pandas>=0.3.0',
        'suds>=0.4',
        'quantities>=0.9.0',
        'sqlalchemy>=0.7.1',
        'attest>=0.5.0',
        'matplotlib'
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
        'attest>=0.5.0'
    ],
)
