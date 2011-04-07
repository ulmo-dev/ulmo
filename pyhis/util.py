"""
    pyhis.util
    ~~~~~~~

    Set of utility functions that help pyhis do its thing.

"""

from shapely.geometry import Point, Polygon

import pyhis


def _get_shapely_from_geolocation(geolocation):
    """returns a shapely object given a suds WaterML geolocation element"""

    if geolocation.geogLocation.__class__.__name__ == 'LatLonPointType':
        return Point(geolocation.geogLocation.longitude,
                     geolocation.geogLocation.latitude)

    else:
        raise NotImplementedError("Don't know how to convert location "
                                  "type: '%s'" %
                                  geolocation.geogLocation.__class__.__name__)


def _get_site_from_site_info(site):
    """returns a PyHIS Site instance from a suds WaterML siteInfo element"""
    if len(site.siteInfo.siteCode) > 1:
        raise NotImplementedError("Multiple site codes not supported")

    site_code = site.siteInfo.siteCode[0]

    return pyhis.Site(name=site.siteInfo.siteName,
                      code=site_code.value,
                      id=site_code._siteID,
                      network=site_code._network,
                      location=site.siteInfo.geoLocation)
