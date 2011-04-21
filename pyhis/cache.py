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
from sqlalchemy.ext.declarative import declarative_base, declared_attr, synonym_for
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


# in-memory cache dict that will keep us from creating multiple cache
# objects that represent the same DB objects
_cache = {
    'source': {},
    'site': {},
    'timeseries': {},
    'variable': {},
    'units': {},
    }


#----------------------------------------------------------------------------
# cache SQLAlchemy models
#----------------------------------------------------------------------------

def create_cache_obj(db_model, cache_key, lookup_key_func, db_lookup_func):
    """
    Create a cache object - this saves some boilerplate
    """

    class CacheObj(object):
        def __new__(cls, *args, **kwargs):
            lookup_key = lookup_key_func(*args, **kwargs)
            if lookup_key in _cache[cache_key]:
                return _cache[cache_key][lookup_key]

            try:
                db_instance = db_lookup_func(*args, **kwargs)
            except NoResultFound:
                db_instance = db_model(*args, **kwargs)

            _cache[cache_key][lookup_key] = db_instance
            return db_instance

    return CacheObj


class DBSource(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    sites = relationship('DBSite', backref='source')

    def __init__(self, source=None, url=None):
        if not source is None:
            self._create_from_pyhis(source)
        else:
            self.url = url

    def _create_from_pyhis(self, pyhis_source):
        self.url = pyhis_source.url

    def to_pyhis(self):
        return pyhis.Source(wsdl_url=self.url)


def _source_lookup_key_func(source=None, url=None):
    if not source is None:
        return source.url
    if url:
        return url


def _source_db_lookup_func(source=None, url=None):
    if not source is None:
        url = source.url

    return db_session.query(DBSource).filter_by(url=url).one()

CacheSource = create_cache_obj(DBSource, 'source', _source_lookup_key_func,
                               _source_db_lookup_func)


class DBSiteMixin(object):
    """
    Using inheritance with the SQLAlchemy declarative pattern is done
    via Mixin Classes. This class provides a Mixin Class for the Site
    DB model that can be used for both spatial and non-spatial
    database site models.
    """
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    site_id = Column(String)
    name = Column(String)
    code = Column(String)
    network = Column(String)

    @declared_attr
    def source_id(cls):
        return Column(Integer, ForeignKey('source.id'), nullable=False)

    @declared_attr
    def timeseries(cls):
        return relationship('DBTimeSeries', backref='site')

    # populated by backref:
    #   source = DBSource

    def _create_from_pyhis(self, pyhis_site):
        self.site_id = pyhis_site.id
        self.name = pyhis_site.name
        self.code = pyhis_site.code
        self.network = pyhis_site.network
        self.latitude = pyhis_site.location.y
        self.longitude = pyhis_site.location.x
        self.source = CacheSource(pyhis_site.source)

    def to_pyhis(self, source=None):
        # because every site needs a reference to a source, a source
        # object *should* be passed to this method to avoid an extra
        # object being created. Some proxy voodoo could that could go
        # on here to prevent this. For now, assume that if we didn't
        # get a source, then just make a new one.
        if source is None:
            source = self.source.to_pyhis()

        return pyhis.Site(
            code=self.code,
            name=self.name,
            id=self.site_id,
            network=self.network,
            latitude=self.latitude,
            longitude=self.longitude,
            source=source)


if USE_SPATIAL:
    class DBSite(Base, DBSiteMixin):
        geom = GeometryColumn(Point(2))

        def __init__(self, site=None, site_id=None, name=None, code=None,
                     network=None, source=None, latitude=None, longitude=None):
            if site:
                self._create_from_pyhis(site)
            else:
                self.site_id = site_id
                self.name = name
                self.code = code
                self.network = network
                self.source = source
                self.latitude = latitude
                self.longitude = longitude

        @property
        def latitude(self):
            x, y = self.geom.coords(db_session)
            return y

        @latitude.setter
        def latitude(self, latitude):
            wkt_point = "POINT(%f %f)" % (self.longitude, latitude)
            self.geom = WKTSpatialElement(wkt_point)

        @property
        def longitude(self):
            x, y = self.geom.coords(db_session)
            return x

        @longitude.setter
        def longitude(self, longitude):
            wkt_point = "POINT(%f %f)" % (longitude, self.latitude)
            self.geom = WKTSpatialElement(wkt_point)

    GeometryDDL(DBSite.__table__)

else:
    class DBSite(Base, DBSiteMixin):
        latitude = Column(Float)
        longitude = Column(Float)

        def __init__(self, site=None, site_id=None, name=None, code=None,
                     network=None, source=None, latitude=None, longitude=None):
            if site:
                self._create_from_pyhis(site)
            else:
                self.site_id = site_id
                self.name = name
                self.code = code
                self.network = network
                self.source = source
                self.latitude = latitude
                self.longitude = longitude



def _site_lookup_key_func(site=None, network=None, code=None):
    if site:
        return (site.network, site.code)

    if name and network:
        return (network, code)


def _site_db_lookup_func(site=None, network=None, code=None):
    if site:
        network  = site.network
        code = site.code

    return db_session.query(DBSite).filter_by(network=network,
                                              code=code).one()

CacheSite = create_cache_obj(DBSite, 'site', _site_lookup_key_func,
                             _site_db_lookup_func)


class DBTimeSeries(Base):
    __tablename__ = 'timeseries'

    id = Column(Integer, primary_key=True)
    begin_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    method = Column(String)
    quality_control_level = Column(String)
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    variable_id = Column(Integer, ForeignKey('variable.id'), nullable=False)

    variable = relationship('DBVariable')
    values = relationship('DBValue', order_by="DBValue.timestamp")

    # populated by backref:
    #   site = DBSite

    def __init__(self, timeseries=None, begin_datetime=None,
                 end_datetime=None, method=None, quality_control_level=None,
                 site=None, variable=None):
        if timeseries:
            self._create_from_pyhis(timeseries)
        else:
            self.begin_datetime = begin_datetime
            self.end_datetime = end_datetime
            self.method = method
            self.quality_control_level = quality_control_level
            self.site = site
            self.variable = variable

    def _create_from_pyhis(self, pyhis_timeseries):
        self.method = pyhis_timeseries.method
        self.begin_datetime = pyhis_timeseries.begin_datetime
        self.end_datetime = pyhis_timeseries.end_datetime
        self.quality_control_level = pyhis_timeseries.quality_control_level
        self.site = CacheSite(pyhis_timeseries.site)
        self.variable = CacheVariable(pyhis_timeseries.variable)


    def to_pyhis(self, site=None, variable=None):
        # as with DBSite.to_pyhis()...
        # because every timeseries needs a reference to a site and a
        # varaible, these objects *should* be passed to this method to
        # avoid extra objects being created. Some proxy voodoo could
        # that could go on here to prevent this. For now, assume that
        # if we didn't get a reference to an existing object, then
        # just make a new one.
        if site is None:
            site = self.site.to_pyhis()

        if variable is None:
            variable = self.variable.to_pyhis()

        return pyhis.TimeSeries(
            variable=variable,
            count=len(self.values),
            method=self.method,
            quality_control_level=self.quality_control_level,
            begin_datetime=self.begin_datetime,
            end_datetime=self.end_datetime,
            site=site)


def _timeseries_lookup_key_func(timeseries=None, network=None, site_code=None,
                                variable=None):
    if timeseries:
        return (timeseries.site.network, timeseries.site.code,
                timeseries.variable.code)
    if network and site_code and variable:
        return (network, site_code, variable)


def _timeseries_db_lookup_func(timeseries=None, network=None, site_code=None,
                                variable=None):
    if timeseries:
        network  = timeseries.site.network
        site_code = timeseries.site.code
        variable = db_session.query(DBVariable).filter_by(
            code=timeseries.variable.code).one()

    if network and site_code and variable:
        variable_code = variable.code

    site = db_session.query(DBSite).filter_by(network=network,
                                              code=site_code).one()
    return db_session.query(DBTimeSeries).filter_by(site=site,
                                                    variable=variable).one()

CacheTimeSeries = create_cache_obj(DBTimeSeries, 'timeseries',
                                   _timeseries_lookup_key_func,
                                   _timeseries_db_lookup_func)


class DBUnits(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
    code = Column(String)

    def __init__(self, units=None, name=None, abbreviation=None, code=None):
        if units:
            self._create_from_pyhis(units)
        else:
            self.name = name
            self.abbreviation = abbreviation
            self.code = code

    def _create_from_pyhis(self, pyhis_units):
        self.name = pyhis_units.name
        self.abbreviation = pyhis_units.abbreviation
        self.code = pyhis_units.code

    def to_pyhis(self):
        return pyhis.Units(
            name=self.name,
            abbreviation=self.abbreviation,
            code=self.code)


def _units_lookup_key_func(units=None, name=None, code=None):
    if units:
        return (units.name, units.code)
    if name and code:
        return (name, code)


def _units_db_lookup_func(units=None, name=None, code=None):
    if units:
        name = units.name
        code = units.code

    return db_session.query(DBUnits).filter_by(name=name,
                                               code=code).one()

CacheUnits = create_cache_obj(DBUnits, 'units', _units_lookup_key_func,
                              _units_db_lookup_func)


# note: value shouldn't need a cache object
class DBValue(Base):
    __tablename__ = 'value'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    timestamp = Column(DateTime)
    timeseries_id = Column(Integer, ForeignKey('timeseries.id'),
                           nullable=False)

    def __init__(self, value=None, time=None, timeseries=None):
        self.value = value
        self.timestamp = timestamp
        self.timeseries = timeseries


class DBVariable(Base):
    __tablename__ = 'variable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    variable_id = Column(String)
    vocabulary = Column(String)
    no_data_value = Column(String)
    units_id = Column(Integer, ForeignKey('units.id'), nullable=False)

    units = relationship('DBUnits')

    def __init__(self, variable=None, name=None, code=None, variable_id=None,
                 vocabulary=None, no_data_value=None, site_id=None,
                 units=None):
        if variable:
            self._create_from_pyhis(variable)
        else:
            self.name = name
            self.code = code
            self.variable_id = variable_id
            self.vocabulary = vocabulary
            self.no_data_value = no_data_value
            self.units = units

    def _create_from_pyhis(self, pyhis_variable):
        self.name = pyhis_variable.name
        self.code = pyhis_variable.code
        self.variable_id = pyhis_variable.id
        self.vocabulary = pyhis_variable.vocabulary
        self.no_data_value = pyhis_variable.no_data_value
        self.units = CacheUnits(pyhis_variable.units)

    def to_pyhis(self):
        return pyhis.Variable(
            name=self.name,
            code=self.code,
            id=self.variable_id,
            vocabulary=self.vocabulary,
            units=self.units.to_pyhis())


def _variable_lookup_key_func(variable=None, vocabulary=None, code=None):
    if variable:
        return (variable.vocabulary, variable.code)
    if vocabulary and code:
        return (vocabulary, code)


def _variable_db_lookup_func(variable=None, vocabulary=None, code=None):
    if variable:
        vocabulary = variable.vocabulary
        code = variable.code

    return db_session.query(DBVariable).filter_by(vocabulary=vocabulary,
                                                  code=code).one()

CacheVariable = create_cache_obj(DBVariable, 'variable',
                                 _variable_lookup_key_func,
                                 _variable_db_lookup_func)


# run create_all to make sure the database tables are all there
Base.metadata.create_all()


#----------------------------------------------------------------------------
# cache functions
#----------------------------------------------------------------------------
def _get_cached_sites(source):
    """returns a list of sites for a given pyhis.core.Source object"""
    try:
        cached_source = db_session.query(DBSource).\
                        filter_by(url=source.url).one()
    except NoResultFound:
        return []

    return dict([(cached_site.code,
                  cached_site.to_pyhis(source))
                 for cached_site in cached_source.sites])


def _update_cache_sites(sites, source):
    try:
        cached_source = db_session.query(DBSource).\
                       filter_by(url=source.url).one()
    except NoResultFound:
        cached_source = CacheSource(url=source.url)
        db_session.add(cached_source)
        db_session.commit()


    for site in sites:
        cache_site = CacheSite(site=site)
        db_session.add(cache_site)

    db_session.commit()


def _get_cached_timeseries_list(site):
    """
    returns a list of timeseries objects for a given pyhis.core.Site
    object
    """
    try:
        cached_site = db_session.query(DBSite).\
                      filter_by(code=site.code).one()
        cached_timeseries_list = db_session.query(DBTimeSeries).\
                                 filter_by(site=cached_site)
    except NoResultFound:
        return []

    return [cached_timeseries.to_pyhis(site)
            for cached_timeseries in cached_timeseries_list]


def _update_cache_timeseries(site):
    try:
        cached_site = db_session.query(DBSite).\
                      filter_by(code=site.code).one()
    except NoResultFound:
        cached_site = CacheSite(site)
        db_session.add(cached_site)
        db_session.commit()

    for timeseries in site.timeseries_list:
        try:
            cached_variable = db_session.query(DBVariable).\
                              filter_by(code=timeseries.variable.code,
                                        vocabulary=timeseries.variable.vocabulary).one()
        except NoResultFound:
            cached_variable = CacheVariable(timeseries.variable)
            db_session.add(cached_variable)
            db_session.commit()

        cache_timeseries = CacheTimeSeries(
            timeseries=timeseries)
        db_session.add(cache_timeseries)

    db_session.commit()


def get_db_obj(DBModel, filter_by_dict, update=True):
    """
    Either get an instance from DBModel or, if it doesn't exist,
    then update the cache.
    """
    try:
        cache_obj = db_session.query(DBModel).\
                    filter_by(**filter_by_dict).one()
    except NoResultFound:
        if update:
            cache_obj = DBModel(cache_obj)
            db_session.add(cache_obj)
            db_session.commit()
        else:
            return False

    return cache_obj
