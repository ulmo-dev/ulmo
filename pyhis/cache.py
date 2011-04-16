"""
    PyHIS.cache
    ~~~~~~~~~~

    SQLAlchemy-based caching support
"""
import platform

from geoalchemy import GeometryColumn, GeometryDDL, Point, WKTSpatialElement
from pysqlite2 import dbapi2 as sqlite
from sqlalchemy import create_engine, Table
from sqlalchemy.schema import UniqueConstraint, ForeignKey
from sqlalchemy import (Column, Boolean, Integer, Text, String, Float,
                        DateTime, Enum)
from sqlalchemy.ext.declarative import declarative_base, synonym_for
from sqlalchemy.orm import relationship, backref, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound

import pyhis


CACHE_DATABASE_URI = 'sqlite:////tmp/pyhis_cache.db'

if "ARCH" in platform.uname()[2]:
    LIBSPATIALITE_LOCATION="select load_extension('/usr/lib/libspatialite.so.1')"
else:
    LIBSPATIALITE_LOCATION="select load_extension('/usr/lib/libspatialite.so.2')"


#XXX: this should be programmatically generated in some clever way
#     (e.g. based on some config)
use_cache = True


# to use geoalchemy with spatialite, the libspatialite library has to
# be loaded as an extension
engine = create_engine(CACHE_DATABASE_URI, convert_unicode=True,
                       module=sqlite, echo=True)

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


class CacheSite(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    site_id=Column(String)
    name = Column(String)
    code = Column(String)
    network = Column(String)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    geom = GeometryColumn(Point(2))

    def __init__(self, site_id=None, name=None, code=None, network=None,
                 source=None, latitude=None, longitude=None):
        self.site_id = site_id
        self.name = name
        self.code = code
        self.network = network
        self.source = source
        self.geom = WKTSpatialElement("POINT (%f %f)" %
                                      (longitude, latitude))

    # populated by backref:
    #   source = CacheSource

GeometryDDL(CacheSite.__table__)




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

    return [_get_site_from_cached_site(cached_site, source.suds_client)
            for cached_site in cache_source.sites]


def _get_site_from_cached_site(cached_site, suds_client):
    return pyhis.Site(code=cached_site.code,
                      name=cached_site.name,
                      id=cached_site.site_id,
                      network=cached_site.network,
                      latitude=db_session.scalar(cached_site.geom.y),
                      longitude=db_session.scalar(cached_site.geom.x),
                      client=suds_client)


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
