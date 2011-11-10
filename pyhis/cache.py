"""
    PyHIS.cache
    ~~~~~~~~~~

    SQLAlchemy-based caching support
"""
#----------------------------------------------------------------------------
# cache should work like this:
#  1. check in-memory cache, if found return the obj
#  2. if not check database, if found return the obj and update in-memory cache
#  3. if not in database, make new network request, update database
#     with results and update the in-memory cache
#----------------------------------------------------------------------------
from datetime import datetime, timedelta
import logging
import os
import tempfile
import warnings

import pandas
import sqlalchemy as sa
from sqlalchemy import (Column, Integer, String, Float, DateTime)
from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
                                        DeclarativeMeta)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql.expression import desc
import suds

import pyhis
from pyhis import waterml
from pyhis.exceptions import NoDataError


USE_SPATIAL = True
try:
    from geoalchemy import (GeometryColumn, GeometryDDL, Point,
                            WKTSpatialElement)
except ImportError:
    USE_SPATIAL = False

CACHE_DATABASE_FILE = os.path.join(tempfile.gettempdir(), "pyhis_cache.db")
ECHO_SQLALCHEMY = False

#XXX: this should be programmatically generated in some clever way
#     (e.g. based on some config)
USE_CACHE = True

# If the difference between now and the last time a these parts of the
# cache were last refreshed, then make a new request and update the
# cache
CACHE_EXPIRES = {
    'get_sites': timedelta(days=7),
    'timeseries': timedelta(days=7)
    }

# If there are more than these values in a value count, break the
# request into a set of smaller requests - this is important for
# services which can return huge amounts of data which can swamp
# memory
MAX_VALUE_COUNT = 50000
DEFAULT_SMALL_REQUEST_INTERVAL = timedelta(days=180)

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


Session = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()

# initialize db_session to None so we can easily test for its
# existence and close it if necessary
db_session = None

_cache = {}


def init_cache(cache_database_uri=CACHE_DATABASE_FILE,
               echo=ECHO_SQLALCHEMY, use_spatial=False, schema=None):
    global engine
    global db_session
    global _cache
    global USE_SPATIAL

    # USE_SPATIAL = use_spatial

    if schema:
        update_models_schema(schema)

    if not '://' in cache_database_uri:
        cache_database_uri = 'sqlite:///' + cache_database_uri

    engine = sa.create_engine(cache_database_uri, convert_unicode=True,
                              echo=echo)

    # if we are reinitializing cache, close the old session
    if db_session:
        db_session.commit()
        db_session.close()

    # bind new engine to the db_session and Base metadata objects
    db_session = Session(bind=engine)
    Base.metadata.bind = engine

    # in-memory cache dict that will keep us from creating multiple cache
    # objects that represent the same DB objects
    _cache = {
        'service': {},       # key: url
        'site': {},         # key: (service_url, network, site_code)
        'timeseries': {},   # key: (service_url, network, site_code, variable_code)
        'variable': {},     # key: (vocabulary, variable_code)
        'units': {},        # key: (name, code)
        }

    log.info('cache initialized with database: %s' % cache_database_uri)

    # there is probably a cleaner way to do this, but the idea is to
    # try to run create_all_tables; this won't work if the DB objects
    # haven't been initialized (i.e. on import), but if init_cache is
    # called post-import (meaning the database file is changed), then
    # the tables need to be created
    try:
        create_all_tables()
    except NameError:
        pass


init_cache()


def clear_memory_cache():
    """Clean out the in-memory cache dict. This is useful for
    large/long-running programs that might be using up all available
    memory.
    """
    global _cache
    _cache = {
        'service': {},       # key: url
        'site': {},         # key: (service_url, network, site_code)
        'timeseries': {},   # key: (service_url, network, site_code, variable_code)
        'variable': {},     # key: (vocabulary, variable_code)
        'units': {},        # key: (name, code)
        }


