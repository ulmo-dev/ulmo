"""
    LCRA Water Quality Data
    ~~~~~~~~~~~~~~~~~~~~~~~
    Access to water quality data in the Colorado River Basin (Texas)
    provided by the `Water Quality`_ web site and web service from
    the `Lower Colorado River Authority`_.

    .. _Lower Colorado River Authority: http://www.lcra.org
    .. _Water Quality: http://waterquality.lcra.org/
"""
from .core import get_sites, get_historical_data, get_recent_data, get_site_info
