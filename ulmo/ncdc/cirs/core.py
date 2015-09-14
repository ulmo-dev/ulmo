"""
    ulmo.ncdc.cirs.core
    ~~~~~~~~~~~~~~~~~~~

    This module provides direct access to the `National Climatic Data Center`_
    `Climate Index Reference Sequential (CIRS)`_ drought dataset.

    .. _National Climatic Data Center: http://www.ncdc.noaa.gov
    .. _Climate Index Reference Sequential (CIRS): http://www1.ncdc.noaa.gov/pub/data/cirs/
"""
from builtins import str
from builtins import range
from past.builtins import basestring
import distutils
import os.path

import pandas

from ulmo import util


CIRS_DIR = util.get_ulmo_dir('ncdc/cirs')

NO_DATA_VALUES = {
    'cddc': '-9999.',
    'hddc': '-9999.',
    'pcpn': '-9.99',
    'pdsi': '-99.99',
    'phdi': '-99.99',
    'pmdi': '-99.99',
    'sp01': '-99.99',
    'sp02': '-99.99',
    'sp03': '-99.99',
    'sp06': '-99.99',
    'sp09': '-99.99',
    'sp12': '-99.99',
    'sp24': '-99.99',
    'tmpc': '-99.90',
    'zndx': '-99.99',

}


def get_data(elements=None, by_state=False, location_names='abbr', as_dataframe=False, use_file=None):
    """Retrieves data.

    Parameters
    ----------
    elements : ``None`, str or list
        The element(s) for which to get data for. If ``None`` (default), then
        all elements are used. An individual element is a string, but a list or
        tuple of them can be used to specify a set of elements.  Elements are:
          * 'cddc': Cooling Degree Days
          * 'hddc': Heating Degree Days
          * 'pcpn': Precipitation
          * 'pdsi': Palmer Drought Severity Index
          * 'phdi': Palmer Hydrological Drought Index
          * 'pmdi': Modified Palmer Drought Severity Index
          * 'sp01': 1-month Standardized Precipitation Index
          * 'sp02': 2-month Standardized Precipitation Index
          * 'sp03': 3-month Standardized Precipitation Index
          * 'sp06': 6-month Standardized Precipitation Index
          * 'sp09': 9-month Standardized Precipitation Index
          * 'sp12': 12-month Standardized Precipitation Index
          * 'sp24': 24-month Standardized Precipitation Index
          * 'tmpc': Temperature
          * 'zndx': ZNDX
    by_state : bool
        If False (default), divisional data will be retrieved. If True, then
        regional data will be retrieved.
    location_names : str or ``None``
        This parameter defines what (if any) type of names will be added to the
        values. If set to 'abbr' (default), then abbreviated location names
        will be used. If 'full', then full location names will be used. If set
        to None, then no location name will be added and the only identifier
        will be the location_codes (this is the most memory-conservative
        option).
    as_dataframe : bool
        If ``False`` (default), a list of values dicts is returned. If ``True``,
        a dict with element codes mapped to equivalent pandas.DataFrame objects
        will be returned. The pandas dataframe is used internally, so setting
        this to ``True`` is faster as it skips a somewhat expensive
        serialization step.
    use_file : ``None``, file-like object or str
        If ``None`` (default), then data will be automatically retrieved from
        the web. If a file-like object or a file path string, then the file will
        be used to read data from. This is intended to be used for reading in
        previously-downloaded versions of the dataset.


    Returns
    -------
    data : list or pandas.DataFrame
        A list of value dicts or a pandas.DataFrame containing data. See
        the ``as_dataframe`` parameter for more.
    """

    if isinstance(elements, basestring):
        elements = [elements]
    elif elements is None:
        elements = [
            'cddc',
            'hddc',
            'pcpn',
            'pdsi',
            'phdi',
            'pmdi',
            'sp01',
            'sp02',
            'sp03',
            'sp06',
            'sp09',
            'sp12',
            'sp24',
            'tmpc',
            'zndx',
        ]

    df = None

    for element in elements:
        element_file = _get_element_file(use_file, element, elements, by_state)

        element_df = _get_element_data(element, by_state, element_file, location_names)

        keys = ['location_code', 'year', 'month']
        for append_key in ['division', 'state', 'state_code']:
            if append_key in element_df.columns:
                keys.append(append_key)
        element_df.set_index(keys, inplace=True)

        if df is None:
            df = element_df
        else:
            df = df.join(element_df, how='outer')

    df = df.reset_index()
    df = _resolve_location_names(df, location_names, by_state)

    if as_dataframe:
        return df
    else:
        return list(df.T.to_dict().values())


