"""
    ulmo
    ~~~~

    an open source library for clean, simple and fast access to public hydrology and climatology data
"""
from __future__ import absolute_import
import datetime

from . import cuahsi
from . import ncdc
from . import usgs
from . import util

import numpy as np
import pandas as pd
import baker


def _isfinite(testval):
    '''
    Private utility for '_printiso' function.
    Just returns a blank in place of 'nan' so that other applications see just
    a missing value.
    '''
    if np.isfinite(testval):
        return str(testval)
    else:
        return ' '


def _printiso(tsd):
    '''
    Prints the series
    '''
    try:
        # Header
        print 'Datetime,', ', '.join(str(i) for i in tsd.columns)

        # Data
        for i in range(len(tsd)):
            print tsd.index[i], ', ', ', '.join(
                _isfinite(j) for j in tsd.values[i])
    except IOError:
        return


@baker.command(default=True)
def get_data(*param_specs, **kwds):
    try:
        date_range = kwds.pop('date_range')
        date_range = datetime.datetime.strptime(date_range, '%Y-%m-%d')
    except KeyError:
        date_range = None
    if kwds:
        raise ValueError(
            '"date_range" is the only keyword allowed, you gave {0}'.format(
                kwds.keys()))

    for index in param_specs:
        orgabbr, station, param = index.split(',')
        if orgabbr == 'NWISDV':
            nts = usgs.nwis.core.get_site_data(station, service='daily',
                    date_range=date_range)
            param_interval = ':00003'
        if orgabbr == 'NWISIV':
            nts = usgs.nwis.core.get_site_data(station, service='instantaneous',
                    date_range=date_range)
            param_interval = ':00011'
        dates = [i['datetime'] for i in nts[param + param_interval]['values']]
        values = [float(i['value']) for i in nts[param + param_interval]['values']]
        nts = pd.DataFrame(pd.Series(values, index=dates),
                columns=['{0}_{1}_{2}'.format(orgabbr, station, param)])
        try:
            result = result.join(nts, how='outer')
        except NameError:
            result = nts
    _printiso(result)


def main():
    baker.run()
