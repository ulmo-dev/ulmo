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
