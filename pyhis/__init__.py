"""
    PyHIS
    ~~~~~

    PyHIS is a python library for querying CUAHSI*-HIS** web
    services. It helps you get water data from unwieldy sources.

    * CUAHSI is the Consortium of Universities for the
    Advancement of Hydrologic Science, Inc.
    ** HIS stands for Hydrlogic Information System
"""
from __future__ import absolute_import

from .core import *

import quantities as pq
from . import quantities as sq

#: mapping of variable codes to quantities they represent
unit_quantities = {
    '48': sq.ftH2O,
    '52': sq.mH2O,
    '96': pq.degC,
    '137': pq.dimensionless,
    '199': sq.mgl,
    '269': sq.mScm,
    '306': sq.ppt,
    }