#----------------------------------------------------------------------------
# cache SQLAlchemy models
#----------------------------------------------------------------------------
def create_cache_obj(db_model, cache_key, lookup_key_func, db_lookup_func):
    """Create a cache object that searches the in-memory cache dict
    for the key returned by calling lookup_key_func. If no object is
    found matching this key, then call db_lookup_func to search the
    database. If no result is found in the database, then create a new
    database object, save it to the database and return the new
    object.
    """

    class CacheObj(object):
        def __new__(cls, *args, **kwargs):
            #: add a check for an auto_commit kwarg that determines
            #: whether or not to automatically commit an obj to the db
            #: cache (if it doesn't already exist in db)
            auto_commit = kwargs.pop('auto_commit', True)
            auto_add = kwargs.pop('auto_add', auto_commit)
            skip_db_lookup = kwargs.pop('skip_db_lookup', False)

            lookup_key = lookup_key_func(*args, **kwargs)
            if lookup_key in _cache[cache_key]:
                return _cache[cache_key][lookup_key]

            if skip_db_lookup:
                db_instance = db_model(*args, **kwargs)
                if auto_add:
                    db_session.add(db_instance)
                if auto_commit:
                    db_session.commit()
            else:
                try:
                    db_instance = db_lookup_func(*args, **kwargs)
                except NoResultFound, SkipDBLookup:
                    db_instance = db_model(*args, **kwargs)
                    if auto_add:
                        db_session.add(db_instance)
                    if auto_commit:
                        db_session.commit()

            _cache[cache_key][lookup_key] = db_instance
            return db_instance

    return CacheObj


#----------------------------------------------------------------------------
# Mixin classes
#----------------------------------------------------------------------------
class DBCacheDatesMixin(object):
    """Mixin class for keeping track of cache times"""
    last_refreshed = Column(DateTime, default=sa.func.now(),
                            onupdate=sa.func.now())


#----------------------------------------------------------------------------
# Database models
#----------------------------------------------------------------------------
class DBService(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    sites = relationship('DBSite', backref='service', lazy='dynamic')
    last_get_sites = Column(DateTime)

    def __init__(self, service=None, url=None):
        if not service is None:
            self._from_pyhis(service)
        else:
            self.url = url

    def _from_pyhis(self, pyhis_service):
        self.url = pyhis_service.url

    def to_pyhis(self):
        return pyhis.Service(wsdl_url=self.url)


def _service_lookup_key_func(service=None, url=None):
    if not service is None:
        return service.url
    if url:
        return url


def _service_db_lookup_func(service=None, url=None):
    if not service is None:
        url = service.url

    return db_session.query(DBService).filter_by(url=url).one()

CacheService = create_cache_obj(DBService, 'service', _service_lookup_key_func,
                               _service_db_lookup_func)


class DBSiteMixin(object):
    """Using inheritance with the SQLAlchemy declarative pattern is
    done via Mixin Classes. This class provides a Mixin Class for the
    Site DB model that can be used for both spatial and non-spatial
    database site models.
    """
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    site_id = Column(String)
    name = Column(String)
    code = Column(String)
    network = Column(String)

    @declared_attr
    def service_id(cls):
        return Column(Integer, ForeignKey('service.id'), nullable=False)

    @declared_attr
    def timeseries_list(cls):
        return relationship('DBTimeSeries', backref='site', lazy='dynamic')

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('network', 'code'),
#            Index('idx_%s_network_code' % cls.__tablename__,
#                  'network', 'code'),
            {}
            )

    # populated by backref:
    #   service = DBService

    def _from_pyhis(self, pyhis_site):
        self.site_id = pyhis_site.id
        self.name = pyhis_site.name
        self.code = pyhis_site.code
        self.network = pyhis_site.network
        self.latitude = pyhis_site.latitude
        self.longitude = pyhis_site.longitude
        self.service = CacheService(pyhis_site.service)

    def to_pyhis(self, service=None):
        # because every site needs a reference to a service, a service
        # object *should* be passed to this method to avoid an extra
        # object being created. Some proxy voodoo could that could go
        # on here to prevent this. For now, assume that if we didn't
        # get a service, then just make a new one.
        if service is None:
            service = self.service.to_pyhis()

        return pyhis.Site(
            code=self.code,
            name=self.name,
            id=self.site_id,
            network=self.network,
            latitude=self.latitude,
            longitude=self.longitude,
            service=service)

