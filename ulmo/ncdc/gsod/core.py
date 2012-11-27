import csv
import datetime
import gzip
import itertools
import os
import tarfile

import numpy as np

from ulmo import util

NCDC_GSOD_DIR = os.path.join(util.get_ulmo_dir(), 'ncdc/gsod')
NCDC_GSOD_STATIONS_FILE = os.path.join(NCDC_GSOD_DIR, 'ish-history.csv')
NCDC_GSOD_START_DATE = datetime.date(1929, 1, 1)


def get_data(station_codes, start_date=None, end_date=None, parameters=None):
    if start_date:
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
    else:
        start_date = NCDC_GSOD_START_DATE
    if end_date:
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
    else:
        end_date = datetime.datetime.now().date()
    if parameters and not 'date' in parameters:
        # add date to list of parameters if it's not there already
        parameters.insert(0, 'date')

    # note: opening tar files and parsing the headers and such is a relatively
    # lengthy operation so you don't want to do it too often, hence try to
    # grab all stations at the same time per tarfile
    data_dict = {station_code: None for station_code in station_codes}

    for year in range(start_date.year, end_date.year + 1):
        tar_path = _get_gsod_file(year)
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
                    # apply date ranges if they exist
                    if start_date or end_date:
                        mask = np.ones(len(year_data), dtype=bool)
                        if start_date:
                            mask = mask & (year_data['date'] >= start_date)
                        if end_date:
                            mask = mask & (year_data['date'] <= end_date)
                        year_data = year_data[mask]

                    if not data_dict[station] is None:
                        # XXX: this could be more efficient for large numbers
                        # of years with a list comprehension or generator
                        data_dict[station] = np.append(data_dict[station], year_data)
                    else:
                        data_dict[station] = year_data
    for key, data_array in data_dict.iteritems():
        if not data_dict[key] is None:
            data_dict[key] = _record_array_to_value_dicts(data_array)
    return data_dict


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


def _convert_date_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y%m%d').date()


def _download_stations_file():
    """download current station list"""
    url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/ish-history.csv'
    util.download_if_new(url, NCDC_GSOD_STATIONS_FILE, check_modified=True)
    print 'Saved station list {0}'.format(NCDC_GSOD_STATIONS_FILE)


def _get_gsod_file(year):
    base_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    print 'retrieving ncdc gsod tar data file for {0}'.format(year)
    url = base_url + '/' + str(year) + '/' + 'gsod_' + str(year) + '.tar'
    path = os.path.join(NCDC_GSOD_DIR, url.split('/')[-1])
    util.download_if_new(url, path, check_modified=True)
    #r = requests.get(url)
    print 'file saved at {0}'.format(path)
    return path


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
    util.mkdir_if_doesnt_exist(ncdc_temp_dir)
    temp_path = os.path.join(ncdc_temp_dir, tar_station_filename)

    gsod_tar.extract('./' + tar_station_filename, ncdc_temp_dir)
    with gzip.open(temp_path, 'rb') as gunzip_f:
        columns = [
            # name, length, # of spaces separating previous column, dtype
            ('USAF', 6, 0, 'S6'),
            ('WBAN', 5, 1, 'S5'),
            ('date', 8, 2, object),
            ('mean_temp', 6, 2, float),
            ('mean_temp_count', 2, 1, int),
            ('dew_point', 6, 2, float),
            ('dew_point_count', 2, 1, int),
            ('sea_level_pressure', 6, 2, float),
            ('sea_level_pressure_count', 2, 1, int),
            ('station_pressure', 6, 2, float),
            ('station_pressure_count', 2, 1, int),
            ('visibility', 5, 2, float),
            ('visibility_count', 2, 1, int),
            ('mean_wind_speed', 5, 2, float),
            ('mean_wind_speed_count', 2, 1, int),
            ('max_wind_speed', 5, 2, float),
            ('max_gust', 5, 2, float),
            ('max_temp', 6, 2, float),
            ('max_temp_flag', 1, 0, 'S1'),
            ('min_temp', 6, 1, float),
            ('min_temp_flag', 1, 0, 'S1'),
            ('precip', 5, 1, float),
            ('precip_flag', 1, 0, 'S1'),
            ('snow_depth', 5, 1, float),
            ('FRSHTT', 6, 2, 'S6'),
        ]

        dtype = np.dtype([
            (column[0], column[3])
            for column in columns])

        # note: ignore initial 0
        delimiter = itertools.chain(*[column[1:3][::-1] for column in columns])
        usecols = range(1, len(columns) * 2, 2)

        data = np.genfromtxt(gunzip_f, skip_header=1, delimiter=delimiter,
                usecols=usecols, dtype=dtype, converters={5: _convert_date_string})
    os.remove(temp_path)

    # somehow we can end up with single-element arrays that are 0-dimensional??
    # (occurs on tyler's machine but is hard to reproduce)
    if data.ndim == 0:
        data = data.flatten()

    return data


def _record_array_to_value_dicts(record_array):
    names = record_array.dtype.names
    value_dicts = [
        {name: value[name_index] for name_index, name in enumerate(names)}
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
    data = get_data(texas_stations, start_date=datetime.datetime(2012, 1, 1),
        end_date=datetime.datetime(2012, 2, 1))
    station_data = data[texas_stations[2]]
    import pandas
    df = pandas.DataFrame(station_data)
    import pdb; pdb.set_trace()
