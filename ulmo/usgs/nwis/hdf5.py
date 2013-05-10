import contextlib
import copy
import os
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas
import tables
from tables.scripts import ptrepack

from ulmo import util
from ulmo.usgs.nwis import core


# default hdf5 file path
DEFAULT_HDF5_FILE_PATH = util.get_default_h5file_path('usgs')

# define column sizes for strings stored in hdf5 tables
# note: this is currently not used as we simply read in and write out entire
# site dataframes to the store (not using tables type)
SITES_MIN_ITEMSIZE = {
    'agency': 20,
    'code': 20,
    'county': 30,
    'huc': 20,
    'name': 250,
    'network': 20,
    'site_type': 20,
    'state_code': 2,
    'srs': 20,
    'default_tz_abbreviation': 5,
    'default_tz_offset': 7,
    'dst_tz_abbreviation': 5,
    'dst_tz_offset': 7,
}

SITES_TABLE = 'sites'


def get_sites(path=None, complevel=None, complib=None):
    """Fetches previously-cached site information from an hdf5 file.

    Parameters
    ----------
    path : ``None`` or file path
        Path to the hdf5 file to be queried, if ``None`` then the default path
        will be used.
    complevel : ``None`` or int {0-9}
        Open hdf5 file with this level of compression. If ``None` (default),
        then a minimum compression level will be used if a compression library
        can be found. If set to 0 then no compression will be used regardless of
        what complib is.
    complib : ``None`` or str {'zlib', 'bzip2', 'lzo', 'blosc'}
        Open hdf5 file with this type of compression. If ``None`` (default) then
        the best available compression library available on your system will be
        selected. If complevel argument is set to 0 then no compression will be
        used.


    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
    """
    if path is None:
        path = DEFAULT_HDF5_FILE_PATH

    if not os.path.exists(path):
        return {}

    with _get_store(path, 'r') as store:
        if SITES_TABLE not in store:
            return {}

        sites_df = store[SITES_TABLE]
    sites_dict = _sites_df_to_dict(sites_df)
    return sites_dict


def get_site(site_code, path=None, complevel=None, complib=None):
    """Fetches previously-cached site information from an hdf5 file.

    Parameters
    ----------
    site_code : str
        The site code of the site you want to get information for.
    path : ``None`` or file path
        Path to the hdf5 file to be queried, if ``None`` then the default path
        will be used.
    complevel : ``None`` or int {0-9}
        Open hdf5 file with this level of compression. If ``None` (default),
        then a minimum compression level will be used if a compression library
        can be found. If set to 0 then no compression will be used regardless of
        what complib is.
    complib : ``None`` or str {'zlib', 'bzip2', 'lzo', 'blosc'}
        Open hdf5 file with this type of compression. If ``None`` (default) then
        the best available compression library available on your system will be
        selected. If complevel argument is set to 0 then no compression will be
        used.


    Returns
    -------
    site_dict : dict
        a python dict containing site information
    """
    if path is None:
        path = DEFAULT_HDF5_FILE_PATH

    # XXX: this could be more efficiently implemented by querying the sites
    # table with actual expressions
    sites = get_sites(path=path, complevel=complevel, complib=complib)
    try:
        return sites[site_code]
    except KeyError:
        raise LookupError("could not find site: %s" % site_code)


