"""
ulmo
----

an open source library for clean, simple and fast access to public hydrology and climatology data
"""

from setuptools import Command, setup, find_packages

setup(
    name='ulmo',
    version='0.1-alpha',
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
        'pandas>=0.8.0',
        'requests==0.13.0',
        'suds>=0.4',
        'tables'
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