if USE_SPATIAL:
    class DBSite(Base, DBSiteMixin, DBCacheDatesMixin):
        #: geom column to hold lat/long
        the_geom = GeometryColumn(Point(2))

        @property
        def latitude(self):
            x, y = self.the_geom.coords(db_session)
            return y

        @latitude.setter
        def latitude(self, latitude):
            wkt_point = "POINT(%f %f)" % (self.longitude, float(latitude))
            self.the_geom = WKTSpatialElement(wkt_point)

        @property
        def longitude(self):
            x, y = self.the_geom.coords(db_session)
            return x

        @longitude.setter
        def longitude(self, longitude):
            wkt_point = "POINT(%f %f)" % (float(longitude), self.latitude)
            self.the_geom = WKTSpatialElement(wkt_point)

        def __init__(self, site=None, site_id=None, name=None, code=None,
                     network=None, service=None, latitude=0, longitude=0):
            self.the_geom = WKTSpatialElement("POINT(%f %f)" % (latitude, longitude))
            if site:
                self._from_pyhis(site)
            else:
                self.site_id = site_id
                self.name = name
                self.code = code
                self.network = network
                self.service = service

    GeometryDDL(DBSite.__table__)

else:
    class DBSite(Base, DBSiteMixin, DBCacheDatesMixin):

        latitude = Column(Float)
        longitude = Column(Float)

        def __init__(self, site=None, site_id=None, name=None, code=None,
                     network=None, service=None, latitude=None, longitude=None):
            if site:
                self._from_pyhis(site)
            else:
                self.site_id = site_id
                self.name = name
                self.code = code
                self.network = network
                self.service = service
                self.latitude = latitude
                self.longitude = longitude


def _site_lookup_key_func(site=None, network=None, code=None, **kwargs):
    if site:
        return (site.network, site.code)
    if network and code:
        return (network, code)


def _site_db_lookup_func(site=None, network=None, code=None, **kwargs):
    if site:
        network = site.network
        code = site.code

    return db_session.query(DBSite).filter_by(network=network,
                                              code=code).one()

CacheSite = create_cache_obj(DBSite, 'site', _site_lookup_key_func,
                             _site_db_lookup_func)


class DBTimeSeries(Base, DBCacheDatesMixin):
    __tablename__ = 'timeseries'

    id = Column(Integer, primary_key=True)
    begin_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    method = Column(String)
    quality_control_level = Column(String)
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    variable_id = Column(Integer, ForeignKey('variable.id'), nullable=False)
    value_count = Column(Integer)

    variable = relationship('DBVariable')
    values = relationship('DBValue',
                          cascade='save-update, merge, delete, delete-orphan',
                          lazy='dynamic', backref='timeseries')

    # populated by backref:
    #   site = DBSite

    def __init__(self, timeseries=None, begin_datetime=None,
                 end_datetime=None, method=None, quality_control_level=None,
                 site=None, variable=None, value_count=None):
        if timeseries:
            self._from_pyhis(timeseries)
        else:
            self.begin_datetime = begin_datetime
            self.end_datetime = end_datetime
            self.method = method
            self.quality_control_level = quality_control_level
            self.site = site
            self.variable = variable
            self.value_count = value_count

    def _from_pyhis(self, pyhis_timeseries):
        self.method = pyhis_timeseries.method
        self.begin_datetime = pyhis_timeseries.begin_datetime
        self.end_datetime = pyhis_timeseries.end_datetime
        self.quality_control_level = pyhis_timeseries.quality_control_level
        self.variable = CacheVariable(pyhis_timeseries.variable)
        self.site = CacheSite(pyhis_timeseries.site, auto_commit=False)
        self.value_count = pyhis_timeseries.value_count

    def to_pyhis(self, site=None, variable=None):
        # as with DBSite.to_pyhis()...
        # because every timeseries needs a reference to a site and a
        # variable, these objects *should* be passed to this method to
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
            method=self.method,
            quality_control_level=self.quality_control_level,
            begin_datetime=self.begin_datetime,
            end_datetime=self.end_datetime,
            site=site,
            value_count=self.value_count)


