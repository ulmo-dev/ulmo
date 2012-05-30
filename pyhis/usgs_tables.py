"""
module that defines pytables cache
"""
import os
import tempfile

import tables

from pyhis import usgs_core

# default hdf5 file path
HDF5_FILE_PATH = os.path.join(tempfile.gettempdir(), "pyhis_usgs.h5")


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


def init_h5(path=HDF5_FILE_PATH):
    h5file = tables.openFile(path, mode="w", title="pyHIS USGS cache")
    h5file.createTable('/', 'sites', USGSSite, "USGS Sites")
    h5file.close()


def update_site_list(state_code, path=HDF5_FILE_PATH):
    """update list of sites for a given state_code"""
    sites = usgs_core.get_sites(state_code)

    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    h5file = tables.openFile(path, mode="r+")
    site_table = h5file.root.sites
    site_row = site_table.row
    for site in sites.itervalues():
        flattened = _flatten_dict(site)
        for k, v in flattened.iteritems():
            site_row[k] = v
        site_row.append()
    site_table.flush()


def _flatten_dict(d, prepend=''):
    """flattens a nested dict structure into structure suitable for inserting
    into a pytables table; assumes that no keys in the nested dict structure
    contain the character '/'
    """
    return_dict = {}

    for k, v in d.iteritems():
        if isinstance(v, dict):
            flattened = _flatten_dict(v, prepend=prepend + k + '/')
            return_dict.update(flattened)
        else:
            return_dict[prepend + k] = v

    return return_dict


if __name__ == '__main__':
    init_h5()
    update_site_list('RI')
