"""
module that defines pytables cache
"""
import os
import tempfile

import tables

from pyhis import usgs_core

# default hdf5 file path
HDF5_FILE_PATH = os.path.join(tempfile.gettempdir(), "pyhis.h5")


class USGSSite(tables.IsDescription):
    agency = tables.StringCol(20)
    code = tables.StringCol(20)
    county = tables.StringCol(30)
    huc = tables.StringCol(20)
    name = tables.StringCol(250)
    network = tables.StringCol(20)
    site_type = tables.StringCol(20)
    state_code = tables.StringCol(2)

    class location(tables.IsDescription):
        srs = tables.StringCol(20)
        latitude = tables.Float32Col()
        longitude = tables.Float32Col()

    class timezone_info(tables.IsDescription):
        uses_dst = tables.BoolCol()

        class default_tz(tables.IsDescription):
            abbreviation = tables.StringCol(5)
            offset = tables.StringCol(7)

        class dst_tz(tables.IsDescription):
            abbreviation = tables.StringCol(5)
            offset = tables.StringCol(7)


class USGSVariable(tables.IsDescription):
    code = tables.StringCol(5)
    description = tables.StringCol(250)
    name = tables.StringCol(250)
    network = tables.StringCol(20)
    no_data_value = tables.StringCol(20)
    type = tables.StringCol(20)
    unit = tables.StringCol(20)
    vocabulary = tables.StringCol(20)

    class statistic(tables.IsDescription):
        code = tables.StringCol(5)
        name = tables.StringCol(5)


class USGSValue(tables.IsDescription):
    datetime = tables.Time64Col()
    qualifiers = tables.StringCol(20)
    value = tables.StringCol(20)

    class site(tables.IsDescription):
        code = tables.StringCol(5)
        network = tables.StringCol(5)

    class variable(tables.IsDescription):
        code = tables.StringCol(5)
        network = tables.StringCol(5)

        class statistic(tables.IsDescription):
            code = tables.StringCol(5)
            name = tables.StringCol(5)


def get_sites(path=HDF5_FILE_PATH):
    """gets a dict of sites from an hdf5 file"""
    h5file = tables.openFile(path, mode='r')
    site_table = h5file.root.usgs.sites
    names = site_table.description._v_nestedNames
    return_dict = dict([(row['code'], _row_to_dict(row, names)) for row in site_table.iterrows()])
    h5file.close()
    return return_dict


def get_site(site_code, path=HDF5_FILE_PATH):
    """gets a site dict for a specific site_code from an hdf5 file"""
    # XXX: this is really dumb
    return get_sites().get(site_code)
def init_h5(path=HDF5_FILE_PATH, mode='w'):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    h5file = tables.openFile(path, mode=mode, title="pyHIS data")

    usgs = h5file.createGroup('/', 'usgs', 'USGS Data')
    sites = h5file.createTable(usgs, 'sites', USGSSite, "USGS Sites")
    sites.cols.code.createIndex()
    sites.cols.network.createIndex()
    h5file.createTable(usgs, 'variables', USGSVariable, "USGS Variables")
    h5file.createTable(usgs, 'values', USGSValue, "USGS Values")
    h5file.close()


def update_site_list(state_code, path=HDF5_FILE_PATH):
    """update list of sites for a given state_code"""
    sites = usgs_core.get_sites(state_code)

    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    h5file = tables.openFile(path, mode="r+")
    site_table = h5file.root.usgs.sites
    site_row = site_table.row
    for site in sites.itervalues():
        flattened = _flatten_nested_dict(site)
        for k, v in flattened.iteritems():
            site_row[k] = v
        site_row.append()
    site_table.flush()
    h5file.close()


def update_site_data(site_code, path=HDF5_FILE_PATH):
    """updates data for a given site
    """
    #site_data = usgs_core.get_site_data(site_code, date_range='all')
    site_data = usgs_core.get_site_data(site_code)

    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    h5file = tables.openFile(path, mode="r+")
    value_table = h5file.root.usgs.values
    value_row = value_table.row

    for d in site_data.itervalues():
        variable = d['variable']

        value_variable = {
            'variable/code': variable['code'],
            'variable/network': variable['network'],
        }
        if 'statistic' in variable:
            value_variable['variable/statistic/code'] = variable['statistic']['code']
            value_variable['variable/statistic/name'] = variable['statistic']['name']

        for value in d['values']:
            value_flat = _flatten_nested_dict(value)
            value_flat.update(value_variable)
            _update_row_with_dict(value_row, value_flat)
            value_row.append()
    value_table.flush()
    h5file.close()


def _flatten_nested_dict(d, prepend=''):
    """flattens a nested dict structure into structure suitable for inserting
    into a pytables table; assumes that no keys in the nested dict structure
    contain the character '/'
    """
    return_dict = {}

    for k, v in d.iteritems():
        if isinstance(v, dict):
            flattened = _flatten_nested_dict(v, prepend=prepend + k + '/')
            return_dict.update(flattened)
        else:
            return_dict[prepend + k] = v

    return return_dict


def _row_to_dict(row, names):
    """converts a row to a dict representation, given the row and nested names
    (i.e. table.description._v_nestedNames)
    """
    return_dict = {}
    for name, val in zip(names, row[:]):
        if not type(name) == tuple:
            return_dict[name] = val
        else:
            return_dict[name[0]] = _row_to_dict(val, name[1])
    return return_dict


def _update_row_with_dict(row, dict):
    """sets the values of row to be the values found in dict"""
    for k, v in dict.iteritems():
        row.__setitem__(k, v)


if __name__ == '__main__':
    #init_h5()
    #update_site_list('RI')
    #sites = get_sites()
    import pdb; pdb.set_trace()
    update_site_data('01116300')
    site = get_site_data('01116300')
    pass
