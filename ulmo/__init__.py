"""
    ulmo
    ~~~~

    an open source library for clean, simple and fast access to public hydrology and climatology data
"""
from __future__ import absolute_import

from .core import *

from . import his_central
from . import ncdc
from . import usgs
from . import wof

#import quantities as pq
#from . import quantities as phq
from . import util

#: mapping of variable codes to quantities they represent
#unit_quantities = {
    #'48': phq.ftH2O,
    #'52': phq.mH2O,
    #'96': pq.degC,
    #'137': pq.dimensionless,
    #'199': phq.mgl,
    #'269': phq.mScm,
    #'306': phq.ppt,
    #}
