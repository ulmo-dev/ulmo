import csv
import datetime
import os

import requests

from pyhis import util

NCDC_GSOD_DIR = os.path.join(util._get_pyhis_dir(), 'ncdc_gsod')
NCDC_GSOD_STATIONS_FILE = os.path.join(NCDC_GSOD_DIR, 'ish-history.csv')
NCDC_GSOD_START_YEAR = 1929


def download_gsod_files(historical=False, start_year=None, end_year=None):
    """downloads Global Summary of Day data from ncdc and saves files in data directory

    Parameters
    ----------
    start_year : year to start downloads. default to current year
    end_year : year to end downloads. default to current year.
    historical : retrieves all available data. i.e start_year=1928, end_year=current year

    default retrieves current year. NCDC GSOD data is updated daily
    """
    _init_temp_dir()
    if historical:
        start_year = NCDC_GSOD_START_YEAR
        end_year = datetime.datetime.now().year

    if not end_year:
        end_year = datetime.datetime.now().year

    if not start_year:
        start_year = datetime.datetime.now().year

    base_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    CHUNK = 64 * 1024
    for year in range(start_year, end_year + 1):
        url = base_url + '/' + str(year) + '/' + 'gsod_' + str(year) + '.tar'
        filename = os.path.join(NCDC_GSOD_DIR, url.split('/')[-1])
        print 'retrieving ncdc gsod tar data file for {0}'.format(year)
        r = requests.get(url)
        download = r.raw
        with open(filename, 'wb') as f:
            # https://gist.github.com/1311816
            while True:
                chunk = download.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

        print 'file saved at {0}'.format(filename)


def download_stations_file():
    """download current station list and return filename
    """
    url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/ish-history.csv'
    r = requests.get(url)
    with open(NCDC_GSOD_STATIONS_FILE, 'wb') as f:
        f.write(r.content)
    print 'Saved station list {0}'.format(NCDC_GSOD_STATIONS_FILE)


def get_stations_list(update=True):
    """returns a dict of station dicts

    stations are keyed to their USAF-WBAN codes


    Parameters
    ----------
    update : if False, tries to use a cached copy of the stations file. If one
             can't be found or if update is True, then a new copy of the
             stations file is pulled from the web.
    """
    if update or not os.path.exists(NCDC_GSOD_STATIONS_FILE):
        download_stations_file()

    with open(NCDC_GSOD_STATIONS_FILE, 'rb') as f:
        reader = csv.DictReader(f)
        stations = {
            '-'.join([row['USAF'], row['WBAN']]): _process_station(row)
            for row in reader
        }
    return stations


def _process_station(station_row):
    """converts a csv row to a more human-friendly version"""
    station_dict = {
        'begin': station_row['BEGIN'],
        'call': station_row['CALL'],
        'country': station_row['CTRY'],
        'elevation': float(station_row['ELEV(.1M)']) * .1 \
                if station_row['ELEV(.1M)'] not in ('', '-99999') else None,
        'end': station_row['END'],
        'FIPS': station_row['FIPS'],
        'latitude': float(station_row['LAT']) * 0.001 \
                if station_row['LAT'] not in ('', '-99999') else None,
        'longitude': float(station_row['LON']) * 0.001 \
                if station_row['LON'] not in ('', '-999999') else None,
        'name': station_row['STATION NAME'],
        'state': station_row['STATE'],
        'USAF': station_row['USAF'],
        'WBAN': station_row['WBAN'],
    }
    return station_dict


def _init_temp_dir():
    if not os.path.exists(NCDC_GSOD_DIR):
        os.mkdir(NCDC_GSOD_DIR)
