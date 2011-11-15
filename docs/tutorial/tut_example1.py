"""
Example script that returns a list of USGS gages within the Austin area whose discharge is below
20th percentile.
"""

#Initialize pyhis

import pyhis

# Connect to the USGS NWIS Unit values and Daily values data services.
# The daily values service will be used to calculate historical percentiles
# and the unit values service provides 15 mn data

nwisdv = pyhis.Service('http://river.sdsc.edu/wateroneflow/NWIS/DailyValues.asmx?WSDL')
nwisuv = pyhis.Service('http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL')

# get si
