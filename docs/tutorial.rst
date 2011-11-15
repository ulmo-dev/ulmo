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

Installing PyHIS
================

PyHIS is available on the Python Package Index and can be installed on most systems using either ``easy_install pyhis``
or ``pip install pyhis``. PyHIS uses several scientific python plotting and analysis libraries. Although easy_install and
pip will attempt to install these automatically it is better to use a scientific python distribution like
PythonXY (http://www.pythonxy.com, Windows Only)) or the Enthought Python Distribution - EPD Free
(http://enthought.com/products/epd_free.php, Windows/Linux/Mac OS X) prior to installing PyHIS.


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
  len(list_of_services) #number of available services
  list_of_services #to see the list

  # Output:
  # In [3]: list_of_services = pyhis.his_central.services()
  # In [4]: len(list_of_services)
  # 76
  # In [5]: list_of_services
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
  # ...
  # ]

The above command returns a lust of all available services. You can also request a list of services with data
available within a bounding box::

  list_of_texas_services = pyhis.his_central.services(xmin=-106.7, ymin=25.5, xmax=-93.4, ymax=36.6)
  len(list_of_texas_services) #number of services available within bounding box
  list_of_services #to see the list

  # Output:
  # In [6]: list_of_texas_services = pyhis.his_central.services()
  # In [7]: len(list_of_texas_services)
  # 27
  # In [8]: list_of_texas_services
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
  # (u'USGS: NWIS Ground Water Level',
  # 'http://river.sdsc.edu/wateroneflow/NWIS/Groundwater.asmx?WSDL',
  # 'NWISGW'),
  # (u'Texas Instream Flow Program: Texas Instream Flow, Lower Sabine',
  # 'http://his.crwr.utexas.edu/SabineBio/cuahsi_1_0.asmx?WSDL',
  # 'TIFP_LowerSabine'),
  # (u'Texas Instream Flow Program: Texas Instream Flow, Lower San Antonio',
  # 'http://his.crwr.utexas.edu/SanAntonioBio/cuahsi_1_0.asmx?WSDL',
  # 'TIFP_LowerSanAntonio'),
  # ...
  # ]

The services a returned as a list of tuples each containing the name of the service, the WSDL to access
the service and the network name. PyHIS is not limited to the services registered at HIS Central, any
WaterOneFlow compliant data service can be accessed as long as your know the WSDL url.

Once you have the WSDL of a service you want to access data from, the service needs to be initialized in pyhis.
For the following several examples we will use the USGS NWIS Unit Values service.

Initialize the service::

  wsdl_url = 'http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL'
  nwisuv = pyhis.Service(wsdl_url)
  nwisuv #lets see what this is ...

  # Output:
  #
  #
  # In [9]: wsdl_url = 'http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL'
  # In [10]: nwisuv = pyhis.Service(wsdl_url)
  # In [11]: nwisuv
  # <Service: http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL>

This creates a pyhis ``Service`` object called nwisuv that knows everything it needs to about the USGS NWIS service.

Alright already! Lets Get Some Data.
====================================

Now that we have a pyhis Service object ``nwisuv``, lets see what functions are available. If you are using IPython,
type ``nwisuv.`` and press the tab button::

  In [12]: nwisuv.
  nwisuv.default_network             nwisuv.get_site                    nwisuv.sites
  nwisuv.description                 nwisuv.get_sites_within_polygon    nwisuv.sites_array
  nwisuv.generate_sites_array        nwisuv.get_sites_within_radius_r   nwisuv.suds_client
  nwisuv.get_all_sites               nwisuv.get_sites_within_shapefile  nwisuv.url

You will see a list of functions and attributes attached to the ``nwisuv`` object. Lets see what some of these
do (Note: Some of these are internal functions that will be hidden in furture versions of PyHIS)::

  nwisuv.url
  # Output: 'http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL'
  # i.e. the original url we specified

  nwisuv.sites
  # Out: making GetSites query...
  # Out:
  {u'01010000': <Site: St. John River at Ninemile Bridge, Maine [01010000]>,
   u'01010070': <Site: Big Black River near Depot Mtn, Maine [01010070]>,
   u'01010500': <Site: St. John River at Dickey, Maine [01010500]>,
   u'01011000': <Site: Allagash River near Allagash, Maine [01011000]>,
   u'01011500': <Site: St. Francis River near Connors, New Brunswick [01011500]>,
   u'01013500': <Site: Fish River near Fort Kent, Maine [01013500]>,
   u'01014000': <Site: St. John River below Fish R, at Fort Kent, Maine [01014000]>,
   u'01015800': <Site: Aroostook River near Masardis, Maine [01015800]>,
   u'01017000': <Site: Aroostook River at Washburn, Maine [01017000]>,
   u'01017060': <Site: Hardwood Brook below Glidden Brk nr Caribou, Mai [01017060]>,
   u'01017290': <Site: Little Madawaska River at Caribou, Maine [01017290]>,
   ...
   }
  len(nwisuv.sites)
  # Out: 11758

Note: The first time you type ``nwisuv.sites`` pyhis has to connect to the USGS NWIS Unit Values service
and download the list of sites by making a web service request. Hence you will see a message saying
'making GetSites query'. Retrieving and parsing this data can take a few minutes for some of the larger
datasets like the USGS. The next time you use nwisuv.sites or any function that needs the list of sites,
PyHIS uses its automated local cache. so the response is immediate. This is true even if you close the
Python window and open a new prompt. PyHIS has options to force refreshing of the cache on demand.

Lets find some sites within the Austin, TX area. PyHIS has three convinience functions you can use to
narrow down the list of sites you are interested in. These are: ``get_sites_within_polygon``, ``get_sites_within_shapefile``
and ``get_sites_within_radius_r``. These do basically what you would expect from the name::

  travis_sites = nwis_uv.get_sites_within_shapefile('travis_county.shp')
  len(travis_sites)
  # Out: 27
  travis_sites
  # Out:  {'08154500/agency=TX071': <Site: LCRA Lk Travis nr Austin, TX [08154500/agency=TX071]>,
  #        '08154700': <Site: Bull Ck at Loop 360 nr Austin, TX [08154700]>,
  #        '08154900/agency=TX071': <Site: LCRA Lk Austin at Austin, TX [08154900/agency=TX071]>,
  #        '08155200': <Site: Barton Ck at SH 71 nr Oak Hill, TX [08155200]>,
  #        '08155240': <Site: Barton Ck at Lost Ck Blvd nr Austin, TX [08155240]>,
  #        '08155300': <Site: Barton Ck at Loop 360, Austin, TX [08155300]>,
  #        '08155400': <Site: Barton Ck abv Barton Spgs at Austin, TX [08155400]>,
  #        '08155500': <Site: Barton Spgs at Austin, TX [08155500]>,
  #        '08155541': <Site: W Bouldin Ck at Oltorf Rd, Austin, TX [08155541]>,
  #        '08156675': <Site: Shoal Ck at Silverway Dr, Austin, TX [08156675]>,
  #        '08156800': <Site: Shoal Ck at W 12th St, Austin, TX [08156800]>,
  #        '08156910': <Site: Waller Ck at Koenig Lane, Austin, TX [08156910]>,
  #        '08158000': <Site: Colorado Rv at Austin, TX [08158000]>,
  #        '08158030': <Site: Boggy Ck at Manor Rd, Austin, TX [08158030]>,
  #        '08158035': <Site: Boggy Ck at Webberville Rd, Austin, TX [08158035]>,
  #        '08158045': <Site: Ft Br Boggy Ck at Manor Rd, Austin, TX [08158045]>,
  #        '08158200': <Site: Walnut Ck at Dessau Rd, Austin, TX [08158200]>,
  #        '08158380': <Site: Little Walnut Ck at Georgian Dr, Austin, TX [08158380]>,
  #        '08158600': <Site: Walnut Ck at Webberville Rd, Austin, TX [08158600]>,
  #        '08158827': <Site: Onion Ck at Twin Creeks Rd nr Manchaca, TX [08158827]>,
  #        '08158840': <Site: Slaughter Ck at FM 1826 nr Austin, TX [08158840]>,
  #        '08158860': <Site: Slaughter Ck at FM 2304 nr Austin, TX [08158860]>,
  #        '08158920': <Site: Williamson Ck at Oak Hill, TX [08158920]>,
  #        '08158927': <Site: Kincheon Br at William Cannon Blvd, Austin, TX [08158927]>,
  #        '08158930': <Site: Williamson Ck at Manchaca Rd, Austin, TX [08158930]>,
  #        '08158970': <Site: Williamson Ck at Jimmy Clay Rd, Austin, TX [08158970]>,
  #        '08159000': <Site: Onion Ck at US Hwy 183, Austin, TX [08159000]>}  

Lets look at one of the sites::

  nwisuv.sites['08158000']
  # Out: <Site: Colorado Rv at Austin, TX [08158000]>

This is a PyHIS ``Site`` object describing the USGS Gage 08158000 on the Colorado River at Austin TX.
Lets see what we can find out about this gage::

  mysite = nwisuv.sites['08158000']
  mysite. #hit tab
  # Out: mysite.code                mysite.latitude            mysite.network             mysite.timeseries
         mysite.dataframe           mysite.longitude           mysite.service
         mysite.id                  mysite.name                mysite.site_info_response

Lets look at some of these::

  mysite.name
  # Out: u'Colorado Rv at Austin, TX'

  mysite.code
  # Out: u'08158000'

  mysite.latitude
  # Out: 30.244653701782227

  mysite.longitude
  # Out: -97.69445037841797

  mysite.service
  # Out: <Service: http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL>

  mysite.network
  # Out: u'NWISUV'

So the PyHIS site object has pretty much all the metadata you should need about the site you are accessing.

Yada, yada, yada... where is the actual data.
=============================================

Patience, we are there::

  mysite.timeseries
  #Out: making GetSiteInfo request for "NWISUV:08158000"...
  #Out: {00060: <TimeSeries: Discharge, cubic feet per second (2011-07-18 07:51:46 - 2011-11-15 07:51:46)>,
         00065: <TimeSeries: Gage height, feet (2011-07-18 07:51:46 - 2011-11-15 07:51:46)>}

Ah hah! This USGS gage has two available time series datasets; Discharge and Gage height. Also summarized are
the available date ranges of the data. ``00060`` and ``00065`` are the parameter codes for these timeseries. In
the background PyHIS has made a GetSiteInfo webservice request to get the data.

Note: In practice, time period and value counts are not very reliable from service to service depending on how
they have been generated by the data provider. It is better to treat them as estimates.

Lets look at some of the metadata about the discharge timeseries::

  mydischarge = mysite.timeseries['00060']
  mydischarge. #press tab
  # Out: mydischarge.begin_datetime         mydischarge.quality_control_level  mydischarge.value_count
         mydischarge.data                   mydischarge.quantity               mydischarge.variable
         mydischarge.end_datetime           mydischarge.series
         mydischarge.method                 mydischarge.site

  mydischarge.value_count
  # Out: 11520

So a time

Lets get the discharge data for the entire time period::

  mydata = mydischarge.data
  #   --- OR ---
  # mydata = mysite.timeseries['00060'].data #i.e. You can string all the commands together.
  #
  # Out: making timeseries request for "NWISUV:08158000:00060 (None - None)"...
         /Users/dharhas/work/pyhis/pyhis/waterml.py:128: UserWarning: Unit conversion not available for 00060: UNKNOWN [cfs]
         (variable_code, quantity, unit_code))
         /Users/dharhas/work/pyhis/pyhis/cache.py:816: UserWarning: value_count (11520) doesn't match number of values (11415) for Colorado Rv at Austin, TX:00060
         cached_timeseries.variable.code))

