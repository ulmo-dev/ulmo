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
    last_modified = tables.StringCol(26)


def get_sites(path=None):
    """gets a dict of sites from an hdf5 file"""
    if not path:
        path = HDF5_FILE_PATH
    h5file = tables.openFile(path, mode='r')
    site_table = h5file.root.usgs.sites
    return_dict = dict([(row['code'], _row_to_dict(row, site_table)) for row in site_table.iterrows()])
    h5file.close()
    return return_dict


def get_site(site_code, path=None):
    """gets a site dict for a specific site_code from an hdf5 file"""
    if not path:
        path = HDF5_FILE_PATH
    # XXX: this is really dumb
    sites = get_sites(path)
    if site_code in sites:
        site = sites.get(site_code)
    else:
        sites = core.get_sites(sites=site_code)
        site = sites.get(site_code)
        if not site:
            raise LookupError("Could not find site %s" % site_code)
    return site


def get_site_data(site_code, agency_code=None, path=None):
    """gets the data for a given site"""
    if not path:
        path = HDF5_FILE_PATH
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


def init_h5(path=None, mode='w'):
    """creates an hdf5 file an initialized it with relevant tables, etc"""
    if not path:
        path = HDF5_FILE_PATH
    h5file = tables.openFile(path, mode=mode, title="pyHIS data")

    usgs = h5file.createGroup('/', 'usgs', 'USGS Data')
    sites = h5file.createTable(usgs, 'sites', USGSSite, "USGS Sites")
    sites.cols.code.createIndex()
    sites.cols.network.createIndex()

    h5file.createGroup(usgs, 'values', "USGS Values")

    h5file.close()


def update_site_list(sites=None, state_code=None, service=None, path=None):
    """update list of sites for a given state_code"""
    if not path:
        path = HDF5_FILE_PATH
    sites = core.get_sites(sites=sites, state_code=state_code, service=service)
    _update_site_table(sites, path)


def update_site_data(site_code, date_range=None, path=None):
    """updates data for a given site
    """
    if not path:
        path = HDF5_FILE_PATH
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
        update_values = d['values']
        # add last_modified date to the values we're updating
        for value in update_values:
            value.update({'last_modified': query_isodate})
        value_table = _get_value_table(h5file, site, variable)
        value_table.attrs.variable = variable
        _update_or_append_sortable(value_table, update_values, 'datetime')
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
    return _row_to_dict_with_names(row, names)


def _row_to_dict_with_names(row, names):
    """converts a row to a dict representation given the row and dested names;
    this is just a helper function for _row_to_dict
    """
    return_dict = {}
    for name, val in zip(names, row[:]):
        if not type(name) == tuple:
            return_dict[name] = val
        else:
            return_dict[name[0]] = _row_to_dict_with_names(val, name[1])
    return return_dict


def _update_or_append(table, update_values, where_filter):
    """updates table with dict representations of rows, appending new rows if
    need be; where_filter should uniquely identify a row within a table and will
    determine whether or not a row is updated or appended
    """
    value_row = table.row
    for i, update_value in enumerate(update_values):
        where_clause = where_filter % update_value
        # update matching rows (should only be one), or append index to append_indices
        updated = False
        for existing_row in table.where(where_clause):
            updated = True
            _update_row_with_dict(existing_row, update_value)
            existing_row.update()
            table.flush()
        if not updated:
            update_value['__flag_for_append'] = True
    for update_value in update_values:
        if '__flag_for_append' in update_value:
            del update_value['__flag_for_append']
            _update_row_with_dict(value_row, update_value)
            value_row.append()
    table.flush()


def _update_or_append_sortable(table, update_values, sortby):
    """updates table with dict representations of rows, appending new rows if
    need be; sortby should be a completly sortable column (with a CSIndex)
    """
    value_row = table.row
    update_values.sort(key=lambda v: v[sortby])
    table_iterator = table.itersorted(sortby)
    try:
        current_row = table_iterator.next()
    except StopIteration:
        current_row = None

    for i, update_value in enumerate(update_values):
        if not current_row or update_value[sortby] < current_row[sortby]:
            update_value['__flag_for_append'] = True

        elif current_row:
            # advance the table iterator until you are >= update_value
            while current_row and current_row[sortby] < update_value[sortby]:
                try:
                    current_row = table_iterator.next()
                except StopIteration:
                    current_row = None

            # if we match, then update
            if current_row and current_row[sortby] == update_value[sortby]:
                _update_row_with_dict(current_row, update_value)
                current_row.update()

            # else flag for append
            else:
                update_value['__flag_for_append'] = True

    for update_value in update_values:
        if '__flag_for_append' in update_value:
            del update_value['__flag_for_append']
            _update_row_with_dict(value_row, update_value)
            value_row.append()
    table.flush()


def _update_row_with_dict(row, dict):
    """sets the values of row to be the values found in dict"""
    for k, v in dict.iteritems():
        row.__setitem__(k, v)


def _update_site_table(sites, path):
    """updates a sites table with a given list of sites dicts
    """
    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    h5file = tables.openFile(path, mode="r+")
    site_table = h5file.root.usgs.sites
    site_values = [
        _flatten_nested_dict(site)
        for site in sites.itervalues()]
    where_filter = "(code == '%(code)s') & (agency == '%(agency)s')"
    _update_or_append(site_table, site_values, where_filter)
    h5file.close()


def _values_table_as_dict(table):
    variable = table.attrs.variable

    values = [_row_to_dict(value, table)
              for value in table.itersorted(table.cols.datetime)]
    values_dict = {
        'variable': variable,
        'values': values
    }

    return variable['code'] + ":" + variable['statistic']['code'], values_dict