def get_site_data(site_code, agency_code=None, path=None, complevel=None,
        complib=None):
    """Fetches previously-cached site data from an hdf5 file.

    Parameters
    ----------
    site_code : str
        The site code of the site you want to get data for.
    agency_code : ``None`` or str
        The agency code to get data for. This will need to be set if a site code
        is in use by multiple agencies (this is rare).
    path : ``None`` or file path
        Path to the hdf5 file to be queried, if ``None`` then the default path
        will be used.
    complevel : ``None`` or int {0-9}
        Open hdf5 file with this level of compression. If ``None` (default),
        then a minimum compression level will be used if a compression library
        can be found. If set to 0 then no compression will be used regardless of
        what complib is.
    complib : ``None`` or str {'zlib', 'bzip2', 'lzo', 'blosc'}
        Open hdf5 file with this type of compression. If ``None`` (default) then
        the best available compression library available on your system will be
        selected. If complevel argument is set to 0 then no compression will be
        used.


    Returns
    -------
    data_dict : dict
        a python dict with parameter codes mapped to value dicts
    """
    if not path:
        path = DEFAULT_HDF5_FILE_PATH

    comp_kwargs = _compression_kwargs(complevel=complevel, complib=complib)

    with _get_store(path, 'r', **comp_kwargs) as store:
        site_group = store.get_node(site_code)
        if site_group is None:
            return {}

        site_data = dict([
            (variable_group._v_pathname.rsplit('/', 1)[-1],
            _variable_group_to_dict(store, variable_group))
            for variable_group in site_group
        ])
    return site_data


def repack(path):
    """repacks the hdf5 file at path to conserve space"""
    with tempfile.NamedTemporaryFile() as temp_f:
        temp_path = temp_f.name
        _ptrepack(path, temp_path)
        shutil.copyfile(temp_path, path)


def update_site_list(sites=None, state_code=None, service=None, path=None,
        input_file=None, complevel=None, complib=None):
    """Update cached site information.

    Parameters
    ----------
    sites : str, iterable of strings or ``None``
        The site to use or list of sites to use; lists will be joined by a ','.
    state_code : str or ``None``
        Two-letter state code used in stateCd parameter.
    site_type : str or ``None``
        Type of site used in siteType parameter.
    service : {``None``, 'instantaneous', 'iv', 'daily', 'dv'}
        The service to use, either "instantaneous", "daily", or ``None``
        (default).  If set to ``None``, then both services are used.  The
        abbreviations "iv" and "dv" can be used for "instantaneous" and "daily",
        respectively.
    path : ``None`` or file path
        Path to the hdf5 file to be updated, if ``None`` then the default path
        will be used.
    input_file: ``None``, file path or file object
        If ``None`` (default), then the NWIS web services will be queried, but
        if a file is passed then this file will be used instead of requesting
        data from the NWIS web services.
    complevel : ``None`` or int {0-9}
        Open hdf5 file with this level of compression. If ``None` (default),
        then a minimum compression level will be used if a compression library
        can be found. If set to 0 then no compression will be used regardless of
        what complib is.
    complib : ``None`` or str {'zlib', 'bzip2', 'lzo', 'blosc'}
        Open hdf5 file with this type of compression. If ``None`` (default) then
        the best available compression library available on your system will be
        selected. If complevel argument is set to 0 then no compression will be
        used.


    Returns
    -------
    None : ``None``
    """
    if not path:
        path = DEFAULT_HDF5_FILE_PATH
    new_sites = core.get_sites(sites=sites, state_code=state_code, service=service,
            input_file=input_file)

    if len(new_sites) == 0:
        return

    comp_kwargs = _compression_kwargs(complevel=complevel, complib=complib)
    with _get_store(path, 'a', **comp_kwargs) as store:
        _update_stored_sites(store, new_sites)

    return None