Data has been downloaded and placed a ``pandas`` time series object. Pandas (http://pandas.sourceforge.net/)
is a powerful Python data analysis toolkit. The data has also been cached. Next time this particular data is
requested by default only new data will be retrieved from the USGS service. Previously retrieved data will be
read from the local cache.

Lets look at the data::

  mydata
  # Out:
  #  2011-07-18 09:00:00    126.0
  #  2011-07-18 09:15:00    126.0
  #  2011-07-18 09:30:00    139.0
  #  2011-07-18 09:45:00    216.0
  #  2011-07-18 10:00:00    372.0
  #  2011-07-18 10:15:00    553.0
  #  2011-07-18 10:30:00    714.0
  #  ...
  #  2011-11-15 08:00:00    101.0
  #  2011-11-15 08:15:00    105.0
  #  2011-11-15 08:30:00    105.0
  #  2011-11-15 08:45:00    108.0
  #  2011-11-15 09:00:00    108.0
  #  2011-11-15 09:15:00    108.0
  #  2011-11-15 09:30:00    108.0
  #  2011-11-15 09:45:00    108.0
  #  length: 11415

  mydata. #press tab
  # Out: mydata.
  #       Display all 131 possibilities? (y or n)
  #       mydata.T                  mydata.data               mydata.map                mydata.shift
  #       mydata.add                mydata.describe           mydata.max                mydata.size
  #       mydata.all                mydata.diagonal           mydata.mean               mydata.skew
  #       mydata.any                mydata.diff               mydata.median             mydata.sort
  #       mydata.append             mydata.div                mydata.merge              mydata.sort_index
  #       mydata.apply              mydata.dot                mydata.min                mydata.sortlevel
  #       mydata.applymap           mydata.drop               mydata.mul                mydata.squeeze
  #       mydata.argmax             mydata.dropna             mydata.nbytes             mydata.std
  #       mydata.argmin             mydata.dtype              mydata.ndim               mydata.strides
  #       mydata.argsort            mydata.dump               mydata.newbyteorder       mydata.sub
  #       mydata.asOf               mydata.dumps              mydata.nonzero            mydata.sum
  #       mydata.asfreq             mydata.fill               mydata.order              mydata.swapaxes
  #       mydata.asof               mydata.fillna             mydata.plot               mydata.swaplevel
  #       mydata.astype             mydata.first_valid_index  mydata.prod               mydata.take
  #       mydata.autocorr           mydata.flags              mydata.ptp                mydata.toCSV
  #       mydata.base               mydata.flat               mydata.put                mydata.toDict
  #       mydata.byteswap           mydata.flatten            mydata.quantile           mydata.toString
  #       mydata.choose             mydata.fromValue          mydata.ravel              mydata.to_csv
  #       mydata.clip               mydata.get                mydata.real               mydata.to_dict
  #       mydata.clip_lower         mydata.getfield           mydata.reindex            mydata.to_sparse
  #       mydata.clip_upper         mydata.groupby            mydata.reindex_like       mydata.tofile
  #       mydata.combine            mydata.hist               mydata.rename             mydata.tolist
  #       mydata.combineFirst       mydata.imag               mydata.repeat             mydata.tostring
  #       mydata.combine_first      mydata.index              mydata.reshape            mydata.trace
  #       mydata.compress           mydata.interpolate        mydata.resize             mydata.transpose
  #       mydata.conj               mydata.item               mydata.round              mydata.truncate
  #       mydata.conjugate          mydata.itemset            mydata.save               mydata.unstack
  #       mydata.copy               mydata.itemsize           mydata.searchsorted       mydata.valid
  #       mydata.corr               mydata.iteritems          mydata.select             mydata.values
  #       mydata.count              mydata.ix                 mydata.setasflat          mydata.var
  #       mydata.ctypes             mydata.keys               mydata.setfield           mydata.view
  #       mydata.cumprod            mydata.last_valid_index   mydata.setflags           mydata.weekday
  #       mydata.cumsum             mydata.load               mydata.shape


As you can see there is a pretty long List of functions available for a ``pandas`` timeseries object. Lets try
a few::

  mydata.min()
  # Out: 52.0

  mydata.max()
  # Out: 2850.0

  mydata.median()
  # Out: 548.0

  mydata.std()
  # Out: 774.01376212573985

  # or just look at all the basic stats
  mydata.describe()
  # Out: count    11415.0
         mean     872.066579063
         std      774.013762126
         min      52.0
         10%      108.0
         50%      548.0
         90%      2030.0
         max      2850.0

  mydata.cumsum()
  # Out: 2011-07-18 09:00:00    126.0
         2011-07-18 09:15:00    252.0
         2011-07-18 09:30:00    391.0
         2011-07-18 09:45:00    607.0
         2011-07-18 10:00:00    979.0
         2011-07-18 10:15:00    1532.0
         2011-07-18 10:30:00    2246.0
         ...
         2011-11-15 08:30:00    9954100.0
         2011-11-15 08:45:00    9954208.0
         2011-11-15 09:00:00    9954316.0
         2011-11-15 09:15:00    9954424.0
         2011-11-15 09:30:00    9954532.0
         2011-11-15 09:45:00    9954640.0
         length: 11415

  # Plot data
  mydata.plot()

  # Plot Cumulative Sum
  mydata.cumsum().plot()

  # save data to csv file
  mydata.to_csv('mydata.csv')

Getting more complicated. Lets write a script
=============================================

Look at tut_example1.py