def _timeseries_lookup_key_func(timeseries=None, url=None, network=None,
                                site_code=None, variable=None, site=None,
                                **kwargs):
    if timeseries:
        return (timeseries.site.service.url, timeseries.site.network,
                timeseries.site.code, timeseries.variable.code)
    if site and variable:
        return (site.service.url, site.network, site.code, variable.code)
    if url and network and site_code and variable:
        return (url, network, site_code, variable.code)


def _timeseries_db_lookup_func(timeseries=None, network=None, site_code=None,
                                variable=None, site=None, **kwargs):
    if timeseries:
        network = timeseries.site.network
        site_code = timeseries.site.code
        variable = db_session.query(DBVariable).filter_by(
            vocabulary=timeseries.variable.vocabulary,
            code=timeseries.variable.code).one()

    if network and site_code and variable:
        variable_code = variable.code

    if not site:
        site = db_session.query(DBSite).filter_by(network=network,
                                                  code=site_code).one()
    return db_session.query(DBTimeSeries).filter_by(site=site,
                                                    variable=variable).one()

CacheTimeSeries = create_cache_obj(DBTimeSeries, 'timeseries',
                                   _timeseries_lookup_key_func,
                                   _timeseries_db_lookup_func)


class DBUnits(Base, DBCacheDatesMixin):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
    code = Column(String)

    def __init__(self, units=None, name=None, abbreviation=None, code=None):
        if units:
            self._from_pyhis(units)
        else:
            self.name = name
            self.abbreviation = abbreviation
            self.code = code

    def _from_pyhis(self, pyhis_units):
        self.name = pyhis_units.name
        self.abbreviation = pyhis_units.abbreviation
        self.code = pyhis_units.code

    def to_pyhis(self):
        return pyhis.Units(
            name=self.name,
            abbreviation=self.abbreviation,
            code=self.code)


def _units_lookup_key_func(units=None, name=None, code=None, **kwargs):
    if units:
        return (units.name, units.code)
    if name and code:
        return (name, code)


def _units_db_lookup_func(units=None, name=None, code=None, **kwargs):
    if units:
        name = units.name
        code = units.code

    return db_session.query(DBUnits).filter_by(name=name,
                                               code=code).one()

CacheUnits = create_cache_obj(DBUnits, 'units', _units_lookup_key_func,
                              _units_db_lookup_func)


class DBValue(Base, DBCacheDatesMixin):
    __tablename__ = 'value'
    __table_args__ = (
        Index('idx_value_timestamp_timeseries_id',
              'timestamp', 'timeseries_id'),)

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    timestamp = Column(DateTime)
    timeseries_id = Column(Integer, ForeignKey('timeseries.id'),
                           nullable=False)

    def __init__(self, value=None, timestamp=None, timeseries=None):
        self.value = value
        self.timestamp = timestamp
        self.timeseries = timeseries


class DBVariable(Base, DBCacheDatesMixin):
    __tablename__ = 'variable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    variable_id = Column(String)
    vocabulary = Column(String)
    no_data_value = Column(String)
    units_id = Column(Integer, ForeignKey('units.id'))

    units = relationship('DBUnits')

    def __init__(self, variable=None, name=None, code=None, variable_id=None,
                 vocabulary=None, no_data_value=None, units=None):
        if not variable is None:
            self._from_pyhis(variable)
        else:
            self.name = name
            self.code = code
            self.variable_id = variable_id
            self.vocabulary = vocabulary
            self.no_data_value = no_data_value
            self.units = units

    def _from_pyhis(self, pyhis_variable):
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


def _variable_lookup_key_func(variable=None, vocabulary=None, code=None,
                              **kwargs):
    if variable:
        return (variable.vocabulary, variable.code)
    if vocabulary and code:
        return (vocabulary, code)


