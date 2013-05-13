"""
    ulmo.twc.kbdi.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides direct access to `Texas Weather Connection`_ `Daily
    Keetch-Byram Drought Index (KBDI)`_ dataset.

    .. _Texas Weather Connection: http://twc.tamu.edu/
    .. _Daily Keetch-Byram Drought Index (KBDI): http://twc.tamu.edu/drought/kbdi
"""

import datetime
import os

import numpy as np
import pandas

from ulmo import util

# directory where drought data will be stashed
TWC_KBDI_DIR = os.path.join(util.get_ulmo_dir(), 'twc/kbdi')


def get_data(county=None, start=None, end=None, as_dataframe=False):
    """Retreives data.


    Parameters
    ----------
    county : ``None`` or str
        If specified, results will be limited to the county corresponding to the
        given 5-character Texas county fips code i.e. 48???.
    start : ``None`` or date (see :ref:`dates-and-times`)
        Results will be limited to those after the given date. Default is the
        start of the current calendar year.
    end : ``None`` or date (see :ref:`dates-and-times`)
        If specified, results will be limited to data before this date. Default is
        the current date.
    as_dataframe: bool
        If ``False`` (default), a dict with a nested set of dicts will be
        returned with data indexed by 5-character Texas county fips code. If ``True``
        then a pandas.DataFrame object will be returned.  The pandas dataframe
        is used internally, so setting this to ``True`` is a little bit faster
        as it skips a serialization step.


    Returns
    -------
    data : dict or pandas.Dataframe
        A dict or pandas.DataFrame representing the data. See the
        ``as_dataframe`` parameter for more.
    """
    if end is None:
        end_date = datetime.date.today()
    else:
        end_date = util.convert_date(end)
    if start is None:
        start_date = datetime.date(end_date.year, 1, 1)
    else:
        start_date = util.convert_date(start)

    data = None
    FIPS = _fips()
    for date in _daterange(start_date, end_date):
        url = _get_data_url(date)
        with _open_data_file(url) as data_file:
            day_data = _parse_data_file(data_file)

        day_data['date'] = pandas.Period(date, freq='D')
        day_data['fips'] = day_data['county'].map(lambda county: FIPS[county])
        day_data = day_data.set_index('date')

        if county:
            day_data = day_data[day_data['fips'] == county]

        if data is None:
            data = day_data
        else:
            data = data.append(day_data)

    if as_dataframe:
        return data
    else:
        return _as_data_dict(data)


def _as_data_dict(dataframe):
    county_dict = {}
    for county in dataframe['fips'].unique():
        county_dataframe = dataframe[dataframe['fips'] == county]
        county_data = county_dataframe.T.drop(['fips'])
        values = [
            _value_dict(date, value)
            for date, value in county_data.iteritems()
        ]
        county_dict[county] = values

    return county_dict


