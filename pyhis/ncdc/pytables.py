import os
import tempfile

import tables

from pyhis.ncdc import core
from pyhis import util

# default hdf5 file path
HDF5_FILE_PATH = util.get_default_h5file()


class NCDCValue(tables.IsDescription):
    date = tables.StringCol(8)
    flag = tables.StringCol(1)
    value = tables.StringCol(20)
    last_modified = tables.StringCol(26)


def get_stations(update=True, path=None):
    #XXX: we should have a fast pytables version of stations list
    return core.get_stations(update=update)


    ncdc = h5file.createGroup('/', 'ncdc', 'NCDC Data')
    gsod = h5file.createGroup(ncdc, 'gsod', 'Global Summary of the Day')
    h5file.createGroup(gsod, 'values', 'Values')
    h5file.close()



def _get_value_table(h5file, site, variable):
    """returns a value table for a given open h5file (writable), site and
    variable. If the value table already exists, it is returned. If it doesn't,
    it will be created.
    """
    gsod_path = '/ncdc/gsod'
    site_group = site['name']
    site_path = '/'.join((gsod_path, site_group))
    util.get_or_create_group(h5file, site_path, "Site %s" % site['code'])

    value_table_name = variable
    values_path = '/'.join([site_path, value_table_name])

    try:
        value_table = h5file.getNode(values_path)
    except NoSuchNodeError:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            value_table = util.get_or_create_table(
                h5file, values_path, NCDCValue,
                "Values for site: %s, variable: %s" % (site['code'], variable))
            value_table.cols.date.createCSIndex()
            value_table.attrs.USAF = site['USAF']
            value_table.attrs.WBAN = site['WBAN']
            value_table.attrs.name = site['name']

    return value_table


def _init_h5(path=None, mode='w'):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    if not path:
        path = HDF5_FILE_PATH
    with tables.openFile(path, mode=mode, title="pyHIS data") as h5file:
        ncdc = h5file.createGroup('/', 'ncdc', 'NCDC Data')
        gsod = h5file.createGroup(ncdc, 'gsod', 'Global Summary of the Day')
        h5file.createGroup(gsod, 'values', 'Values')


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
