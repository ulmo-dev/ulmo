"""
export data to gems format
"""
import csv
from datetime import datetime

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

CACHE_DATABASE_FILE = "/tmp/pyhis_tpwd_cache.db"
CACHE_DATABASE_URI = 'sqlite:///' + CACHE_DATABASE_FILE

TPWD_CSV_FILE = '/home/wilsaj/data/tpwd/request_20110510/aransas_20110510.csv'

ECHO_SQLALCHEMY = True

TPWD_NETWORK = 'TPWDCoastalFisheries'
TPWD_VOCABULARY = 'TPWDCoastalFisheries'


# to use geoalchemy with spatialite, the libspatialite library has to
# be loaded as an extension
# pyhis_engine = create_engine(CACHE_DATABASE_URI, convert_unicode=True,
#                              module=sqlite, echo=ECHO_SQLALCHEMY)
# PyhisSession = sessionmaker(autocommit=False, autoflush=False,
#                             bind=pyhis_engine)
# pyhis_session = PyhisSession()

cache.init_cache(CACHE_DATABASE_FILE, ECHO_SQLALCHEMY)


def tpwd_cache_variable(variable_code):
    return cache.CacheVariable(
        vocabulary = TPWD_VOCABULARY,
        code = variable_code,
        name = variable_code,
        )


def export_to_cache():
    with open(TPWD_CSV_FILE, 'rb') as f:
        reader = csv.DictReader(f)
        file_source = cache.CacheSource(url='file:///' + TPWD_CSV_FILE)

        variable_codes = (
            'barometric_pressure',
            'temperature',
            'dissolved_oxygen',
            'salinity',
            'turbidity')

        variables = dict([code, tpwd_cache_variable(code)]
                         for code in variable_codes)

        for row in reader:
            site = cache.CacheSite(
                network= TPWD_NETWORK,
                code=row['station_code'],
                latitude=row['start_latitude_num'],
                longitude=row['start_longitude_num'],
                source=file_source,
                auto_commit=False)

            timestamp_format = '%d%b%Y:%H:%M:%S.000'
            timestamp = datetime.strptime(row['completion_dttm'],
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


if __name__ == '__main__':
    export_to_cache()
