from builtins import range
from past.builtins import basestring
import datetime

import tables

from ulmo.ncdc.gsod import core
from ulmo import util

# default hdf5 file path
HDF5_FILE_PATH = util.get_default_h5file_path()

raise NotImplementedError("ncdc.gsod.pytables is still a work in progress")


class NCDCValue(tables.IsDescription):
    date = tables.StringCol(8)
    flag = tables.StringCol(1)
    value = tables.StringCol(20)
    last_modified = tables.StringCol(26)


def get_data(station_codes, start=None, end=None, parameters=None,
        path=None):
    if isinstance(station_codes, basestring):
        return _get_station_data(station_codes, start, end,
                parameters)
    else:
        return_dict = {}
        for station_code in station_codes:
            return_dict[station_code] = _get_station_data(station_codes,
                    start, end, parameters)


def get_stations(update=True, path=None):
    #XXX: we should have a fast pytables version of stations list
    return core.get_stations(update=update)


def update_data(station_codes=None, start_year=None, end_year=None, path=None):
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
        stations = dict([
                (station_code, all_stations.get(station_code))
                for station_code in station_codes
                if station_code in all_stations
        ])
    else:
        stations = all_stations

    for year in range(start_year, end_year + 1):
        start = datetime.datetime(year, 1, 1)
        end = datetime.datetime(year, 12, 31)
        data = core.get_data(list(stations.keys()), start=start, end=end)
        for station_code, station_data in data.items():
            station = stations.get(station_code)
            if not station_data is None:
                _update_station_data(station, station_data, path)


def _get_station_data(station_code, start=None, end=None, parameters=None):
    pass


def _get_value_table(h5file, station, variable):
    """returns a value table for a given open h5file (writable), station and
    variable. If the value table already exists, it is returned. If it doesn't,
    it will be created.
    """
    gsod_values_path = '/ncdc/gsod/values'
    station_code = core._station_code(station)
    station_path = '/'.join((gsod_values_path, station_code))
    util.get_or_create_group(h5file, station_path, "station %s" % station_code,
            createparents=True)

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


def _last_updated():
    """returns date of last update"""
    #TODO: implement
    return datetime.datetime.now()


def _update_station_data(station, station_data, path=None):
    if not path:
        path = HDF5_FILE_PATH
    with util.open_h5file(path, mode='a') as h5file:
        #XXX: assumes first dict is representative of all dicts
        variables = list(station_data[0].keys())

        for variable in variables:
            value_table = _get_value_table(h5file, station, variable)
            util.update_or_append_sortable(value_table, station_data, 'date')


if __name__ == '__main__':
    test_path = '/Users/wilsaj/test/pyhis_test.h5'
    stations = get_stations(update=False, path=test_path)
    texas_stations = [
        code
        for code, station in stations.items()
        if station['state'] == 'TX']
    update_data(texas_stations, 2012, 2012, path=test_path)
    import pdb; pdb.set_trace()
