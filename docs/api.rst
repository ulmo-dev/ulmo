.. _api:


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



National Climatic Data Center Global Historical Climate Network Daily
=====================================================================
.. automodule:: ulmo.ncdc.ghcn_daily
   :members: get_data, get_stations


National Climatic Data Center Global Summary of the Day
=======================================================
.. automodule:: ulmo.ncdc.gsod
   :members: get_data, get_stations


USGS National Water Information System
======================================
.. automodule:: ulmo.usgs.nwis
   :members: get_sites, get_site_data

.. automodule:: ulmo.usgs.nwis.hdf5
   :members:


US Army Corps of Engineers - Tulsa District Water Control
=========================================================
.. automodule:: ulmo.usace.swtwc
   :members: get_stations, get_station_data


.. _dates-and-times:

note on dates and times
-----------------------

Dates and times can provided a few different ways, depending on what is
convenient. They can either be a string representation or as instances of date
and datetime objects from python's datetime standard library module.  For
strings, the ISO 8061 format ('YYYY-mm-dd HH:MM:SS' or some abbreviated version)
is accepted, as well dates in 'mm/dd/YYYY' format.
