"""
module that defines pytables cache
"""
from __future__ import absolute_import

import datetime
import isodate
import warnings

import tables
from tables.exceptions import NoSuchNodeError

from ulmo import util
from ulmo.usgs import core

# default hdf5 file path
HDF5_FILE_PATH = util.get_default_h5file_path()


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


class USGSValue(tables.IsDescription):
    datetime = tables.StringCol(26)
    qualifiers = tables.StringCol(20)
    value = tables.StringCol(20)
    last_modified = tables.StringCol(26)


def get_sites(path=None):
    """gets a dict of sites from an hdf5 file"""
    if not path:
        path = HDF5_FILE_PATH
    with util.open_h5file(path, 'r') as h5file:
        #site_table = h5file.root.usgs.sites
        #return_dict = dict([(row['code'], _row_to_dict(row, site_table)) for row in site_table.iterrows()])
        sites_table = _get_sites_table(h5file)
        if not sites_table:
            return {}

        return dict([
            (row['code'], _row_to_dict(row, sites_table))
            for row in sites_table.iterrows()])
    #return return_dict


def get_site(site_code, path=None):
    """gets a site dict for a specific site_code from an hdf5 file"""
    if not path:
        path = HDF5_FILE_PATH
    # XXX: this is really dumb
    sites = get_sites(path)
    if site_code in sites:
        site = sites.get(site_code)
    else:
        # TODO: this might be a bad idea - it requires writing to the file and
        # we might want to guarantee that gets don't require a write lock
        update_site_list(sites=site_code, path=path)
        sites = get_sites(path)
        site = sites.get(site_code)
        if not site:
            raise LookupError("Could not find site %s" % site_code)
    return site


def get_site_data(site_code, agency_code=None, path=None):
    """gets the data for a given site"""
    if not path:
        path = HDF5_FILE_PATH
    # walk the agency groups looking for site code
    with util.open_h5file(path, mode='r') as h5file:
        sites_table = _get_sites_table(h5file)
        if sites_table is None:
            return {}

        if agency_code:
            where_clause = "(code == '%s') & (agency == '%s')" % (site_code, agency_code)
        else:
            where_clause = '(code == "%s")' % site_code

        agency = None
        for count, row in enumerate(sites_table.where(where_clause)):
            agency = row['agency']

        if not agency:
            return {}

        if count >= 1 and not agency_code:
            raise ('more than one site found, limit your query using an agency code')

        site_path = '/usgs/values/%s/%s' % (agency, site_code)
        try:
            site_group = h5file.getNode(site_path)
        except NoSuchNodeError:
            raise Exception("no site found for code: %s" % site_code)

        values_dict = dict([
            _values_table_as_dict(table)
            for table in site_group._f_walkNodes('Table')])
        return values_dict


def update_site_list(sites=None, state_code=None, service=None, path=None):
    """update list of sites for a given state_code"""
    if not path:
        path = HDF5_FILE_PATH
    sites = core.get_sites(sites=sites, state_code=state_code, service=service)
    _update_sites_table(sites.itervalues(), path)


def update_site_data(site_code, date_range=None, path=None):
    """updates data for a given site
    """
    if not path:
        path = HDF5_FILE_PATH
    update_site_list(sites=site_code, path=path)
    site = get_site(site_code, path=path)

    query_isodate = isodate.datetime_isoformat(datetime.datetime.now())

    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    with util.open_h5file(path, mode="r+") as h5file:
        if not date_range:
            last_site_refresh = _last_refresh(site, h5file)
            if last_site_refresh:
                date_range = datetime.datetime.now() - isodate.parse_datetime(last_site_refresh)
            else:
                date_range = 'all'

        site_data = core.get_site_data(site_code, date_range=date_range)

        for d in site_data.itervalues():
            variable = d['variable']
            update_values = d['values']
            # add last_modified date to the values we're updating
            for value in update_values:
                value.update({'last_modified': query_isodate})
            value_table = _get_value_table(h5file, site, variable)
            value_table.attrs.variable = variable
            value_table.attrs.last_refresh = query_isodate
            _update_or_append_sortable(value_table, update_values, 'datetime')
            value_table.flush()


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


