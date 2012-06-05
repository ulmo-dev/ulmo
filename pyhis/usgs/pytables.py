"""
module that defines pytables cache
"""
from __future__ import absolute_import

import datetime
import isodate
import os
import tempfile
import warnings

import tables
from tables.exceptions import NoSuchNodeError

from pyhis.usgs import core

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
    last_refresh = tables.StringCol(26)

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


class USGSValue(tables.IsDescription):
    datetime = tables.StringCol(26)
    qualifiers = tables.StringCol(20)
    value = tables.StringCol(20)


def get_sites(path=HDF5_FILE_PATH):
    """gets a dict of sites from an hdf5 file"""
    h5file = tables.openFile(path, mode='r')
    site_table = h5file.root.usgs.sites
    return_dict = dict([(row['code'], _row_to_dict(row, site_table)) for row in site_table.iterrows()])
    h5file.close()
    return return_dict


def get_site(site_code, path=HDF5_FILE_PATH):
    """gets a site dict for a specific site_code from an hdf5 file"""
    # XXX: this is really dumb
    return get_sites().get(site_code)


def get_site_data(site_code, agency_code=None, path=HDF5_FILE_PATH):
    """gets the data for a given site"""
    # walk the agency groups looking for site code
    h5file = tables.openFile(path, mode='r')
    site_table = h5file.root.usgs.sites
    if agency_code:
        where_clause = "(code == '%s') & (agency == '%s')" % (site_code, agency_code)
    else:
        where_clause = '(code == "%s")' % site_code

    agency = None
    for count, row in enumerate(site_table.where(where_clause)):
        agency = row['agency']

    if not agency:
        h5file.close()
        return {}
    if count >= 1 and not agency_code:
        raise ('more than one site found, limit your query using an agency code')

    site_path = '/usgs/values/%s/%s' % (agency, site_code)
    try:
        site_group = h5file.getNode(site_path)
    except NoSuchNodeError:
        raise "no site found for code: %s" % site_code

    values_dict = dict([
        _values_table_as_dict(table)
        for table in site_group._f_walkNodes('Table')])
    h5file.close()
    return values_dict


def init_h5(path=HDF5_FILE_PATH, mode='w'):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    h5file = tables.openFile(path, mode=mode, title="pyHIS data")

    usgs = h5file.createGroup('/', 'usgs', 'USGS Data')
    sites = h5file.createTable(usgs, 'sites', USGSSite, "USGS Sites")
    sites.cols.code.createIndex()
    sites.cols.network.createIndex()

    h5file.createGroup(usgs, 'values', "USGS Values")

    h5file.close()


def update_site_list(state_code, service=None, path=HDF5_FILE_PATH):
    """update list of sites for a given state_code"""
    sites = core.get_sites(state_code, service=service)

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


def update_site_data(site_code, date_range=None, path=HDF5_FILE_PATH):
    """updates data for a given site
    """
    site = get_site(site_code)

    if not date_range:
        if site['last_refresh']:
            date_range = datetime.datetime.now() - isodate.parse_datetime(site['last_refresh'])
        else:
            date_range = 'all'

    query_isodate = isodate.datetime_isoformat(datetime.datetime.now())
    site_data = core.get_site_data(site_code, date_range=date_range)

    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    h5file = tables.openFile(path, mode="r+")
    sites_table = h5file.root.usgs.sites

    for d in site_data.itervalues():
        variable = d['variable']
        value_table = _get_value_table(h5file, site, variable)
        value_table.attrs.variable = variable
        value_row = value_table.row

        update_values = d['values']
        append_indices = []

        for i, update_value in enumerate(update_values):
            updated = False
            where_clause = '(datetime == "%s")' % update_value['datetime']

            # update matching rows (should only be one), or append index to append_indices
            for existing_row in value_table.where(where_clause):
                _update_row_with_dict(existing_row, update_value)
                updated = True

            # note: you can't use break/else pattern above due to the way
            # updates are implemented (http://www.pytables.org/trac-bck/ticket/140)
            if not updated:
                append_indices.append(i)

        for i in append_indices:
            append_value = update_values[i]
            _update_row_with_dict(value_row, append_value)
            value_row.append()
        value_table.flush()

    for site_row in sites_table.where('(code == "%s")' % site['code']):
        site_row['last_refresh'] = query_isodate
        site_row.update()
        sites_table.flush()

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


def _get_value_table(h5file, site, variable):
    """returns a value table for a given open h5file (writable), site and
    variable. If the value table already exists, it is returned. If it doesn't,
    it will be created.
    """
    agency_group = site['agency']
    agency_path = '/usgs/values/%s' % agency_group

    try:
        h5file.getNode(agency_path)
    except NoSuchNodeError:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            h5file.createGroup('/usgs/values', agency_group, "%s sites" % site['agency'])

    site_group = site['code']
    site_path = '%s/%s' % (agency_path, site_group)

    try:
        h5file.getNode(site_path)
    except NoSuchNodeError:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            h5file.createGroup(agency_path, site_group, "Site %s" % site['code'])

    if 'statistic' in variable:
        value_table_name = variable['code'] + ":" + variable['statistic']['code']
    else:
        value_table_name = variable['code']

    try:
        values_path = '/'.join([site_path, value_table_name])
        value_table = h5file.getNode(values_path)
    except NoSuchNodeError:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            value_table = h5file.createTable(site_path, value_table_name, USGSValue, "Values for site: %s, variable: %s:%s" % (site['code'],
                variable['code'], variable['statistic']['code']))
            value_table.cols.datetime.createCSIndex()

    return value_table


def _row_to_dict(row, table):
    """converts a row to a dict representation, given the row and table
    """
    names = table.description._v_nestedNames
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


def _values_table_as_dict(table):
    variable = table.attrs.variable

    values = [_row_to_dict(value, table)
              for value in table.itersorted(table.cols.datetime)]
    values_dict = {
        'variable': variable,
        'values': values
    }

    return variable['code'] + ":" + variable['statistic']['code'], values_dict
