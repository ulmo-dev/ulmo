import os

import numpy as np
import pandas

from ulmo import util
from ulmo.usgs.nwis import core


# default hdf5 file path
DEFAULT_HDF5_FILE_PATH = util.get_default_h5file_path()

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


def get_sites(path=None):
    """Fetches previously-cached site information from an hdf5 file.

    Parameters
    ----------
    path : ``None`` or file path
        Path to the hdf5 file to be queried, if ``None`` then the default path
        will be used.


    Returns
    -------
    sites_dict : dict
        a python dict with site codes mapped to site information
    """
    if path is None:
        path = DEFAULT_HDF5_FILE_PATH

    if not os.path.exists(path):
        return {}

    with pandas.io.pytables.get_store(path, 'r') as store:
        if SITES_TABLE not in store:
            return {}

        sites_df = store[SITES_TABLE]
    sites_dict = _sites_dataframe_to_dict(sites_df)
    return sites_dict


def get_site(site_code, path=None):
    """Fetches previously-cached site information from an hdf5 file.

    Parameters
    ----------
    site_code : str
        The site code of the site you want to get information for.
    path : ``None`` or file path
        Path to the hdf5 file to be queried, if ``None`` then the default path
        will be used.


    Returns
    -------
    site_dict : dict
        a python dict containing site information
    """
    if path is None:
        path = DEFAULT_HDF5_FILE_PATH

    # XXX: this could be more efficiently implemented by querying the sites
    # table with actual expressions
    sites = get_sites(path=path)
    try:
        return sites[site_code]
    except KeyError:
        raise LookupError("could not find site: %s" % site_code)


def get_site_data(site_code, agency_code=None, path=None):
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


    Returns
    -------
    data_dict : dict
        a python dict with parameter codes mapped to value dicts
    """
    pass


def update_site_list(sites=None, state_code=None, service=None, path=None,
        input_file=None):
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

    new_sites_df = _sites_dict_to_dataframe(new_sites)

    with pandas.io.pytables.get_store(path, 'a') as store:
        if SITES_TABLE in store:
            sites_df = store[SITES_TABLE]
            new_sites_df = new_sites_df.combine_first(sites_df)

        store[SITES_TABLE] = new_sites_df

    return None


def update_site_data(site_code, start=None, end=None, period=None, path=None,
        input_path=None):
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


    Returns
    -------
    None : ``None``
    """
    pass


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


def _sites_dataframe_to_dict(df):
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


def _sites_dict_to_dataframe(sites_dict):
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
