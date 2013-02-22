"""
    ulmo.usace.rivergages.core
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `United States Army
    Corps of Engineers`_ `Rivergages`_ web site.

    .. _United States Army Corps of Engineers: http://www.usace.army.mil/
    .. _Rivergages: http://rivergages.mvr.usace.army.mil/WaterControl/new/layout.cfm
"""
import os.path

from bs4 import BeautifulSoup

from ulmo import util

USACE_RIVERGAGES_DIR = os.path.join(util.get_ulmo_dir(), 'usace/rivergages/')


def get_stations():
    url = 'http://rivergages.mvr.usace.army.mil/WaterControl/datamining2.cfm'
    path = os.path.join(USACE_RIVERGAGES_DIR, 'datamining_field_list.cfm')

    with util.open_file_for_url(url, path) as f:
        soup = BeautifulSoup(f)

        options = soup.find('select', id='fld_station').find_all('option')

        stations = dict([
            (option.attrs.get('value'), option.text.strip())
            for option in options
            if option.attrs.get('value') != ''
        ])

    return stations
