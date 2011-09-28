"""
export tceq data to gems format
"""
import csv
import datetime
import glob
import os
import sys
import tempfile

from sqlalchemy import create_engine, func, Table
from sqlalchemy.schema import UniqueConstraint, ForeignKey
import sqlalchemy as sa
from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
                                        synonym_for)
from sqlalchemy.orm import relationship, backref, sessionmaker, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlite3 import dbapi2 as sqlite


TCEQ_DATABASE_FILE = "tceq_direct.db"
TCEQ_DATABASE_URI = 'sqlite:///' + TCEQ_DATABASE_FILE

TCEQ_DATA_DIR = '/home/wilsaj/data/tceq/'

ECHO_SQLALCHEMY = False

TCEQ_SOURCE = 'TCEQFiles'
TCEQ_NETWORK = 'TCEQWaterQuality'
TCEQ_VOCABULARY = 'TCEQWaterQuality'


tceq_engine = create_engine(TCEQ_DATABASE_URI, convert_unicode=True,
                            module=sqlite, echo=ECHO_SQLALCHEMY)
TceqSession = sessionmaker(autocommit=False, autoflush=False,
                            bind=tceq_engine)
tceq_session = TceqSession()

Base = declarative_base(bind=tceq_engine)


# ftp://ftp.tceq.state.tx.us/pub/WaterResourceManagement/WaterQuality/DataCollection/CleanRivers/public/stnsmeta.txt
class Site(Base):
    __tablename__ = 'site'

    id = sa.Column(sa.Integer, primary_key=True)
    basin_id = sa.Column(sa.Integer)
    tceq_station_id = sa.Column(sa.String)
    usgs_gauge_id = sa.Column(sa.String)
    short_description = sa.Column(sa.String)
    long_description = sa.Column(sa.Text)
    stream_station_location_type = sa.Column(sa.String)
    stream_station_condition_type = sa.Column(sa.String)
    county = sa.Column(sa.String)
    tceq_county_id = sa.Column(sa.Integer)
    stream_segment = sa.Column(sa.String)
    tceq_region = sa.Column(sa.Integer)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)
    nhd_reach = sa.Column(sa.Integer)
    on_segment = sa.Column(sa.String)


# # http://www.tceq.texas.gov/assets/public/compliance/monops/crp/data/ParameterCodeFieldDescriptions.pdf
# class Parameter(Base):
#     parameter_code
#     description
#     units
#     media
#     method


# http://www.tceq.state.tx.us/assets/public/compliance/monops/crp/data/event_struct.pdf
class Event(Base):
    __tablename__ = 'event'

    id = sa.Column(sa.Integer, primary_key=True)
    tag_id = sa.Column(sa.String, unique=True)
    # fk to site
    station_id = sa.Column(sa.String)
    end_date = sa.Column(sa.Date)
    end_time = sa.Column(sa.Time)
    end_depth = sa.Column(sa.Float)
    start_date = sa.Column(sa.Date)
    start_time = sa.Column(sa.Time)
    start_depth = sa.Column(sa.Float)
    # T=time, S=space, B=both, and F=flow weightpth
    category = sa.Column(sa.String)
    #called type ##/CN/GB
    number_of_samples = sa.Column(sa.String)
    comment = sa.Column(sa.Text)
    # fk to Chapter 4 of the Data Management Reference Guide
    submitting_entity = sa.Column(sa.String)
    # fk to Chapter 4 of the Data Management Reference Guide
    collecting_entity = sa.Column(sa.String)
    # fk TCEQ assigns valid codes, and they are listed in Chapter 4 of
    # the Data Management Reference Guide (e.g., RT=Routine ambient
    # sampling, BF=Sampling biased to high or low flow).ty
    monitoring_type = sa.Column(sa.String)
    results = relationship('Result', lazy='dynamic')


class Result(Base):
    __tablename__ = 'result'

    id = sa.Column(sa.Integer, primary_key=True)
    # fk to Event
    tag_id = sa.Column(sa.String, sa.ForeignKey('event.tag_id'))
    # must match event end_data
    end_date = sa.Column(sa.Date)
    parameter_code = sa.Column(sa.String)
    # value > or < quantification limits or blankmeter_code
    gtlt = sa.Column(sa.String)
    value = sa.Column(sa.Float)
    # limit of Detectionue
    limit_of_detection = sa.Column(sa.Float)
    # Limit of Quantification
    limit_of_quantification = sa.Column(sa.Float)
    # from chapter 9 of reference
    qualifier_code = sa.Column(sa.String)
    # if value outside max/min limits & TCEQ verifies as correct then = 1ode
    verify_flag = sa.Column(sa.Integer)