def _variable_db_lookup_func(variable=None, vocabulary=None, code=None,
                             **kwargs):
    if variable:
        vocabulary = variable.vocabulary
        code = variable.code

    return db_session.query(DBVariable).filter_by(vocabulary=vocabulary,
                                                  code=code).one()

CacheVariable = create_cache_obj(DBVariable, 'variable',
                                 _variable_lookup_key_func,
                                 _variable_db_lookup_func)


def create_all_tables():
    """run create_all to make sure the database tables are all there"""
    Base.metadata.create_all()


def update_models_schema(schema):
    def is_a_pyhis_cache_model(x):
        return getattr(x, '__module__', None) == 'pyhis.cache' and isinstance(x, DeclarativeMeta)

    pyhis_cache_models = filter(is_a_pyhis_cache_model, globals().values())
    for model in pyhis_cache_models:
        model.__table__.schema = schema

create_all_tables()


#----------------------------------------------------------------------------
# cache functions
#----------------------------------------------------------------------------
def cache_all(service_url, update_values=None):
    """Cache all available data for a service"""
    service = pyhis.Service(service_url)
    cache_sites(service.sites.values(), update_values=update_values)


def cache_sites(sites, update_values=None):
    """Cache all available data for a collection of sites"""
    total_sites = len(sites)

    for i, site in enumerate(sites, 1):
        # this could be improved by not having to create the
        # dataframe object
        # try:
        log.info('caching values for site %s/%s: %s' %
                 (i, total_sites, site.name))

        # update the timeseries dict, which will automatically
        # cache the values then delete it to free up the memory
        for timeseries in site.timeseries.values():
            try:
                cache_timeseries(timeseries, update_values=update_values)
            except suds.WebFault as fault:
                warnings.warn(
                    "There was a problem getting values for %s:%s\n%s " % (
                        site, timeseries, fault))
            except NoDataError as e:
                warnings.warn(str(e))
            except Exception as e:
                pass
            _clear_timeseries_from_memory_cache(timeseries)

        _clear_site_from_memory_cache(site)
        # except Exception as e:
        #     import pdb; pdb.set_trace()
        #     warnings.warn("There was a problem getting values for "
        #                   "%s, skipping..." % (site))


def _clear_site_from_memory_cache(site):
    """clears the potentially weighty parts of a cached site from
    in-memory cache (like site response and Timeseries objects). This
    can keep the memory footprint of long running scripts from
    ballooning, but it means that you won't have the performance
    advantage of having these objects in the in-memory cache after
    this function is called. Note: these objects won't be gc'd if
    there are references to them somewhere else (e.g. a service object
    that still holds a reference to the site object in its sites
    dict).
    """
    for timeseries in site._timeseries_dict.values():
        try:
            _clear_timeseries_from_memory_cache(timeseries)
        except KeyError:
            pass

    site_vars_to_delete = (
        '_timeseries_dict',
        '_site_info_response')

    for site_var in site_vars_to_delete:
        try:
            delattr(site, site_var)
        except AttributeError:
            pass

    try:
        site_cache_key = _site_lookup_key_func(site)
        del _cache['site'][site_cache_key]
    except KeyError:
        pass


def _clear_timeseries_from_memory_cache(timeseries):
    """clears a timeseries from the in-memory cache"""
    timeseries_cache_key = _timeseries_lookup_key_func(timeseries)
    del _cache['timeseries'][timeseries_cache_key]


def get_sites_for_service(service):
    """return a dict of pyhis.Site objects for a given service. The
    service can be either a string representing the url or a
    pyhis.Service object
    """
    cached_service = CacheService(service)

    if not cached_service.last_get_sites or \
           _need_to_update_service(cached_service):
        site_list = waterml.get_sites_for_service(cached_service.to_pyhis())

        # since the sites don't exist in the db yet, just
        # instantiating them via the CacheSite constructor will
        # queue them to be saved to the db and (update them in the
        # in-memory cache)
        skip_db_lookup = bool(cached_service.sites.count() == 0)
        cache_sites = [CacheSite(site, auto_commit=False,
                                 skip_db_lookup=skip_db_lookup)
                       for site in site_list.values()]

        # add queued sites to cache
        db_session.add_all(cache_sites)

        # update cached_service.last_get_sites
        cached_service.last_get_sites = sa.func.now()

        # commit
        db_session.commit()

    return dict([(cached_site.code,
                  cached_site.to_pyhis(service))
                 for cached_site in cached_service.sites])


