import os.path

import pandas

from ulmo import util


CIRS_DIR = util.get_ulmo_dir('ncdc/cirs')


def get_data(index, by_state=False, as_dataframe=False, use_file=None):
    url = _get_url(index, by_state)
    filename = url.rsplit('/', 1)[-1]
    path = os.path.join(CIRS_DIR, filename)

    with util.open_file_for_url(url, path, use_file=use_file) as f:
        data = _parse_values(f, by_state)

    if as_dataframe:
        return data
    else:
        return data.T.to_dict().values()


def _get_url(index, by_state):
    return "ftp://ftp.ncdc.noaa.gov/pub/data/cirs/drd964x.%s%s.txt" % (
        index, 'st' if by_state else '')


def _parse_values(file_handle, by_state):
    id_columns = [
        ('state_code', 0, 2, None),
        ('division', 2, 4, None),
        #('element', 4, 6, None),  # element is redundant
        ('year', 6, 10, None),
    ]

    month_columns = [
        (str(n), 3 + (7 * n), 10 + (7 * n), None)
        for n in range(1, 13)
    ]

    columns = id_columns + month_columns

    data = util.parse_fwf(file_handle, columns, na_values=["-99.99"])

    month_columns = [id_column[0] for id_column in id_columns]
    melted = pandas.melt(data, id_vars=month_columns)\
        .rename(columns={'variable': 'month'})

    melted.month = melted.month.astype(int)

    states = _states_regions_dataframe()\
        .rename(columns={'abbr': 'state'})['state']
    return melted.join(states, on='state_code')


def _states_regions_dataframe():
    """returns a dataframe indexed by state/region code with columns for the
    name and abbrevitation (abbr) to use
    """
    STATES_REGIONS = {
        # (code, full name, abbrevation)
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
        101: ("Northeast Region", "northeast"),
        102: ("East North Central Region", "enc"),
        103: ("Central Region", "central"),
        104: ("Southeast Region", "southeast"),
        105: ("West North Central Region", "wnc"),
        106: ("South Region", "south"),
        107: ("Southwest Region", "southwest"),
        108: ("Northwest Region", "northwest"),
        109: ("West Region", "west"),
        110: ("National (contiguous 48 States)", "national"),
    }
    return pandas.DataFrame(STATES_REGIONS).T.rename(columns={0: 'name', 1: 'abbr'})
