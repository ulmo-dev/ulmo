import csv
import datetime
import gzip
import itertools
import os
import tarfile

import numpy as np
import requests

from pyhis import util

NCDC_GSOD_DIR = os.path.join(util.get_pyhis_dir(), 'ncdc_gsod')
NCDC_GSOD_STATIONS_FILE = os.path.join(NCDC_GSOD_DIR, 'ish-history.csv')
NCDC_GSOD_START_YEAR = 1929


def get_data(station_codes, start_date=None, end_date=None, parameters=None):
    if start_date:
        start_year = start_date.year
    else:
        start_year = NCDC_GSOD_START_YEAR
    if end_date:
        end_year = end_date.year
    else:
        end_year = datetime.datetime.now().year
    if parameters and not 'date' in parameters:
        # add date to list of parameters if it's not there already
        parameters.insert(0, 'date')

    for year in range(start_year, end_year + 1):
        return _get_gsod_data(station_codes, start_year, end_year, parameters)


def get_stations(update=True):
    """returns a dict of station dicts

    stations are keyed to their USAF-WBAN codes


    Parameters
    ----------
    update : if False, tries to use a cached copy of the stations file. If one
             can't be found or if update is True, then a new copy of the
             stations file is pulled from the web.
    """
    if update or not os.path.exists(NCDC_GSOD_STATIONS_FILE):
        _download_stations_file()

    with open(NCDC_GSOD_STATIONS_FILE, 'rb') as f:
        reader = csv.DictReader(f)
        stations = {
            _station_code(row): _process_station(row)
            for row in reader
        }
    return stations


def _download_gsod_file(year):
    base_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    CHUNK = 64 * 1024
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


def _download_stations_file():
    """download current station list"""
    url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/ish-history.csv'
    r = requests.get(url)
    with open(NCDC_GSOD_STATIONS_FILE, 'wb') as f:
        f.write(r.content)
    print 'Saved station list {0}'.format(NCDC_GSOD_STATIONS_FILE)


def _get_gsod_data(station_codes, start_year, end_year, parameters):
    # note: opening tar files and parsing the headers and such is a relatively
    # lengthy operation so you don't want to do it too often, hence try to
    # grab all stations at the same time per tarfile
    data_dict = {station_code: None for station_code in station_codes}

    for year in range(start_year, end_year + 1):
        tar_path = os.path.join(NCDC_GSOD_DIR, 'gsod_' + str(year) + '.tar')
        with tarfile.open(tar_path, 'r:') as gsod_tar:
            stations_in_file = [
                name.split('./')[-1].rsplit('-', 1)[0]
                for name in gsod_tar.getnames() if len(name) > 1]
            if station_codes:
                stations = list(set(station_codes) & set(stations_in_file))
            else:
                stations = stations_in_file
            for station in stations:
                year_data = _read_gsod_file(gsod_tar, station, year)
                if parameters:
                    year_data = year_data[parameters]
                if not year_data is None:
                    if not data_dict[station] is None:
                        data_dict[station] = np.append(data_dict[station], year_data)
                    else:
                        data_dict[station] = year_data
    return data_dict


def _init_temp_dir():
    ncdc_temp_dir = os.path.join(NCDC_GSOD_DIR, 'temp')
    if not os.path.exists(ncdc_temp_dir):
        os.makedirs(ncdc_temp_dir)


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


def _read_gsod_file(gsod_tar, station, year):
    tar_station_filename = station + '-' + str(year) + '.op.gz'
    try:
        gsod_tar.getmember('./' + tar_station_filename)
    except KeyError:
        return None

    ncdc_temp_dir = os.path.join(NCDC_GSOD_DIR, 'temp')
    temp_path = os.path.join(ncdc_temp_dir, tar_station_filename)

    gsod_tar.extract('./' + tar_station_filename, ncdc_temp_dir)
    with gzip.open(temp_path, 'rb') as gunzip_f:
        columns = [
            # name, length, # of spaces separating previous column
            ('USAF', 6, 0),
            ('WBAN', 5, 1),
            ('date', 8, 2),
            ('mean_temp', 6, 2),
            ('mean_temp_count', 2, 1),
            ('dew_point', 6, 2),
            ('dew_point_count', 2, 1),
            ('sea_level_pressure', 6, 2),
            ('sea_level_pressure_count', 2, 1),
            ('station_pressure', 6, 2),
            ('station_pressure_count', 2, 1),
            ('visibility', 5, 2),
            ('visibility_count', 2, 1),
            ('mean_wind_speed', 5, 2),
            ('mean_wind_speed_count', 2, 1),
            ('max_wind_speed', 5, 2),
            ('max_gust', 5, 2),
            ('max_temp', 6, 2),
            ('max_temp_flag', 1, 0),
            ('min_temp', 6, 1),
            ('min_temp_flag', 1, 0),
            ('precip', 5, 1),
            ('precip_flag', 1, 0),
            ('snow_depth', 5, 1),
            ('FRSHTT', 6, 2),
        ]

        dtype = np.dtype([
            (column[0], '|S%s' % column[1])
            for column in columns])

        # note: ignore initial 0
        delimiter = itertools.chain(*[column[1:][::-1] for column in columns])
        usecols = range(1, len(columns) * 2, 2)

        data_array = np.genfromtxt(gunzip_f, skip_header=1, delimiter=delimiter,
                usecols=usecols, dtype=dtype)
    os.remove(temp_path)

    data = _record_array_to_value_dicts(data_array)
    return data


def _record_array_to_value_dicts(record_array):
    keys = record_array.dtype.fields.keys()
    value_dicts = [
        {key: value[key] for key in keys}
        for value in record_array]
    return value_dicts


def _station_code(station):
    """returns station code from a station dict"""
    return '-'.join([station['USAF'], station['WBAN']])


if __name__ == '__main__':
    #_download_gsod_file(2012)
    stations = get_stations(update=False)
    texas_stations = [
        _station_code(station)
        for station in stations.values()
        if station['state'] == 'TX']
    data = get_data(texas_stations, datetime.datetime(2011, 1, 1),
            datetime.datetime.now(), parameters=['date', 'mean_temp', 'precip',
                'max_wind_speed'])
    import pdb; pdb.set_trace()
