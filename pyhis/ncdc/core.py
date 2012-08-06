import datetime
import os

import requests

from pyhis import util

NCDC_GSOD_DIR = os.path.join(util._get_pyhis_dir(), 'ncdc_gsod')
NCDC_GSOD_START_YEAR = 1929


def download_gsod_files(historical=False, start_year=None, end_year=None):
    """downloads Global Summary of Day data from ncdc and saves files in data directory

    Parameters
    ----------
    start_year : year to start downloads. default to current year
    end_year : year to end downloads. default to current year.
    historical : retrieves all available data. i.e start_year=1928, end_year = current year

    default retrieves current year. NCDC GSOD data is updated daily
    """
    _init_temp_dir()
    if historical:
        start_year = NCDC_GSOD_START_YEAR
        end_year = datetime.datetime.now().year

    if not end_year:
        end_year = datetime.datetime.now().year

    if not start_year:
        start_year = datetime.datetime.now().year

    base_url = 'http://www1.ncdc.noaa.gov/pub/data/gsod/'
    CHUNK = 64 * 1024
    for year in range(start_year, end_year + 1):
        url = base_url + '/' + str(year) + '/' + 'gsod_' + str(year) + '.tar'
        filename = os.path.join(NCDC_GSOD_DIR, url.split('/')[-1])
        print 'retrieving ncdc gsod tar data file for {0}'.format(year)
        r = requests.get(url)
        download = r.raw
        with open(filename, 'wb') as f:
            # https://gist.github.com/1311816
            while True:
                chunk = download.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

        print 'file saved at {0}'.format(filename)


def _init_temp_dir():
    if not os.path.exists(NCDC_GSOD_DIR):
        os.mkdir(NCDC_GSOD_DIR)
