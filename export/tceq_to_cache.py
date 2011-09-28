"""
export tceq data to gems format
"""
import csv
from datetime import datetime
import glob
import os

from sqlalchemy import create_engine, func, Table
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy import (Column, Boolean, Integer, Text, String, Float,
                        DateTime, Enum)
from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
                                        synonym_for)
from sqlalchemy.orm import relationship, backref, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlite3 import dbapi2 as sqlite

from pyhis import cache

CACHE_DATABASE_FILE = "pyhis_tceq_cache.db"
CACHE_DATABASE_URI = 'sqlite:///' + CACHE_DATABASE_FILE

TCEQ_DATA_DIR = '/home/wilsaj/data/tceq/'

ECHO_SQLALCHEMY = True

TCEQ_SOURCE = 'TCEQFiles'
TCEQ_NETWORK = 'TCEQWaterQuality'
TCEQ_VOCABULARY = 'TCEQWaterQuality'


# to use geoalchemy with spatialite, the libspatialite library has to
# be loaded as an extension
# pyhis_engine = create_engine(CACHE_DATABASE_URI, convert_unicode=True,
#                              module=sqlite, echo=ECHO_SQLALCHEMY)
# PyhisSession = sessionmaker(autocommit=False, autoflush=False,
#                             bind=pyhis_engine)
# pyhis_session = PyhisSession()

cache.init_cache(CACHE_DATABASE_FILE, ECHO_SQLALCHEMY)


def create_sites_from_stations(stations_file):
    """read a stations file and create all the sites for that file"""
    file_source = cache.CacheSource(url='file:///' + TCEQ_SOURCE)
    with open(stations_file, 'rb') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            # there's some weird unicode in site 20828
            site_name = row['shortdesc'].replace('\xc2\x92', "'")
            site = cache.CacheSite(
                network=TCEQ_NETWORK,
                code=row['stationid'],
                name=site_name,
                latitude=row['latitude'],
                longitude=row['longitude'],
                source=file_source,
                auto_commit=False,
                skip_db_lookup=True)
    cache.db_session.commit()


def export_to_cache():
    csv_files = glob.glob('/'.join([TCEQ_DATA_DIR, '/*']))
    for csv_file in csv_files:
        # reinit cache to keep memory usage down
        cache.init_cache(CACHE_DATABASE_FILE, ECHO_SQLALCHEMY)
        with open(csv_file, 'rb') as f:
            reader = csv.DictReader(f)
            file_source = cache.CacheSource(url='file:///' + csv_file)

            variable_codes = (
                'barometric_pressure',
                'temperature',
                'dissolved_oxygen',
                'salinity',
                'turbidity')

            variables = dict([code, tpwd_cache_variable(code)]
                             for code in variable_codes)

            for row in reader:
                site_code = site_code_hash(
                    row['major_area_code'],
                    row['minor_bay_code'],
                    row['station_code'],
                    row['start_latitude_num'],
                    row['start_longitude_num'])

                site = cache.CacheSite(
                    network=TCEQ_NETWORK,
                    code=site_code,
                    latitude=row['start_latitude_num'],
                    longitude=row['start_longitude_num'],
                    source=file_source,
                    auto_commit=False)

                timestamp_format = '%d%b%Y:%H:%M:%S.000'
                timestamp = datetime.strptime(row['start_dttm'],
                                              timestamp_format)

                # skip dates from files that are not the 2009 files
                if timestamp.year == 2009 and not '20110524' in csv_file:
                    continue

                for code, cache_var in variables.items():
                    row_index = 'start_%s_num' % code
                    if row[row_index]:
                        timeseries = cache.CacheTimeSeries(
                            site=site,
                            variable=cache_var, )
                        timeseries.values.append(cache.DBValue(
                            timestamp=timestamp,
                            value=row[row_index],
                            timeseries=timeseries))

            cache.db_session.commit()


if __name__ == '__main__':
    cache.init_cache(CACHE_DATABASE_FILE, ECHO_SQLALCHEMY)
    stations_file = os.path.join(TCEQ_DATA_DIR, 'stations.txt')
    create_sites_from_stations(stations_file)
