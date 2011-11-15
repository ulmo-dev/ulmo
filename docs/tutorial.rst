.. index::
   single: tutorial, PyHIS
   single: PyHIS tutorial


************
PyHIS Basics
************

Introduction
============

This tutorial demonstrates how to retrieve data from the the CUAHSI-HIS system using PyHIS. It will
cover the basics of data access, available convinience functions and some simple scripts using the toolkit.

This tutorial requires PyHIS to be installed on your computer (http://pypi.python.org/pypi/pyhis).

Screenshots and examples in this tutorial are shown using the IPython (http://ipython.org/) interactive python
prompt for convinience but IPython is not required to use PyHIS. A Python code editor or IDE is recommended for
writing scripts or viewing code. This tutorial follows the convention below. A basic familiarity with Python is
useful but the examples have been chosen for readibility and a non python user should be able to follow the tutorial.

Code Snippet to be run in IPython or Python prompt::

  a = 5
  b = 9
  print a + b

  # Output:
  # In [1]: a = 5
  # In [2]: b = 9
  # In [3]: print a + b
  # 14

The line starting with a ``#`` are comment lines. The section following ``# Output:`` demonstrates the expected output of the code snippet.
You can follow along by cutting and pasting the each code snippet into the IPython prompt.

Initiating PyHIS
================

To start off lets import pyhis into python::

  import pyhis

  # Output:
  #
  # In [1]: import pyhis
  # cache initialized with database: sqlite:////var/folders/j0/3qhzgkzn7xgdzh0488y4_b340000gn/T/pyhis_cache.db
  
This command makes pyhis and all of its abilities available to python. If you look at the output above you can see
that by default PyHIS has created a sqlite database to automatically cache (store locally) any data and metadata
you access with PyHIS.

If you would like to store the data somewhere else you can provide a path and name for your database::
  pyhis.cache.init_cache(cache_database_uri='mycache.db')
  
  # Output:
  #
  # In [2]: pyhis.cache.init_cache(cache_database_uri='mycache.db')
  # cache initialized with database: sqlite:///mycache.db

This stores downloaded data in the current directory in a sqlite file called mycache.db.
You can also turn off caching for individual services or use different database backends. This is not covered here.

Dude where is my WSDL!
======================

Accessing CUAHSI-HIS data services requires knowing the WSDL (Web Service Definition Language)
of the service you are interested in. This is a very complicated way of saying you need to now the
special web link that provides the data. WSDL's look like this
http://river.sdsc.edu/wateroneflow/NWIS/DailyValues.asmx?WSDL . Clicking on that link takes you to a page
full of gobbledy gook XML that is impossible to understand. This is what PyHIS needs to make the magic happen.

CUAHSI-HIS maintains a list of registered HIS data services on at HIS Central (http://hiscentral.cuahsi.org/). These
can be viewed from within PyHIS by using the following function::

  list_of_services = pyhis.his_central.services()
  list_of_services #to see the list

  # Output:
  # In [3]: list_of_services = pyhis.his_central.services()
  # In [4]: list_of_services
  # [(u'USGS: NWIS Daily Values',
  # 'http://river.sdsc.edu/wateroneflow/NWIS/DailyValues.asmx?WSDL',
  # 'NWISDV'),
  # (u'USGS: NWIS Instantaneous Irregular Data',
  # 'http://river.sdsc.edu/wateroneflow/NWIS/Data.asmx?WSDL',
  # 'NWISIID'),
  # (u'USGS: NWIS Unit Values',
  # 'http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL',
  # 'NWISUV'),
  # (u'EPA: EPA STORET',
  # 'http://river.sdsc.edu/wateroneflow/EPA/cuahsi_1_0.asmx?WSDL',
  # 'EPA'),
  # (u'Chesapeake Bay Information Management System: Chesapeake Bay Information Management System',
  # 'http://eddy.ccny.cuny.edu/CIMS/cuahsi_1_1.asmx?WSDL',
  # 'CIMS'),

The services a returned as a list of tuples each containing the name of the service, the WSDL to access
the service and the network name. PyHIS is not limited to the services registered at HIS Central, any
WaterOneFlow compliant data service can be accessed as long as your know the WSDL url.

