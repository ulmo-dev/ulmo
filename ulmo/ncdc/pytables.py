import datetime
import os

import tables

from ulmo.ncdc import core
from ulmo import util

# default hdf5 file path
HDF5_FILE_PATH = util.get_default_h5file_path()


class NCDCValue(tables.IsDescription):
    date = tables.StringCol(8)
    flag = tables.StringCol(1)
    value = tables.StringCol(20)
    last_modified = tables.StringCol(26)


def get_data(station_codes, start_date=None, end_date=None, parameters=None,
        path=None):
    if isinstance(station_codes, basestring):
        return _get_station_data(station_codes, start_date, end_date,
                parameters)
    else:
        return_dict = {}
        for station_code in station_codes:
            return_dict[station_code] = _get_station_data(station_codes,
                    start_date, end_date, parameters)


def get_stations(update=True, path=None):
    #XXX: we should have a fast pytables version of stations list
    return core.get_stations(update=update)


def update_data(station_codes=None, start_year=None, end_year=None, path=None):
    if not os.path.exists(path):
        _init_h5(path)
    if not start_year:
        last_updated = _last_updated()
        if not last_updated:
            start_year = core.NCDC_GSOD_START_DATE.year
        else:
            start_year = last_updated.year
    if not end_year:
        end_year = datetime.datetime.now().year

    all_stations = get_stations()
    if station_codes:
        stations = {
                station_code: all_stations.get(station_code)
                for station_code in station_codes
                if station_code in all_stations
        }
    else:
        stations = all_stations

    for year in range(start_year, end_year + 1):
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year, 12, 31)
        data = core.get_data(stations.keys(), start_date=start_date,
                end_date=end_date)
        for station_code, station_data in data.iteritems():
            station = stations.get(station_code)
            if not station_data is None:
                _update_station_data(station, station_data, path)


def _get_station_data(station_code, start_date=None, end_date=None, parameters=None):
    pass


def _get_value_table(h5file, station, variable):
    """returns a value table for a given open h5file (writable), station and
    variable. If the value table already exists, it is returned. If it doesn't,
    it will be created.
    """
    gsod_values_path = '/ncdc/gsod/values'
    station_code = core._station_code(station)
    station_path = '/'.join((gsod_values_path, station_code))
    util.get_or_create_group(h5file, station_path, "station %s" % station_code)

    value_table_name = variable
    values_path = '/'.join([station_path, value_table_name])

    try:
        value_table = h5file.getNode(values_path)
    except tables.exceptions.NoSuchNodeError:
        value_table = util.get_or_create_table(
            h5file, values_path, NCDCValue,
            "Values for station: %s, variable: %s" % (station_code, variable))
        value_table.cols.date.createCSIndex()
        value_table.attrs.USAF = station['USAF']
        value_table.attrs.WBAN = station['WBAN']
        value_table.attrs.name = station['name']

    return value_table


def _init_h5(path=None):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    if not path:
        path = HDF5_FILE_PATH
    with tables.openFile(path, mode='a', title="pyHIS data") as h5file:
        ncdc = h5file.createGroup('/', 'ncdc', 'NCDC Data')
        gsod = h5file.createGroup(ncdc, 'gsod', 'Global Summary of the Day')
        h5file.createGroup(gsod, 'values', 'Values')


def _last_updated():
    """returns date of last update"""
    #TODO: implement
    return datetime.datetime.now()


def _update_station_data(station, station_data, path=None):
    if not path:
        path = HDF5_FILE_PATH
    with tables.openFile(path, mode='a') as h5file:
        #XXX: assumes first dict is representative of all dicts
        variables = station_data[0].keys()

        for variable in variables:
            value_table = _get_value_table(h5file, station, variable)
            util.update_or_append_sortable(value_table, station_data, 'date')


if __name__ == '__main__':
    test_path = '/User/wilsaj/test/pyhis_test.h5'
    _init_h5()
    stations = get_stations(update=False)
    texas_stations = [
        code
        for code, station in stations.iteritems()
        if station['state'] == 'TX']
    update_data(texas_stations, 2012, 2012, path=test_path)
    import pdb; pdb.set_trace()
