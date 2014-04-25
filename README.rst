ulmo
====

**clean, simple and fast access to public hydrology and climatology data**

-----------

.. image:: https://secure.travis-ci.org/ulmo-dev/ulmo.png?branch=master
        :target: https://travis-ci.org/ulmo-dev/ulmo


Features
--------

- retrieves and parses datasets from the web 
- returns simple python data structures that can be easily pulled into `more
  sophisticated tools`_ for analysis
- caches datasets locally and harvests updates as needed



Datasets
--------

Currently, ulmo supports the following datasets / services:

- Climate Prediction Center Weekly Drought Monitor
- CUAHSI WaterOneFlow
- National Climatic Data Center Climate Index Reference Sequential (CIRS)
- National Climatic Data Center Global Summary of the Day
- National Climatic Data Center Global Historical Climatology Network
- Texas Weather Connection's Daily Keetch-Byram Drought Index
- US Army Corps of Engineers Tulsa District Water Control
- United States Geological Survey National Water Information System 



Future
------

A list of future datasets is kept in on the `issue tracker`_. If there's a dataset
you'd like to see added, please open an issue about it.



Links
-----

* Documentation: http://ulmo.readthedocs.org
* Repository: https://github.com/twdb/ulmo


.. _more sophisticated tools: http://pandas.pydata.org
.. _issue tracker: https://github.com/twdb/ulmo/issues?labels=new+dataset&state=open 