def _get_element_data(element, by_state, use_file, location_names):
    if use_file:
        url = None
        path = None
    else:
        url = _get_url(element, by_state)
        filename = url.rsplit('/', 1)[-1]
        path = os.path.join(CIRS_DIR, filename)

    with util.open_file_for_url(url, path, use_file=use_file) as f:
        element_df = _parse_values(f, by_state, location_names, element)

    return element_df


def _get_element_file(use_file, element, elements, by_state):
    if isinstance(use_file, basestring):
        if os.path.basename(use_file) == '':
            if len(elements) > 1:
                assert ValueError(
                    "'use_file' must be a path to a directory if using "
                    "'use_file' with multiple elements")

            return use_file + _get_filename(element, by_state, os.path.dirname(use_file))

    return use_file


def _get_filename(element, by_state, dir_path):
    files = os.listdir(dir_path)
    return _most_recent(files, element, by_state)


def _get_url(element, by_state):
    ftp_dir = "ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/"
    files = util.dir_list(ftp_dir)
    most_recent = _most_recent(files, element, by_state)
    return ftp_dir + most_recent


def _most_recent(files, element, by_state):
    geographic_extent = 'st' if by_state else 'dv'
    match_str = 'climdiv-{element}{geographic_extent}'.format(
        element=element,
        geographic_extent=geographic_extent,
    )
    matches = [s for s in files if s.startswith(match_str)]
    return sorted(matches, key=_file_key)[0]


def _file_key(filename):
    version_str = filename.split('-')[2][1:]
    return distutils.version.StrictVersion(version_str)


def _parse_values(file_handle, by_state, location_names, element):
    if by_state:
        id_columns = [
            ('location_code', 0, 3, None),
            #('division', 3, 3, None), # ignored in state files
            #('element', 4, 6, None),  # element is redundant
            ('year', 6, 10, None),
        ]
    else:
        id_columns = [
            ('location_code', 0, 2, None),
            ('division', 2, 4, None),
            #('element', 4, 6, None),  # element is redundant
            ('year', 6, 10, None),
        ]

    year_col_end = id_columns[-1][2]

    month_columns = [
        (str(n), year_col_end - 6 + (7 * n), year_col_end + (7 * n), None)
        for n in range(1, 13)
    ]

    columns = id_columns + month_columns

    na_values = [NO_DATA_VALUES.get(element)]
    parsed = util.parse_fwf(file_handle, columns, na_values=na_values)

    month_columns = [id_column[0] for id_column in id_columns]
    melted = pandas.melt(parsed, id_vars=month_columns)\
        .rename(columns={'variable': 'month'})

    melted.month = melted.month.astype(int)

    # throw away NaNs
    melted = melted[melted['value'].notnull()]

    data = melted.rename(columns={
        'value': element,
    })

    return data


def _resolve_location_names(df, location_names, by_state):
    if location_names is None:
        return df
    elif location_names not in ('abbr', 'full'):
        raise ValueError("location_names should be set to either None, 'abbr' or 'full'")
    else:
        locations = _states_regions_dataframe()[location_names]
        with_locations = df.join(locations, on='location_code')

        if by_state:
            return with_locations.rename(columns={
                location_names: 'location',
            })
        else:
            return with_locations.rename(columns={
                location_names: 'state',
                'location_code': 'state_code',
            })