def get_site(service, network, code):
    """return a pyhis.Site for a given service, network and
    site_code. The service can be either a string representing the url
    or a pyhis.Service object
    """
    cached_service = CacheService(service)

    try:
        cached_site = _site_db_lookup_func(network=network, code=code)
        return cached_site.to_pyhis()
    except NoResultFound:
        pyhis_site = pyhis.core.Site(network=network, code=code,
                                     service=cached_service.to_pyhis())
        CacheSite(site=pyhis_site)
        return pyhis_site


def get_timeseries_dict_for_site(site):
    """returns a dict of pyhis.TimeSeries objects with the variable
    code as keys for a given site and variable_code
    """
    cached_site = CacheSite(site)

    if cached_site.timeseries_list.count() == 0:
        timeseries_dict = waterml.\
                          get_timeseries_dict_for_site(cached_site.to_pyhis())
        # Since the timeseries don't exist in the db yet, just
        # instantiating them via the CacheSite constructor will save
        # them to the db and (update them in the in-memory
        # cache). This can be expensive if there are a lot of
        # timeseries objects, so we defer commits until they have all
        # been instantiated and can be commited at once.
        timeseries_list = [CacheTimeSeries(timeseries, auto_commit=False,
                                           skip_db_lookup=True)
                           for timeseries in timeseries_dict.values()]
        db_session.add_all(timeseries_list)
        db_session.commit()

        return timeseries_dict

    # else:
    timeseries_list = [cached_timeseries.to_pyhis(site=site)
                       for cached_timeseries in cached_site.timeseries_list]
    return dict([(timeseries.variable.code, timeseries)
                 for timeseries in timeseries_list])


def get_series_and_quantity_for_timeseries(
    timeseries, check_for_updates=False, defer_commit=False):
    """returns a tuple where the first element is a pandas.Series
    containing the timeseries data for the timeseries and the second
    element is the python quantity that corresponds the unit for the
    variable. Takes a suds WaterML TimeSeriesResponseType object.
    """
    cached_timeseries = CacheTimeSeries(timeseries)

    if check_for_updates or \
           _need_to_update_timeseries(cached_timeseries, timeseries):
        series, quantity = \
                waterml.get_series_and_quantity_for_timeseries(timeseries)

        _cache_series_values(series, cached_timeseries,
                             defer_commit=defer_commit)
        num_db_values = cached_timeseries.values.count()
        if num_db_values != cached_timeseries.value_count:
            warnings.warn("value_count (%s) doesn't match number of values (%s) for %s:%s" %
                          (cached_timeseries.value_count, num_db_values,
                           cached_timeseries.site.name,
                           cached_timeseries.variable.code))

        return series, quantity

    series_dict = dict([(cached_value.timestamp, cached_value.value)
                        for cached_value in cached_timeseries.values])
    series = pandas.Series(series_dict)

    # look for the unit code in the unit_quantities dict, if it's not
    # there just use the unit name
    unit_code = cached_timeseries.variable.units.code
    try:
        quantity = pyhis.unit_quantities[unit_code]
    except KeyError:
        quantity = cached_timeseries.variable.units.name
        variable_code = cached_timeseries.variable.code
        warnings.warn("Unit conversion not available for %s: %s [%s]" %
                      (variable_code, quantity, unit_code))

    return series, quantity