def update_site_data(site_code, start=None, end=None, period=None, path=None,
        input_file=None, complevel=None, complib=None):
    """Update cached site data.

    Parameters
    ----------
    site_code : str
        The site code of the site you want to query data for.
    start : ``None`` or datetime (see :ref:`dates-and-times`)
        Start of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    end : ``None`` or datetime (see :ref:`dates-and-times`)
        End of a date range for a query. This parameter is mutually exclusive
        with period (you cannot use both).
    period : {``None``, str, datetime.timedelta}
        Period of time to use for requesting data. This will be passed along as
        the period parameter. This can either be 'all' to signal that you'd like
        the entire period of record, or string in ISO 8601 period format (e.g.
        'P1Y2M21D' for a period of one year, two months and 21 days) or it can
        be a datetime.timedelta object representing the period of time. This
        parameter is mutually exclusive with start/end dates.
    path : ``None`` or file path
        Path to the hdf5 file to be updated, if ``None`` then the default path
        will be used.
    input_file: ``None``, file path or file object
        If ``None`` (default), then the NWIS web services will be queried, but
        if a file is passed then this file will be used instead of requesting
        data from the NWIS web services.


    Returns
    -------
    None : ``None``
    """
    if not path:
        path = DEFAULT_HDF5_FILE_PATH

    if input_file is None and start is None and end is None and period is None:
        prior_last_refresh = _get_last_refresh(site_code, path)
        if prior_last_refresh is None:
            period = 'all'
        else:
            start = prior_last_refresh

    new_site_data = core.get_site_data(site_code, start=start, end=end,
            period=period, input_file=input_file)

    comp_kwargs = _compression_kwargs(complevel=complevel, complib=complib)
    with _get_store(path, 'a', **comp_kwargs) as store:
        for variable_code, data_dict in new_site_data.iteritems():
            variable_group_path = site_code + '/' + variable_code

            site_dict = data_dict.pop('site')
            _update_stored_sites(store, {site_dict['code']: site_dict})

            values_path = variable_group_path + '/values'
            new_values = _values_dicts_to_df(data_dict.pop('values', {}))
            last_refresh = data_dict.get('last_refresh')
            if last_refresh is None:
                last_refresh = np.nan
            new_values['last_checked'] = last_refresh
            if values_path in store:
                compare_cols = ['value', 'qualifiers']
                original_values = store[values_path]
                original_align, new_align = original_values.align(new_values)
                new_nulls = (new_align[compare_cols] == np.nan).sum(axis=1).astype(bool)
                modified_mask = ~new_nulls & ((
                    original_align[compare_cols] == new_align[compare_cols]) \
                    .sum(axis=1) < len(compare_cols))

                combined = new_values.combine_first(original_values)
                combined['last_modified'][modified_mask] = last_refresh
                new_values = combined
            else:
                new_values['last_modified'] = last_refresh

            store[values_path] = new_values

            variable_group = store.get_node(variable_group_path)
            for key, value in data_dict.iteritems():
                setattr(variable_group._v_attrs, key, value)

        site_group = store.get_node(site_code)
        site_group._v_attrs.last_refresh = last_refresh


def _compression_kwargs(complevel=None, complib=None):
    """returns a dict containing the compression settings to use"""
    if complib is None and complevel is None:
        possible_compressions = ('blosc', 'zlib')
        for possible_compression in possible_compressions:
            try:
                try_kwargs = dict(complevel=1, complib=possible_compression)
                tables.Filters(**try_kwargs)
                return try_kwargs
            except tables.FiltersWarning:
                pass

        complevel = 0

    elif complib is not None and complevel is None:
        complevel = 1

    return dict(complevel=complevel, complib=complib)


@contextlib.contextmanager
def _filter_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pandas.io.pytables.PerformanceWarning)
        warnings.simplefilter("ignore", tables.NaturalNameWarning)
        yield


def _get_last_refresh(site_code, path, complevel=None, complib=None):
    comp_kwargs = _compression_kwargs(complevel=complevel, complib=complib)
    try:
        with _get_store(path, 'r', **comp_kwargs) as store:
            site_group = store.get_node(site_code)
            if site_group is None:
                return None
            last_refresh = getattr(site_group._v_attrs, 'last_refresh')
            if pandas.isnull(last_refresh):
                last_refresh = None
            return last_refresh
    except IOError:
        return None


@contextlib.contextmanager
def _get_store(*args, **kwargs):
    with pandas.io.pytables.get_store(*args, **kwargs) as store:
        with _filter_warnings():
            yield store