def _daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def _fips():
        # fips codes from http://www.census.gov/geo/www/ansi/national.txt
        # with names adjusted to match twc kbdi: DEWITT --> DE WITT
    return {
        'ANDERSON': '48001',
        'ANDREWS': '48003',
        'ANGELINA': '48005',
        'ARANSAS': '48007',
        'ARCHER': '48009',
        'ARMSTRONG': '48011',
        'ATASCOSA': '48013',
        'AUSTIN': '48015',
        'BAILEY': '48017',
        'BANDERA': '48019',
        'BASTROP': '48021',
        'BAYLOR': '48023',
        'BEE': '48025',
        'BELL': '48027',
        'BEXAR': '48029',
        'BLANCO': '48031',
        'BORDEN': '48033',
        'BOSQUE': '48035',
        'BOWIE': '48037',
        'BRAZORIA': '48039',
        'BRAZOS': '48041',
        'BREWSTER': '48043',
        'BRISCOE': '48045',
        'BROOKS': '48047',
        'BROWN': '48049',
        'BURLESON': '48051',
        'BURNET': '48053',
        'CALDWELL': '48055',
        'CALHOUN': '48057',
        'CALLAHAN': '48059',
        'CAMERON': '48061',
        'CAMP': '48063',
        'CARSON': '48065',
        'CASS': '48067',
        'CASTRO': '48069',
        'CHAMBERS': '48071',
        'CHEROKEE': '48073',
        'CHILDRESS': '48075',
        'CLAY': '48077',
        'COCHRAN': '48079',
        'COKE': '48081',
        'COLEMAN': '48083',
        'COLLIN': '48085',
        'COLLINGSWORTH': '48087',
        'COLORADO': '48089',
        'COMAL': '48091',
        'COMANCHE': '48093',
        'CONCHO': '48095',
        'COOKE': '48097',
        'CORYELL': '48099',
        'COTTLE': '48101',
        'CRANE': '48103',
        'CROCKETT': '48105',
        'CROSBY': '48107',
        'CULBERSON': '48109',
        'DALLAM': '48111',
        'DALLAS': '48113',
        'DAWSON': '48115',
        'DE WITT': '48123',
        'DEAF SMITH': '48117',
        'DELTA': '48119',
        'DENTON': '48121',
        'DEWITT': '48123',
        'DICKENS': '48125',
        'DIMMIT': '48127',
        'DONLEY': '48129',
        'DUVAL': '48131',
        'EASTLAND': '48133',
        'ECTOR': '48135',
        'EDWARDS': '48137',
        'EL PASO': '48141',
        'ELLIS': '48139',
        'ERATH': '48143',
        'FALLS': '48145',
        'FANNIN': '48147',
        'FAYETTE': '48149',
        'FISHER': '48151',
        'FLOYD': '48153',
        'FOARD': '48155',
        'FORT BEND': '48157',
        'FRANKLIN': '48159',
        'FREESTONE': '48161',
        'FRIO': '48163',
        'GAINES': '48165',
        'GALVESTON': '48167',
        'GARZA': '48169',
        'GILLESPIE': '48171',
        'GLASSCOCK': '48173',
        'GOLIAD': '48175',
        'GONZALES': '48177',
        'GRAY': '48179',
        'GRAYSON': '48181',
        'GREGG': '48183',
        'GRIMES': '48185',
        'GUADALUPE': '48187',
        'HALE': '48189',
        'HALL': '48191',
        'HAMILTON': '48193',
        'HANSFORD': '48195',
        'HARDEMAN': '48197',
        'HARDIN': '48199',
        'HARRIS': '48201',
        'HARRISON': '48203',
        'HARTLEY': '48205',
        'HASKELL': '48207',
        'HAYS': '48209',
        'HEMPHILL': '48211',
        'HENDERSON': '48213',
        'HIDALGO': '48215',
        'HILL': '48217',
        'HOCKLEY': '48219',
        'HOOD': '48221',
        'HOPKINS': '48223',
        'HOUSTON': '48225',
        'HOWARD': '48227',
        'HUDSPETH': '48229',
        'HUNT': '48231',
        'HUTCHINSON': '48233',
        'IRION': '48235',
        'JACK': '48237',
        'JACKSON': '48239',
        'JASPER': '48241',
        'JEFF DAVIS': '48243',
        'JEFFERSON': '48245',
        'JIM HOGG': '48247',
        'JIM WELLS': '48249',
        'JOHNSON': '48251',
        'JONES': '48253',
        'KARNES': '48255',
        'KAUFMAN': '48257',
        'KENDALL': '48259',
        'KENEDY': '48261',
        'KENT': '48263',
        'KERR': '48265',
        'KIMBLE': '48267',
        'KING': '48269',
        'KINNEY': '48271',
        'KLEBERG': '48273',
        'KNOX': '48275',
        'LA SALLE': '48283',
        'LAMAR': '48277',
        'LAMB': '48279',
        'LAMPASAS': '48281',
        'LAVACA': '48285',
        'LEE': '48287',
        'LEON': '48289',
        'LIBERTY': '48291',
        'LIMESTONE': '48293',
        'LIPSCOMB': '48295',
        'LIVE OAK': '48297',
        'LLANO': '48299',
        'LOVING': '48301',
        'LUBBOCK': '48303',
        'LYNN': '48305',
        'MADISON': '48313',
        'MARION': '48315',
        'MARTIN': '48317',
        'MASON': '48319',
        'MATAGORDA': '48321',
        'MAVERICK': '48323',
        'MCCULLOCH': '48307',
        'MCLENNAN': '48309',
        'MCMULLEN': '48311',
        'MEDINA': '48325',
        'MENARD': '48327',
        'MIDLAND': '48329',
        'MILAM': '48331',
        'MILLS': '48333',
        'MITCHELL': '48335',
        'MONTAGUE': '48337',
        'MONTGOMERY': '48339',
        'MOORE': '48341',
        'MORRIS': '48343',
        'MOTLEY': '48345',
        'NACOGDOCHES': '48347',
        'NAVARRO': '48349',
        'NEWTON': '48351',
        'NOLAN': '48353',
        'NUECES': '48355',
        'OCHILTREE': '48357',
        'OLDHAM': '48359',
        'ORANGE': '48361',
        'PALO PINTO': '48363',
        'PANOLA': '48365',
        'PARKER': '48367',
        'PARMER': '48369',
        'PECOS': '48371',
        'POLK': '48373',
        'POTTER': '48375',
        'PRESIDIO': '48377',
        'RAINS': '48379',
        'RANDALL': '48381',
        'REAGAN': '48383',
        'REAL': '48385',
        'RED RIVER': '48387',
        'REEVES': '48389',
        'REFUGIO': '48391',
        'ROBERTS': '48393',
        'ROBERTSON': '48395',
        'ROCKWALL': '48397',
        'RUNNELS': '48399',
        'RUSK': '48401',
        'SABINE': '48403',
        'SAN AUGUSTINE': '48405',
        'SAN JACINTO': '48407',
        'SAN PATRICIO': '48409',
        'SAN SABA': '48411',
        'SCHLEICHER': '48413',
        'SCURRY': '48415',
        'SHACKELFORD': '48417',
        'SHELBY': '48419',
        'SHERMAN': '48421',
        'SMITH': '48423',
        'SOMERVELL': '48425',
        'STARR': '48427',
        'STEPHENS': '48429',
        'STERLING': '48431',
        'STONEWALL': '48433',
        'SUTTON': '48435',
        'SWISHER': '48437',
        'TARRANT': '48439',
        'TAYLOR': '48441',
        'TERRELL': '48443',
        'TERRY': '48445',
        'THROCKMORTON': '48447',
        'TITUS': '48449',
        'TOM GREEN': '48451',
        'TRAVIS': '48453',
        'TRINITY': '48455',
        'TYLER': '48457',
        'UPSHUR': '48459',
        'UPTON': '48461',
        'UVALDE': '48463',
        'VAL VERDE': '48465',
        'VAN ZANDT': '48467',
        'VICTORIA': '48469',
        'WALKER': '48471',
        'WALLER': '48473',
        'WARD': '48475',
        'WASHINGTON': '48477',
        'WEBB': '48479',
        'WHARTON': '48481',
        'WHEELER': '48483',
        'WICHITA': '48485',
        'WILBARGER': '48487',
        'WILLACY': '48489',
        'WILLIAMSON': '48491',
        'WILSON': '48493',
        'WINKLER': '48495',
        'WISE': '48497',
        'WOOD': '48499',
        'YOAKUM': '48501',
        'YOUNG': '48503',
        'ZAPATA': '48505',
        'ZAVALA': '48507'
    }


def _get_data_url(date):
    return 'http://twc.tamu.edu/weather_images/summ/summ%s.txt' % date.strftime('%Y%m%d')


def _parse_data_file(data_file):
    """
    example:
        COUNTY                        KBDI_AVG   KBDI_MAX    KBDI_MIN
                ----------------------------------------------------------------
                ANDERSON                         262       485        47
                ANDREWS                          485       614       357
                ...
    """

    dtype = [
        ('county', '|S15'),
        ('kbdi_avg', 'i4'),
        ('kbdi_max', 'i4'),
        ('kbdi_min', 'i4'),
    ]

    data_array = np.genfromtxt(
        data_file, delimiter=[31, 11, 11, 11], dtype=dtype, skip_header=2,
        skip_footer=1, autostrip=True)
    dataframe = pandas.DataFrame(data_array)
    return dataframe


def _open_data_file(url):
    """returns an open file handle for a data file; downloading if necessary or otherwise using a previously downloaded file"""
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(TWC_KBDI_DIR, file_name)
    return util.open_file_for_url(url, file_path, check_modified=True)


def _value_dict(date, value):
    value_dict = value.to_dict()
    value_dict['date'] = str(date)
    return value_dict
