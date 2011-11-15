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

from . import his_central

import quantities as pq
from . import quantities as phq
from . import util

#: mapping of variable codes to quantities they represent
unit_quantities = {
    '48': phq.ftH2O,
    '52': phq.mH2O,
    '96': pq.degC,
    '137': pq.dimensionless,
    '199': phq.mgl,
    '269': phq.mScm,
    '306': phq.ppt,
    }
