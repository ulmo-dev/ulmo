"""
    `USGS National Water Information System`_ web services


    .. _USGS National Water Information System: http://waterdata.usgs.gov/nwis
"""
from __future__ import absolute_import

from . import core

from .core import (get_sites, get_site_data)

from ulmo import util

try:
    from . import hdf5

except ImportError:
    hdf5 = util.module_with_dependency_errors([
        'get_site',
        'get_sites',
        'get_site_data',
        'update_site_list',
        'update_site_data',
    ])

pytables = util.module_with_deprecation_warnings([
        hdf5.get_site,
        hdf5.get_sites,
        hdf5.get_site_data,
        hdf5.update_site_list,
        hdf5.update_site_data,
    ],
    "the nwis.pytables module has moved to nwis.hdf5 - nwis.pytables "
    "is deprecated and will be removed in a future ulmo release."
)
