"""
    PyHIS.cache
    ~~~~~~~~~~

    SQLAlchemy-based caching support
"""
import platform

from sqlalchemy import create_engine, Table
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy import (Column, Boolean, Integer, Text, String, Float,
                        DateTime, Enum)
from sqlalchemy.ext.declarative import declarative_base, synonym_for
from sqlalchemy.orm import relationship, backref, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound

import pyhis


CACHE_DATABASE_FILE = "/tmp/pyhis_cache.db"
CACHE_DATABASE_URI = 'sqlite:///' + CACHE_DATABASE_FILE
ECHO_SQLALCHEMY = True

#XXX: this should be programmatically generated in some clever way
#     (e.g. based on some config)
USE_CACHE = True
USE_SPATIAL = False

try:
    from geoalchemy import GeometryColumn, GeometryDDL, Point, WKTSpatialElement
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    from sqlite3 import dbapi2 as sqlite
    USE_SPATIAL = False


# to use geoalchemy with spatialite, the libspatialite library has to
# be loaded as an extension
engine = create_engine(CACHE_DATABASE_URI, convert_unicode=True,
                       module=sqlite, echo=ECHO_SQLALCHEMY)

if USE_SPATIAL:
    if "ARCH" in platform.uname()[2]:
        LIBSPATIALITE_LOCATION="select load_extension('/usr/lib/libspatialite.so.1')"
    else:
        LIBSPATIALITE_LOCATION="select load_extension('/usr/lib/libspatialite.so.2')"

    if 'sqlite' in CACHE_DATABASE_URI:
        connection = engine.raw_connection().connection
        connection.enable_load_extension(True)
        engine.execute(LIBSPATIALITE_LOCATION)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = Session()

Base = declarative_base(bind=engine)

#----------------------------------------------------------------------------
# cache SQLAlchemy models
#----------------------------------------------------------------------------
class CacheSource(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    sites = relationship('CacheSite', backref='source')

    def __init__(self, url=None):
        self.url = url


if USE_SPATIAL:
    class CacheSite(Base):
        __tablename__ = 'site'

        id = Column(Integer, primary_key=True)
        site_id = Column(String)
        name = Column(String)
        code = Column(String)
        network = Column(String)
        source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
        geom = GeometryColumn(Point(2))
        timeseries = relationship('CacheTimeSeries', backref='site')

        @property
        def latitude(self):
            x, y = self.geom.coords(db_session)
            return y

        @property
        def longitude(self):
            x, y = self.geom.coords(db_session)
            return x

        # populated by backref:
        #   source = CacheSource

        def __init__(self, site_id=None, name=None, code=None, network=None,
                     source=None, latitude=None, longitude=None):
            self.site_id = site_id
            self.name = name
            self.code = code
            self.network = network
            self.source = source
            self.geom = WKTSpatialElement("POINT (%f %f)" %
                                          (longitude, latitude))

    GeometryDDL(CacheSite.__table__)

else:
    class CacheSite(Base):
        __tablename__ = 'site'

        id = Column(Integer, primary_key=True)
        site_id = Column(String)
        name = Column(String)
        code = Column(String)
        network = Column(String)
        source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)

        timeseries = relationship('CacheTimeSeries', backref='site')

        # populated by backref:
        #   source = CacheSource

        def __init__(self, site_id=None, name=None, code=None, network=None,
                     source=None, latitude=None, longitude=None):
            self.site_id = site_id
            self.name = name
            self.code = code
            self.network = network
            self.source = source
            self.latitude = latitude
            self.longitude = longitude


class CacheTimeSeries(Base):
    __tablename__ = 'timeseries'

    id = Column(Integer, primary_key=True)
    method = Column(String)
    quality_control_level = Column(String)
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    variable_id = Column(Integer, ForeignKey('variable.id'), nullable=False)

    variable = relationship('CacheVariable')
    values = relationship('CacheValue', backref='timeseries')

    # populated by backref:
    #   site = CacheSite

    def __init__(self, method=None, quality_control_level=None, site=None, variable=None):
        self.method = method
        self.quality_control_level = quality_control_level
        self.site = site
        self.variable = variable


class CacheUnits(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
    code = Column(String)

    # populated by backref:

    def __init__(self, name=None, abbreviation=None, code=None):
        self.name = name
        self.abbreviation = abbreviation
        self.code = code


class CacheValue(Base):
    __tablename__ = 'value'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    time = Column(DateTime)
    timeseries_id = Column(Integer, ForeignKey('timeseries.id'), nullable=False)



    def __init__(self, value=None, time=None, timeseries=None):
        self.value = value
        self.time = time
        self.timeseries = timeseries


class CacheVariable(Base):
    __tablename__ = 'variable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    variable_id = Column(String)
    vocabulary = Column(String)
    no_data_value = Column(String)
    units_id = Column(Integer, ForeignKey('units.id'), nullable=False)

    variable = relationship('CacheUnits')

    def __init__(self, name=None, code=None, variable_id=None, vocabulary=None,
                 no_data_value=None, site_id=None, units_id=None):
        self.name = name
        self.code = code
        self.variable_id = variable_id
        self.vocabulary = vocabulary
        self.no_data_value = no_data_value
        self.site_id = site_id
        self.units_id = units_id



# run create_all to make sure the database tables are all there
Base.metadata.create_all()


#----------------------------------------------------------------------------
# cache functions
#----------------------------------------------------------------------------
def _get_cached_sites_for_source(source):
    """returns a list of sites for a given pyhis.core.Source object"""
    try:
        cache_source = db_session.query(CacheSource).\
                       filter_by(url=source.url).one()
    except NoResultFound:
        return []

    return dict([(cached_site.code,
                  _get_site_from_cached_site(cached_site, source))
                 for cached_site in cache_source.sites])


def _get_site_from_cached_site(cached_site, source):
    return pyhis.Site(code=cached_site.code,
                      name=cached_site.name,
                      id=cached_site.site_id,
                      network=cached_site.network,
                      latitude=cached_site.latitude,
                      longitude=cached_site.longitude,
                      source=source)


def _update_cache_sites(sites, source):
    try:
        cache_source = db_session.query(CacheSource).\
                       filter_by(url=source.url).one()
    except NoResultFound:
        cache_source = CacheSource(url=source.url)
        db_session.add(cache_source)
        db_session.commit()


    for site in sites:
        cache_site = CacheSite(site_id=site.id,
                               name=site.name,
                               code=site.code,
                               network=site.network,
                               source=cache_source,
                               latitude=site.location.y,
                               longitude=site.location.x)
        db_session.add(cache_site)

    db_session.commit()