def _get_agency_group(h5file, agency_name):
    values_group = _get_values_group(h5file)
    if values_group is None:
        return None

    try:
        agency_group = h5file.getNode(values_group, agency_name)
    except NoSuchNodeError:
        if _is_writable(h5file):
            agency_group = h5file.createGroup(
                    values_group, agency_name, "%s sites" % agency_name)
        else:
            return None

    return agency_group


def _get_site_group(h5file, site):
    agency_name = site['agency']
    site_code = site['code']

    agency_group = _get_agency_group(h5file, agency_name)
    if agency_group is None:
        return None

    try:
        site_group = h5file.getNode(agency_group, site_code)
    except NoSuchNodeError:
        if _is_writable(h5file):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                site_group = h5file.createGroup(agency_group, site_code, "Site %s" % site_code)
        else:
            return None
    return site_group


def _get_sites_table(h5file):
    usgs_group = _get_usgs_group(h5file)
    if usgs_group is None:
        return None

    sites_table_name = 'sites'
    try:
        sites_table = h5file.getNode(usgs_group, sites_table_name)
    except NoSuchNodeError:
        if _is_writable(h5file):
            sites_table = h5file.createTable(usgs_group, sites_table_name, USGSSite, 'USGS Sites')
            sites_table.cols.code.createIndex()
            sites_table.cols.network.createIndex()
        else:
            return None

    return sites_table


def _get_usgs_group(h5file):
    try:
        usgs_group = h5file.getNode('/usgs')
    except NoSuchNodeError:
        if _is_writable(h5file):
            usgs_group = h5file.createGroup('/', 'usgs', 'USGS Data')
        else:
            return None

    return usgs_group


def _get_value_table(h5file, site, variable):
    """returns a value table for a given open h5file (writable), site and
    variable. If the value table already exists, it is returned. If it doesn't,
    it will be created.
    """
    site_group = _get_site_group(h5file, site)
    if site_group is None:
        return None

    if 'statistic' in variable:
        value_table_name = variable['code'] + ":" + variable['statistic']['code']
    else:
        value_table_name = variable['code']

    try:
        value_table = h5file.getNode(site_group, value_table_name)
    except NoSuchNodeError:
        if _is_writable(h5file):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                value_table = h5file.createTable(site_group, value_table_name, USGSValue, "Values for site: %s, variable: %s:%s" % (site['code'],
                    variable['code'], variable['statistic']['code']))
                value_table.cols.datetime.createCSIndex()
        else:
            return None

    return value_table


def _get_values_group(h5file):
    usgs_group = _get_usgs_group(h5file)
    if usgs_group is None:
        return None

    values_group_name = 'values'
    try:
        values_group = h5file.getNode(usgs_group, values_group_name)
    except NoSuchNodeError:
        if _is_writable(h5file):
            values_group = h5file.createGroup(
                usgs_group, values_group_name, 'USGS Values')
        else:
            return None

    return values_group


def _is_writable(h5file):
    """returns True if h5file is writable, false otherwise"""
    if h5file.mode in ['r', 'rb']:
        return False
    else:
        return True


def _last_refresh(site, h5file):
    """returns last refresh for a given site"""
    site_group = _get_site_group(h5file, site)
    last_refresheds = [
        getattr(child.attrs, 'last_refreshed', None)
        for child in site_group._f_iterNodes()]

    # XXX: this won't work in python3
    if not len(last_refresheds):
        return None
    else:
        return min(last_refresheds)


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


def _update_sites_table(sites, path):
    """updates a sites table with a given list of sites dicts
    """
    # XXX: use some sort of mutex or file lock to guard against concurrent
    # processes writing to the file
    with util.open_h5file(path, mode="r+") as h5file:
        sites_table = _get_sites_table(h5file)
        site_values = [
            _flatten_nested_dict(site)
            for site in sites]
        where_filter = "(code == '%(code)s') & (agency == '%(agency)s')"
        _update_or_append(sites_table, site_values, where_filter)


def _values_table_as_dict(table):
    variable = table.attrs.variable

    values = [_row_to_dict(value, table)
              for value in table.itersorted(table.cols.datetime)]
    values_dict = {
        'variable': variable,
        'values': values
    }

    return variable['code'] + ":" + variable['statistic']['code'], values_dict