def cache_timeseries(timeseries, force_intervals=False,
                     small_request_interval=None, update_values=None):
    """cache all values for a timeseries

    update_values can be one of several types of values: If
    update_values is None or False, then it will only add new records,
    and further more it will only add records AFTER the latest
    timestamp for a particular timeseries. This can be much faster if
    you know the service you're hitting won't be updating old data. In
    this case, you will only be requesting new data. If update_values
    is a datetime, it will force an update of values after that
    date. If update_values is a datetime.timedelta object, then it
    will force an update of values of since the timedelta amount of
    time since the last record in the database. This is a good choice
    for services which provide provisional data that may be qa/qc'd or
    changed after for a short period of time, but then it becomes more
    or less permanent. If update_values is True, then it will request
    and update ALL records in the database.
    """
    cached_timeseries = CacheTimeSeries(timeseries)

    if update_values == True:
        start_time = timeseries.begin_datetime
    elif update_values == None or update_values == False:
        last_value = cached_timeseries.values.order_by(
            desc(DBValue.timestamp)).first()
        if last_value:
            start_time = last_value.timestamp
        else:
            start_time = timeseries.begin_datetime
    elif type(update_values) == datetime:
        start_time = update_values
    elif type(update_values) == timedelta:
        last_value = cached_timeseries.values.order_by(
            desc(DBValue.timestamp)).first()
        start_time = last_value.timestamp - timedelta
    else:
        raise TypeError("update_values must be either: None, False, True, a datetime.datetime object, or a datetime.timedelta object")

    if start_time >= cached_timeseries.end_datetime:
        return
    if timeseries.value_count < MAX_VALUE_COUNT and force_intervals == False:
        series, quantity = \
                waterml.get_series_and_quantity_for_timeseries(
            timeseries,
            begin_date_str=start_time.strftime('%Y-%m-%d'))
        _cache_series_values(series, cached_timeseries,
                             update_values=update_values)
    else:
        request_interval = DEFAULT_SMALL_REQUEST_INTERVAL
        end_time = start_time + request_interval
        while end_time < timeseries.end_datetime:
            begin_date_str=start_time.strftime('%Y-%m-%d')
            end_date_str=end_time.strftime('%Y-%m-%d')
            series, quantity = \
                    waterml.get_series_and_quantity_for_timeseries(
                timeseries,
                begin_date_str=begin_date_str,
                end_date_str=end_date_str)
            _cache_series_values(series, cached_timeseries,
                                 update_values=update_values)
            start_time = end_time
            end_time = start_time + request_interval


def _cache_series_values(series, cached_timeseries, defer_commit=False,
                         update_values=None):
    """Adds all the values in a pandas series to the database cache,
    associating them with the DBTimeSeries object cached_timeseries.
    """

    # quit early if the series is empty
    if not len(series):
        return None

    start_time = series.keys()[0]
    end_time = series.keys()[-1]

    db_values = cached_timeseries.values.filter(
        DBValue.timestamp.between(start_time, end_time)).all()

    for timestamp, value in series.iteritems():
        match_values = filter(
            lambda db_value: db_value.timestamp == timestamp,
            db_values)
        if len(match_values):
            match_value = match_values[0]
            match_value.value = value
        else:
            cached_timeseries.values.append(
                DBValue(value=value, timestamp=timestamp,
                        timeseries=cached_timeseries))

    if not defer_commit:
        db_session.commit()


def _need_to_update_service(cached_service):
    time_since_last_cached = datetime.now() - cached_service.last_get_sites
    return bool(time_since_last_cached > CACHE_EXPIRES['get_sites'])


def _need_to_update_timeseries(cached_timeseries, pyhis_timeseries):
    number_of_cached_values = cached_timeseries.values.count()

    if number_of_cached_values == 0:
        return True

    if number_of_cached_values != pyhis_timeseries.value_count:
        # it seems that value_count is not very reliable - lots of
        # services get it wrong, so we only update if value_count is
        # off and we are outside of our pre-determined cache window
        time_since_last_cached = datetime.utcnow() - cached_timeseries.last_refreshed
        return bool(time_since_last_cached > CACHE_EXPIRES['timeseries'])

    try:
        if cached_timeseries.values[0].timestamp == pyhis_timeseries.begin_datetime \
            and cached_timeseries.values[-1].timestamp == pyhis_timeseries.end_datetime:
            return False
    except KeyError:
        return True

    return True
