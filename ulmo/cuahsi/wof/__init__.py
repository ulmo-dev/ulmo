"""
    CUAHSI WaterOneFlow
    ~~~~~~~~~~~~~~~~~~~
    `CUAHSI WaterOneFlow`_ web data access services

    .. _CUAHSI WaterOneFlow: http://his.cuahsi.org/wofws.html
"""
from __future__ import absolute_import

from . import core

from .core import (get_sites, get_site_info, get_values, get_variable_info)
