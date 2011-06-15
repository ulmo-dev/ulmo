"""
    pyhis.quantities
    ~~~~~~~~~~~~~~~~

    This module contains a few custom quantities that are used
    primarily for unit conversion.
"""
from __future__ import absolute_import
import quantities as pq


#: Unit of concentration - milligrams per liter
mgl = pq.UnitQuantity('Concentration',
                      pq.CompoundUnit("mg/L"),
                      symbol='mg/L')

#: Unit of specific conductivity - milliSiemens per centimeter
mScm = pq.UnitQuantity('Specific Conductivity in MilliSiemens per Centimeter',
                       pq.CompoundUnit("1e-3*S/cm"),
                       symbol='mS/cm')

#: Unit of turbidity - nephelometric turbidity units
ntu = pq.UnitQuantity('Turbidity',
                      pq.dimensionless,
                      symbol='NTU')

#: Unit of salinity - practical salinity units
psu = pq.UnitQuantity('Salinity',
                      pq.dimensionless,
                      symbol='PSU')
ppt = psu

# nickname for dimensionless
dl = pq.dimensionless

#unit of speed
mps = pq.UnitQuantity('Speed', pq.m / pq.second, symbol='m/s')

#: Unit of specific conductivity - microSiemens per centimeter
uScm = pq.UnitQuantity('Specific Conductivity',
                       pq.CompoundUnit("1e-6*S/cm"),
                       symbol='uS/cm')

#: Units of Depth/Water Surface Elevation - meters/ft of water
mH2O = pq.UnitQuantity('meters of water', pq.m * pq.conventional_water,
                       symbol='mH2O')
ftH2O = pq.ftH2O  # since ftH20 already exists in pq
#: Pressure in dbar
dbar = pq.UnitQuantity('decibar', pq.CompoundUnit('0.1*bar'), symbol='dbar')