def create_sites(stations_file):
    """
    read a stations file and save all the stations in that file to the
    database
    """
    temp_file = clean_file(stations_file)
    with open(temp_file, 'rb') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            site = Site(
                basin_id=row['basinid'],
                tceq_station_id=row['stationid'],
                usgs_gauge_id=row['gaugeid'],
                short_description=row['shortdesc'],
                long_description=row['longdesc'],
                stream_station_location_type=row['streamtype'],
                stream_station_condition_type=row['streamtype2'],
                county=row['county'],
                tceq_county_id=row['tceqcountyid'],
                stream_segment=row['segment'],
                tceq_region=row['tceqregion'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                nhd_reach=row['nhdreachid'],
                on_segment=row['onsegflag'])
            tceq_session.add(site)
    tceq_session.commit()
    os.remove(temp_file)


def create_events(event_file):
    """
    read an event file and save all the events in that file to
    the database
    """
    temp_file = clean_file(event_file)
    with open(temp_file, 'rU') as f:
        # these aren't the data you're looking for
        if 'You requested' in f.readline():
            return
        f.seek(0)

        keys = ['tag_id', 'station_id', 'end_date', 'end_time', 'end_depth',
                'start_date', 'start_time', 'start_depth', 'category',
                'number_of_samples', 'comment', 'submitting_entity',
                'collecting_entity', 'monitoring_type']
        reader = csv.DictReader(f, delimiter='|', fieldnames=keys, quoting=csv.QUOTE_NONE)
        for row in reader:
            # skip non-unique tag id (see note at bottom of file)
            if row['tag_id'] == '3198440':
                continue

            event = Event(
                tag_id=row['tag_id'],
                station_id=row['station_id'],
                end_date=convert_date(row['end_date']),
                end_time=convert_time(row['end_time']),
                end_depth=row['end_depth'] if row['end_depth'] != '' else None,
                start_date=convert_date(row['start_date']),
                start_time=convert_time(row['start_time']),
                start_depth=row['start_depth'] if row['start_depth'] != '' else None,
                category=row['category'],
                number_of_samples=row['number_of_samples'],
                comment=row['comment'],
                submitting_entity=row['submitting_entity'],
                collecting_entity=row['collecting_entity'],
                monitoring_type=row['monitoring_type'])
            tceq_session.add(event)
        tceq_session.commit()
    os.remove(temp_file)


def create_results(results_file):
    """
    read a results file and save all the results in that file to
    the database
    """
    temp_file = clean_file(results_file)
    with open(temp_file, 'rb') as f:
        # these aren't the data you're looking for
        if 'You requested' in f.readline():
            return
        f.seek(0)

        keys = ['tag_id', 'end_date', 'parameter_code', 'gtlt', 'value',
                'limit_of_detection', 'limit_of_quantification',
                'qualifier_code', 'verify_flag']
        reader = csv.DictReader(f, delimiter='|', fieldnames=keys)
        for row in reader:
            result = Result(
                tag_id=row['tag_id'],
                end_date=convert_date(row['end_date']),
                parameter_code=row['parameter_code'],
                gtlt=row['gtlt'],
                value=row['value'],
                limit_of_detection=row['limit_of_detection'] if row['limit_of_detection'] != '' else None,
                limit_of_quantification=row['limit_of_quantification'] if row['limit_of_quantification'] != '' else None,
                qualifier_code=row['qualifier_code'],
                verify_flag=row['verify_flag'])
            tceq_session.add(result)
        tceq_session.commit()
    os.remove(temp_file)


def convert_date(datestr):
    """returns a date from a string formatted as MM/DD/YYYY"""
    date_split = datestr.split('/')
    if len(date_split) == 3:
        return datetime.date(int(date_split[2]), int(date_split[0]),
                             int(date_split[1]))
    else:
        return None


def convert_time(timestr):
    """returns a time from a string formatted as HH:SS"""
    time_split = timestr.split(':')
    if len(time_split) == 2:
        return datetime.time(int(time_split[0]), int(time_split[1]))
    else:
        return None


def clean_file(dirty_file_path):
    """returns a file path string for a temp file that is a cleaned up
    version of this file"""
    fh, temp_path = tempfile.mkstemp()
    temp_fid = open(temp_path, 'w')
    dirty_fid = open(dirty_file_path, 'rb')
    for line in dirty_fid:
        # 11_2005_1.psv has a few lines with extra pipes at the
        # beginning of them
        if line.startswith('|||'):
            temp_fid.write(line[3:])
        else:
            # 4_2001_1.psv contains null characters
            replace_line = line.replace('\x00', '% c')
            # 22_2009_1.psv contains \xbf for apostrophes
            replace_line = replace_line.replace('\xbf', "'")
            # stations file contains some weird ctrl sequence for apostrophes
            replace_line = replace_line.replace('\xc2\x92', "'")
            temp_fid.write(replace_line)
    temp_fid.close()
    dirty_fid.close()
    os.close(fh)
    return temp_path


if __name__ == '__main__':
    Base.metadata.create_all()
    stations_file = os.path.join(TCEQ_DATA_DIR, 'stations.txt')
    # create_sites(stations_file)
    # event_files = glob.glob('/'.join([TCEQ_DATA_DIR, '*_1.psv']))
    # found = False
    # for event_file in event_files:
    #     print "creating events for: %s" % event_file
    #     create_events(event_file)
    results_files = glob.glob('/'.join([TCEQ_DATA_DIR, '*_2.psv']))
    for results_file in results_files:
        if results_file == '/home/wilsaj/data/tceq/25_2011_2.psv':
            found = True
        if found:
            print "creating results for: %s" % results_file
            create_results(results_file)



# notes:
# events file tag id 3198440 does not appear to be unique
# file: 24_2010_1.psv line 112:
#     3198440|13302|06/09/2010|9:05|2.8|06/09/2010|9:00|2.8|Analytical Result|03||WC|FO|RT
# file: 22_1999_1.psv line 124:
#     3198440|13782|06/15/1999|10:42|4.5|||||||WC|FO|RT
