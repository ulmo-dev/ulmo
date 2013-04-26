

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
    pass


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
    pass


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


def update_site_list(sites=None, state_code=None, service=None, path=None):
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


    Returns
    -------
    None : ``None``
    """
    pass


def update_site_data(site_code, start=None, end=None, period=None, path=None):
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