def _nans_to_none(df):
    return df.astype(object).where(pandas.notnull(df), None)


def _nest_dataframe_dicts(unnested_df, nested_column, keys):
    df = unnested_df.copy()
    df = _nans_to_none(df)

    def _nest_func(row):
        return dict(zip(keys, row))

    nested_values = map(_nest_func, df[keys].values)
    df[nested_column] = nested_values

    for key in keys:
        del df[key]

    return df


def _ptrepack(src, dst):
    """run ptrepack to repack from src to dst"""
    with _sysargs_hacks():
        sys.argv = ['', src, dst]
        with _filter_warnings():
            ptrepack.main()


def _sites_df_to_dict(df):
    df = _nest_dataframe_dicts(df, 'location', ['latitude', 'longitude', 'srs'])
    for tz_type in ['default_tz', 'dst_tz']:
        tz_keys = ['abbreviation', 'offset']
        rename_dict = dict([
            (tz_type + '_' + key, key) for key in tz_keys])
        df = df.rename(columns=rename_dict)
        df = _nest_dataframe_dicts(df, tz_type,
                tz_keys)
    df = _nest_dataframe_dicts(df, 'timezone_info',
            ['uses_dst', 'default_tz', 'dst_tz'])

    return df.T.to_dict()


def _sites_dict_to_df(sites_dict):
    df = pandas.DataFrame(sites_dict).T.copy()
    df = _unnest_dataframe_dicts(df, 'location', ['latitude', 'longitude', 'srs'])
    df = _unnest_dataframe_dicts(df, 'timezone_info',
            ['uses_dst', 'default_tz', 'dst_tz'])
    for tz_type in ['default_tz', 'dst_tz']:
        tz_keys = ['abbreviation', 'offset']
        df = _unnest_dataframe_dicts(df, tz_type,
                tz_keys)
        rename_dict = dict([
            (key, tz_type + '_' + key) for key in tz_keys])
        df = df.rename(columns=rename_dict)

    return df


@contextlib.contextmanager
def _sysargs_hacks():
    """temporarily replace sys.argv without leaking global state"""
    orig_sysargv = copy.copy(sys.argv)
    yield
    sys.argv = orig_sysargv


def _unnest_dataframe_dicts(df, nested_column, keys):
    def _unnest_func(nested_dict):
        if pandas.isnull(nested_dict):
            return [np.nan] * len(keys)
        return [nested_dict.get(key, np.nan) for key in keys]

    unzipped_values = zip(*df[nested_column].map(_unnest_func).values)

    for key, values in zip(keys, unzipped_values):
        df[key] = values

    del df[nested_column]
    return df


def _values_dicts_to_df(values_dicts):
    df = pandas.DataFrame(values_dicts, dtype=object)
    if len(df) == 0:
        df = pandas.DataFrame(columns=['datetime', 'value', 'qualifiers', 'last_checked',
            'last_modified'])
    else:
        df = df.set_index(pandas.DatetimeIndex(df['datetime']))
    return df


def _values_df_to_dicts(values_df):
    df = values_df.where(pandas.notnull(values_df), None)
    dicts = df.T.to_dict().values()
    dicts.sort(key=lambda d: d['datetime'])
    return dicts


def _variable_group_to_dict(store, variable_group):
    _v_attrs = variable_group._v_attrs
    variable_dict = dict([
        (key, getattr(_v_attrs, key))
        for key in _v_attrs._f_list()
    ])
    values_path = variable_group._v_pathname + '/values'
    values_df = store[values_path]
    variable_dict['values'] = _values_df_to_dicts(values_df)

    return variable_dict


def _update_stored_sites(store, sites_dict):
    new_sites_df = _sites_dict_to_df(sites_dict)
    if SITES_TABLE in store:
        sites_df = store[SITES_TABLE]
        new_sites_df = new_sites_df.combine_first(sites_df)

    store[SITES_TABLE] = new_sites_df