def _states_regions_dataframe():
    """returns a dataframe indexed by state/region code with columns for the
    name and abbrevitation (abbr) to use
    """
    STATES_REGIONS = {
        # code: (full name, abbrevation)
        1: ("Alabama", "AL"),
        2: ("Arizona", "AZ"),
        3: ("Arkansas", "AR"),
        4: ("California", "CA"),
        5: ("Colorado", "CO"),
        6: ("Connecticut", "CT"),
        7: ("Delaware", "DE"),
        8: ("Florida", "FL"),
        9: ("Georgia", "GA"),
        10: ("Idaho", "ID"),
        11: ("Illinois", "IL"),
        12: ("Indiana", "IN"),
        13: ("Iowa", "IA"),
        14: ("Kansas", "KS"),
        15: ("Kentucky", "KY"),
        16: ("Louisiana", "LA"),
        17: ("Maine", "ME"),
        18: ("Maryland", "MD"),
        19: ("Massachusetts", "MA"),
        20: ("Michigan", "MI"),
        21: ("Minnesota", "MN"),
        22: ("Mississippi", "MS"),
        23: ("Missouri", "MO"),
        24: ("Montana", "MT"),
        25: ("Nebraska", "NE"),
        26: ("Nevada", "NV"),
        27: ("New Hampshire", "NH"),
        28: ("New Jersey", "NJ"),
        29: ("New Mexico", "NM"),
        30: ("New York", "NY"),
        31: ("North Carolina", "NC"),
        32: ("North Dakota", "ND"),
        33: ("Ohio", "OH"),
        34: ("Oklahoma", "OK"),
        35: ("Oregon", "OR"),
        36: ("Pennsylvania", "PA"),
        37: ("Rhode Island", "RI"),
        38: ("South Carolina", "SC"),
        39: ("South Dakota", "SD"),
        40: ("Tennessee", "TN"),
        41: ("Texas", "TX"),
        42: ("Utah", "UT"),
        43: ("Vermont", "VT"),
        44: ("Virginia", "VA"),
        45: ("Washington", "WA"),
        46: ("West Virginia", "WV"),
        47: ("Wisconsin", "WI"),
        48: ("Wyoming", "WY"),
        101: ("Northeast Region", "ner"),
        102: ("East North Central Region", "encr"),
        103: ("Central Region", "cr"),
        104: ("Southeast Region", "ser"),
        105: ("West North Central Region", "wncr"),
        106: ("South Region", "sr"),
        107: ("Southwest Region", "swr"),
        108: ("Northwest Region", "nwr"),
        109: ("West Region", "wr"),
        110: ("National (contiguous 48 States)", "national"),

        # The following are the range of code values for the National Weather Service Regions, river basins, and agricultural regions.
        111: ("NWS: Great Plains", "nws:gp"),
        115: ("NWS: Southern Plains and Gulf Coast", "nws:spgc"),
        120: ("NWS: US Rockies and Westward", "nws:usrw"),
        121: ("NWS: Eastern Region", "nws:er"),
        122: ("NWS: Southern Region", "nws:sr"),
        123: ("NWS: Central Region", "nws:cr"),
        124: ("NWS: Western Region", "nws:wr"),
        201: ("NWS: Pacific Northwest Basin", "nws:pnwb"),
        202: ("NWS: California River Basin", "nws:crb"),
        203: ("NWS: Great Basin", "nws:gb"),
        204: ("NWS: Lower Colorado River Basin", "nws:lcrb"),
        205: ("NWS: Upper Colorado River Basin", "nws:urcb"),
        206: ("NWS: Rio Grande River Basin", "nws:rgrb"),
        207: ("NWS: Texas Gulf Coast River Basin", "nws:tgcrb"),
        208: ("NWS: Arkansas-White-Red Basin", "nws:awrb"),
        209: ("NWS: Lower Mississippi River Basin", "nws:lmrb"),
        210: ("NWS: Missouri River Basin", "nws:mrb"),
        211: ("NWS: Souris-Red-Rainy Basin", "nws:srrb"),
        212: ("NWS: Upper Mississippi River Basin", "nws:umrb"),
        213: ("NWS: Great Lakes Basin", "nws:glb"),
        214: ("NWS: Tennessee River Basin", "nws:trb"),
        215: ("NWS: Ohio River Basin", "nws:ohrb"),
        216: ("NWS: South Atlantic-Gulf Basin", "nws:sagb"),
        217: ("NWS: Mid-Atlantic Basin", "nws:mab"),
        218: ("NWS: New England Basin", "nws:neb"),
        220: ("NWS: Mississippi River Basin & Tributaties (N. of Memphis, TN",
              "nws:mrbt"),

        # below( codes are weighted by area)
        250: ("Area: Spring Wheat Belt", "area:swb"),
        255: ("Area: Primary Hard Red Winter Wheat Belt", "area:phrwwb"),
        256: ("Area: Winter Wheat Belt", "area:wwb"),
        260: ("Area: Primary Corn and Soybean Belt", "area:pcsb"),
        261: ("Area: Corn Belt", "area:cb"),
        262: ("Area: Soybean Belt", "area:sb"),
        265: ("Area: Cotton Belt", "area:cb"),

        # below( codes are weighted by productivity)
        350: ("Prod: Spring Wheat Belt", "prod:swb"),
        356: ("Prod: Winter Wheat Belt", "prod:wwb"),
        361: ("Prod: Corn Belt", "prod:cb"),
        362: ("Prod: Soybean Belt", "prod:sb"),
        365: ("Prod: Cotton Belt", "prod:cb"),

        # below( codes are for percent productivity in the Palmer Z Index categories)
        450: ("% Prod: Spring Wheat Belt", "%prod:swb"),
        456: ("% Prod: Winter Wheat Belt", "%prod:wwb"),
        461: ("% Prod: Corn Belt", "%prod:cb"),
        462: ("% Prod: Soybean Belt", "%prod:sb"),
        465: ("% Prod: Cotton Belt", "%prod:cb"),
    }
    return pandas.DataFrame(STATES_REGIONS).T.rename(columns={0: 'full', 1: 'abbr'})
