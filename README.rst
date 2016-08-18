ulmo
====

**clean, simple and fast access to public hydrology and climatology data**


Project Status
--------------

.. image:: https://secure.travis-ci.org/ulmo-dev/ulmo.png?branch=master
        :target: https://travis-ci.org/ulmo-dev/ulmo

.. image:: https://ci.appveyor.com/api/projects/status/mqo6rl0f2ocngxcu/branch/master?svg=true
        :target: https://ci.appveyor.com/project/dharhas/ulmo/branch/master

.. image:: https://coveralls.io/repos/ulmo-dev/ulmo/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/ulmo-dev/ulmo?branch=master


Features
--------

- retrieves and parses datasets from the web
- returns simple python data structures that can be easily pulled into `more
  sophisticated tools`_ for analysis
- caches datasets locally and harvests updates as needed


Datasets
--------

Currently, ulmo supports the following datasets / services:

- California Department of Water Resources Historical Data
- Climate Prediction Center Weekly Drought
- CUAHSI WaterOneFlow
- Lower Colorado River Authority Hydromet and Water Quality Data
- NASA Daymet weather data
- National Climatic Data Center Climate Index Reference Sequential (CIRS)
- National Climatic Data Center Global Historical Climate Network Daily
- National Climatic Data Center Global Summary of the Day
- Texas Weather Connection Daily Keetch-Byram Drought Index (KBDI)
- US Army Corps of Engineers - Tulsa District Water Control
- USGS National Water Information System
- USGS Emergency Data Distribution Network services
- USGS Earth Resources Observation Systems (EROS) services
- USGS National Elevation Dataset (NED) services

Installation
------------

Ulmo depends on a lot of libraries from the scientific python stack (namely:
numpy, pytables and pandas) and lxml. There are a couple of ways to get these
dependencies installed but it can be tricky if doing it by hand. The simplest
way to get things up and running is to use a scientific python distribution that
will install everything together. A full list is available on the `scipy`_
website but `Anaconda`_ / `Miniconda`_ is recommended as it is the easiest to set up.

If you are using Anaconda/Miniconda then you can install ulmo from the `conda_forge`_
channel with the following command:

    conda install -c conda-forge ulmo

Otherwise, follow the instructions below:

Once the requisite scientific python libraries are installed, the
most recent release of ulmo can be installed from pypi. Pip is a good way to do
that:

    pip install ulmo

To install the bleeding edge development version, grab a copy of the `source
code`_ and run setup.py from the root directory:

To setup a development environment using conda:

    conda env create -n myenv --file py2_conda_environment.yml (or py3_conda_environment.yml if you want to work with python 3)

    source activate myenv (use 'activate test_environment' on windows)

    python setup.py develop


Future
------

A list of future datasets is kept in on the `issue tracker`_. If there's a dataset
you'd like to see added, please open an issue about it.



Links
-----

* Documentation: http://ulmo.readthedocs.org
* Repository: https://github.com/ulmo-dev/ulmo


.. _more sophisticated tools: http://pandas.pydata.org
.. _issue tracker: https://github.com/ulmo-dev/ulmo/issues?labels=new+dataset&state=open
.. _Anaconda: http://continuum.io/downloads.html
.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _conda-forge: https://conda-forge.github.io
.. _scipy: http://scipy.org/install.html
.. _source code: https://github.com/ulmo-dev/ulmo
