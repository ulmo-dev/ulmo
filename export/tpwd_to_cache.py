"""
export data to gems format
"""
import csv
from datetime import datetime
import glob
import itertools

from sqlalchemy import create_engine, func, Table
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy import (Column, Boolean, Integer, Text, String, Float,
                        DateTime, Enum)
from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
                                        synonym_for)
from sqlalchemy.orm import relationship, backref, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlite3 import dbapi2 as sqlite

import pyhis
from pyhis import cache

CACHE_DATABASE_FILE = "/tmp/pyhis_tpwd_cache.db"
CACHE_DATABASE_URI = 'sqlite:///' + CACHE_DATABASE_FILE

TPWD_CSV_DIRS = ['/home/wilsaj/data/tpwd/request_20110510/',
                 '/home/wilsaj/data/tpwd/request_20100401/']
TPWD_SOURCE_URL = 'TPWD_COASTAL_FISHERIES_DATA_REQUEST'

ECHO_SQLALCHEMY = False

TPWD_NETWORK = 'TPWDCoastalFisheries'
TPWD_VOCABULARY = 'TPWDCoastalFisheries'


# to use geoalchemy with spatialite, the libspatialite library has to
# be loaded as an extension
# pyhis_engine = create_engine(CACHE_DATABASE_URI, convert_unicode=True,
#                              module=sqlite, echo=ECHO_SQLALCHEMY)
# PyhisSession = sessionmaker(autocommit=False, autoflush=False,
#                             bind=pyhis_engine)
# pyhis_session = PyhisSession()


def create_variables_dict():
    return {
    'barometric_pressure': cache.CacheVariable(
        name='Barometric Pressure',
        code='barometric_pressure',
        vocabulary=TPWD_VOCABULARY,
        units=cache.CacheUnits(
            pyhis.Units(
                name='Inches of mercury',
                abbreviation='inches_hg',
                code='inches_hg'))),
    'temperature': cache.CacheVariable(
        name='Temperature',
        code='temperature',
        vocabulary=TPWD_VOCABULARY,
        units=cache.CacheUnits(
            pyhis.Units(
                name='Degrees Celcius',
                abbreviation='DegC',
                code='DegC'))),
    'dissolved_oxygen':  cache.CacheVariable(
        name='Dissolved Oxygen',
        code='dissolved_oxygen',
        vocabulary=TPWD_VOCABULARY,
        units=cache.CacheUnits(
            pyhis.Units(
                name='Parts per Million',
                abbreviation='ppm',
                code='ppm'))),
    'salinity': cache.CacheVariable(
        name='Salinity',
        code='salinity',
        vocabulary=TPWD_VOCABULARY,
        units=cache.CacheUnits(
            pyhis.Units(
                name='Parts per thousand',
                abbreviation='ppt',
                code='ppt'))),
    'turbidity':  cache.CacheVariable(
        name='Turbidity',
        code='turbidity',
        vocabulary=TPWD_VOCABULARY,
        units=cache.CacheUnits(
            pyhis.Units(
                name='NTU',
                abbreviation='ntu',
                code='ntu')))
    }


def export_to_cache():
    file_paths = set(itertools.chain(*[glob.glob(tpwd_dir + '/*')
                                       for tpwd_dir in TPWD_CSV_DIRS]))
    file_paths -= set([path for path in file_paths
                       if 'email_request' in path])

    for path in file_paths:
        # re-init cache, to clear cache dict
        cache.init_cache(CACHE_DATABASE_FILE, ECHO_SQLALCHEMY)
        print "exporting %s ..." % path
        export_file_to_cache(path)


def export_file_to_cache(csv_file):
    variables = create_variables_dict()
    create_sites_and_timeseries(csv_file)

    with open(csv_file, 'rb') as f:
        reader = csv.DictReader(f)
        file_source = cache.CacheSource(url=TPWD_SOURCE_URL)

        for row in reader:
            site_code = _generate_site_code(
                row['major_area_code'], row['minor_bay_code'],
                row['station_code'], row['start_latitude_num'],
                row['start_longitude_num'])

            site = cache.CacheSite(
                network=TPWD_NETWORK,
                code=site_code,
                name=site_code)

            timestamp_format = '%d%b%Y:%H:%M:%S.000'
            timestamp = datetime.strptime(row['start_dttm'],
                                          timestamp_format)

            for code, cache_var in variables.items():
                timeseries = cache.CacheTimeSeries(
                    site=site,
                    variable=cache_var, )
                row_index = 'start_%s_num' % code
                if row[row_index]:
                    timeseries.values.append(cache.DBValue(
                        timestamp=timestamp,
                        value=row[row_index],
                        timeseries=timeseries))

        cache.db_session.commit()


def create_sites_and_timeseries(csv_file):
    """
    Run through the file and create/cache all the sites and timeseries
    values we'll need. Commits are expensive, so doing this up front
    means we only need to commit a few times.
    """
    variables = create_variables_dict()

    with open(csv_file, 'rb') as f:
        reader = csv.DictReader(f)
        file_source = cache.CacheSource(url=TPWD_SOURCE_URL)

        sites = set([(_generate_site_code(row['major_area_code'],
                                          row['minor_bay_code'],
                                          row['station_code'],
                                          row['start_latitude_num'],
                                          row['start_longitude_num']),
                      row['start_latitude_num'],
                      row['start_longitude_num'])
                     for row in reader])

        cache_sites = [cache.CacheSite(
            network=TPWD_NETWORK,
            code=site[0],
            latitude=site[1],
            longitude=site[2],
            source=file_source,
            auto_add=False,
            auto_commit=False)
                       for site in sites]

        cache.db_session.add_all(cache_sites)

        for cache_var in variables.values():
            timeseries_list = [cache.CacheTimeSeries(
                site=site,
                variable=cache_var,
                auto_add=False,
                auto_commit=False)
                               for site in cache_sites]
            cache.db_session.add_all(timeseries_list)

        cache.db_session.commit()


def _generate_site_code(major_area_code, minor_bay_code, station_code,
                        latitude, longitude):
    """returns a site code suitable for establishing unique sites for
    TPWD Coastal Fisheries measurements

    Arguments:
    - `major_area_code`: TPWD major_area_code
    - `minor_bay_code`: TPWD minor_bay_code
    - `station_code`: TPWD station code
    - `latitude`: latitude in decimal degrees
    - `longitude`: longtitude in decimal degrees
    """
    return '_'.join([major_area_code, minor_bay_code, station_code,
                     _generate_lat_long_hash(latitude, longitude)])


def _generate_lat_long_hash(latitude, longitude):
    """Generate a hash of the latitude and longitude for building a site code

    Arguments:
    - `latitude`: latitude in decimal degrees
    - `longitude`: longtitude in decimal degrees
    """
    return (str(latitude)[-4:] + str(longitude)[-4:]).replace('.', '0')


if __name__ == '__main__':
    export_to_cache()
