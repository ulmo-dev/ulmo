.. _api:


ulmo Readers
============

ulmo readers / api's.


.. _dates-and-times:

note on dates and times
-----------------------

Dates and times can provided a few different ways, depending on what is
convenient. They can either be a string representation or as instances of date
and datetime objects from python's datetime standard library module.  For
strings, the ISO 8061 format ('YYYY-mm-dd HH:MM:SS' or some abbreviated version)
is accepted, as well dates in 'mm/dd/YYYY' format.


California Department of Water Resources Historical Data
========================================================
.. automodule:: ulmo.cdec.historical
   :members: get_stations, get_sensors, get_station_sensors, get_data


Climate Prediction Center (CPC) Weekly Drought
==============================================
.. automodule:: ulmo.cpc.drought
   :members: get_data


CUAHSI Hydrologic Information System (HIS)
==========================================

CUAHSI HIS Central
------------------
.. automodule:: ulmo.cuahsi.his_central
   :members: get_services


CUAHSI WaterOneFlow
-------------------
.. automodule:: ulmo.cuahsi.wof
   :members: get_sites, get_site_info, get_values, get_variable_info


Lower Colorado River Authority (LCRA)
=====================================

LCRA Hydromet Data
------------------
.. automodule:: ulmo.lcra.hydromet
   :members: get_sites_by_type, get_site_data, get_all_sites, get_current_data


LCRA Water Quality Data
-----------------------
.. automodule:: ulmo.lcra.waterquality
   :members: get_sites, get_historical_data, get_recent_data, get_site_info


NASA ORNL Daymet weather data services
======================================
.. automodule:: ulmo.nasa.daymet
   :members: get_variables, get_daymet_singlepixel
   

National Climatic Data Center (NCDC)
====================================

NCDC Climate Index Reference Sequential (CIRS)
-----------------------------------------------
.. automodule:: ulmo.ncdc.cirs
   :members: get_data


NCDC Global Historical Climate Network (GHCN) Daily
---------------------------------------------------
.. automodule:: ulmo.ncdc.ghcn_daily
   :members: get_data, get_stations


NCDC Global Summary of the Day (GSoD)
-------------------------------------
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


USGS National Water Information System (NWIS)
=============================================
.. automodule:: ulmo.usgs.nwis
   :members: get_sites, get_site_data

.. automodule:: ulmo.usgs.nwis.hdf5
   :members:


USGS Emergency Data Distribution Network (EDDN) services
========================================================
.. automodule:: ulmo.usgs.eddn
   :members: get_data, decode


USGS National Elevation Dataset (NED) services
========================================================
.. automodule:: ulmo.usgs.ned
   :members: get_available_layers, get_raster, get_raster_availability
