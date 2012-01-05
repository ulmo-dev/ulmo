from sqlalchemy import (Column, Integer, String,  DateTime)
from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
                                        DeclarativeMeta)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql.expression import asc, desc

from pyhis import cache


class USGSService(cache.Base):
    __tablename__ = 'usgs_service'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    sites = relationship('USGSSite', backref='service', lazy='dynamic')
    last_get_sites = Column(DateTime)


class USGSSite(cache.Base, cache.DBCacheDatesMixin):
    """Using inheritance with the SQLAlchemy declarative pattern is
    done via Mixin Classes. This class provides a Mixin Class for the
    Site DB model that can be used for both spatial and non-spatial
    database site models.
    """
    __tablename__ = 'usgs_site'
    __table_args__ = (
        UniqueConstraint('code', 'network', 'service_id'),
           Index('idx_%s_code_network_service_id' % __tablename__,
                 'code', 'network', 'service_id'),
            {}
            )
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    network = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    agency = Column(String)
    site_type = Column(String)
    huc = Column(String)
    state = Column(String)
    county = Column(String)

    service_id = Column(Integer, ForeignKey('usgs_service.id'), nullable=False)

    timeseries = relationship('USGSTimeSeries', lazy='dynamic')


class USGSVariable(cache.Base, cache.DBCacheDatesMixin):
    __tablename__ = 'usgs_variable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, index=True)
    network = Column(String)
    vocabulary = Column(String)
    description = Column(String)
    type = Column(String)
    unit = Column(String)
    no_data_value = Column(String)

    timeseries = relationship('USGSTimeSeries', lazy='dynamic')


class USGSTimeSeries(cache.Base, cache.DBCacheDatesMixin):
    __tablename__ = 'usgs_timeseries'
    __table_args__ = (
        UniqueConstraint('site_id', 'variable_id'),
        Index('idx_%s_site_id_variable_id' % __tablename__,
              'site_id', 'variable_id'),
        {}
        )

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('usgs_site.id'), nullable=False,
                     index=True)
    site = relationship('USGSSite', uselist=False)

    variable_id = Column(Integer, ForeignKey('usgs_variable.id'),
                         nullable=False)
    variable = relationship('USGSVariable', uselist=False)

    values = relationship('USGSValue', lazy='dynamic')


class USGSValue(cache.Base, cache.DBCacheDatesMixin):
    __tablename__ = 'usgs_value'
    __table_args__ = (
        UniqueConstraint('timeseries_id', 'timestamp'),
        Index('idx_%s_timeseries_id_timestamp' % __tablename__,
              'timeseries_id', 'timestamp'),
        {}
        )

    id = Column(Integer, primary_key=True)
    value = Column(String)
    timestamp = Column(DateTime)
    qualifiers = Column(String)

    timeseries_id = Column(Integer, ForeignKey('usgs_timeseries.id'),
                           nullable=False)
    timeseries = relationship('USGSTimeSeries', uselist=False)
