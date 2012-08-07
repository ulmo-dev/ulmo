import os
import tempfile

import tables


# default hdf5 file path
HDF5_FILE_PATH = os.path.join(tempfile.gettempdir(), "pyhis.h5")


class NCDCValue(tables.IsDescription):
    date = tables.StringCol(8)
    flag = tables.StringCol(1)
    value = tables.StringCol(20)
    last_modified = tables.StringCol(26)


def init_h5(path=None, mode='w'):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    if not path:
        path = HDF5_FILE_PATH
    h5file = tables.openFile(path, mode=mode, title="pyHIS data")

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
