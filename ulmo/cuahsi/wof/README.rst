`CUAHSI WaterOneFlow`_ (WOF) web data access services. These services provide
access to a wide variety of data sources that use the standardized WOF service protocol.
Most such services are registered with the `CUAHSI HIS Central`_ catalog and can
be identified via queries using the ``ulmo.cuahsi.his_central.get_services`` catalog
web service. Each WOF service may have some unique characteristics, such as specific
regional and temporal domains, set of variables, or additional constraints.
The notes below provides additional usage details for some data sources.

- `NRCS SNOTEL`_: USDA Natural Resources Conservation Service (NRCS) Snow Telemetry network
  of remote, high-elevation mountain sites in the western U.S., used to monitor snowpack,
  precipitation, temperature and other climatic conditions. Timestamps in the request and data
  response are in PST (UTC-8).


.. _CUAHSI WaterOneFlow: https://his.cuahsi.org/wofws.html
.. _CUAHSI HIS Central: https://hiscentral.cuahsi.org
.. _NRCS SNOTEL: https://hiscentral.cuahsi.org/pub_network.aspx?n=241
