.. _api:



California Department of Water Resources Historical Data
========================================================
.. automodule:: ulmo.cdec.historical
   :members: get_stations, get_sensors, get_station_sensors, get_data


Climate Prediction Center Weekly Drought
========================================
.. automodule:: ulmo.cpc.drought
   :members: get_data


CUAHSI WaterOneFlow
===================
.. automodule:: ulmo.cuahsi.his_central
   :members: get_services

.. automodule:: ulmo.cuahsi.wof
   :members: get_sites, get_site_info, get_values, get_variable_info


Lower Colorado River Authority (LCRA) Hydromet Data
===================================================
.. automodule:: ulmo.lcra.hydromet
   :members: get_sites_by_type, get_site_data, get_all_sites, get_current_data


Lower Colorado River Authority (LCRA) Water Quality Data
========================================================
.. automodule:: ulmo.lcra.waterquality
   :members: get_sites, get_historical_data, get_recent_data, get_site_info


NASA ORNL Daymet weather data services
========================================================
.. automodule:: ulmo.nasa.daymet
   :members: get_variables, get_daymet_singlepixel
   

National Climatic Data Center Climate Index Reference Sequential (CIRS)
=======================================================================
.. automodule:: ulmo.ncdc.cirs
   :members: get_data


National Climatic Data Center Global Historical Climate Network Daily
=====================================================================
.. automodule:: ulmo.ncdc.ghcn_daily
   :members: get_data, get_stations


National Climatic Data Center Global Summary of the Day
=======================================================
.. automodule:: ulmo.ncdc.gsod
   :members: get_data, get_stations


Texas Weather Connection Daily Keetch-Byram Drought Index (KBDI)
================================================================
.. automodule:: ulmo.twc.kbdi
   :members: get_data


US Army Corps of Engineers - Tulsa District Water Control
=========================================================
.. automodule:: ulmo.usace.swtwc
   :members: get_stations, get_station_data


USGS National Water Information System
======================================
.. automodule:: ulmo.usgs.nwis
   :members: get_sites, get_site_data

.. automodule:: ulmo.usgs.nwis.hdf5
   :members:


USGS Emergency Data Distribution Network services
=================================================
.. automodule:: ulmo.usgs.eddn
   :members: get_data, decode


USGS Earth Resources Observation Systems (EROS) services
========================================================
.. automodule:: ulmo.usgs.eros
   :members: get_available_datasets, get_themes, get_attribute_list, get_available_formats, get_raster, get_raster_availability


USGS National Elevation Dataset (NED) services
========================================================
.. automodule:: ulmo.usgs.ned
   :members: get_available_layers, get_raster, get_raster_availability


.. _dates-and-times:

note on dates and times
-----------------------

Dates and times can provided a few different ways, depending on what is
convenient. They can either be a string representation or as instances of date
and datetime objects from python's datetime standard library module.  For
strings, the ISO 8061 format ('YYYY-mm-dd HH:MM:SS' or some abbreviated version)
is accepted, as well dates in 'mm/dd/YYYY' format.
