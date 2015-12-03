"""
    ulmo.usgs.eros.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `United States Geological
    Survey`_ `Earth Resources Observation and Science (EROS) Center`_ application
    services web site.

    The `DCP message format`_ includes some header information that is parsed and
    the message body, with a variable number of characters. The format of the
    message body varies widely depending on the manufacturer of the transmitter,
    data logger, sensors, and the technician who programmed the DCP. The body can
    be simple ASCII, sometime with parameter codes and time-stamps embedded,
    sometimes not. The body can also be in 'Pseudo-Binary' which is character
    encoding of binary data that uses 6 bits of every byte and guarantees that
    all characters are printable.


    .. _United States Geological Survey: http://www.usgs.gov/
    .. _Earth Resources Observation and Science (EROS) Center: http://nimbus.cr.usgs.gov/app_services.php

"""
from __future__ import print_function

from geojson import Feature, FeatureCollection, Polygon
import hashlib
import logging
import os
import pandas as pd
import requests
import subprocess
from ulmo import util
import zipfile


# eros services base urls
EROS_INVENTORY_URL = 'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx'
EROS_VALIDATION_URL = 'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp?TOP=%s&BOTTOM=%s&LEFT=%s&RIGHT=%s&LAYER_IDS=%s&JSON=true'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/eros/'

ext = {
        'geotiff': '.tif',
        'img': '.img',
        'jpg2000': '.jp2',
        '': '',
    }

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_attribute_list(as_dataframe=True):
    """retrieve list of metadata attributes for dataset

    Parameters
    ----------
    as_dataframe : ``True`` (default) or ``False``
        if ``True`` return pandas dataframe

    Returns
    -------
        available metadata attributes
    """
    url = EROS_INVENTORY_URL + '/return_Attribute_List'
    return _call_service(url, {}, as_dataframe)


def get_available_datasets(bbox, attrs=None, as_dataframe=True):
    """retrieve available datasets for a given bounding box. 

    Parameters
    ----------
    bbox : (sequence of float|str)
        bounding box of in geographic coordinates of area to download tiles 
        in the format (min longitude, min latitude, max longitude, max latitude)
    attrs: comma separated list of str
        metadata attributes to retrieve, `None` (default) retrieves all
    as_dataframe : ``True`` (default) or ``False``
        if ``True`` return pandas dataframe
        
    Returns
    -------
    datasets : dict or pandas DataFrame
        returns availabel datasets
    """
    xmin, ymin, xmax, ymax = [float(n) for n in bbox]
    epsg = 4326

    if attrs is None:
        attrs = ','.join(get_attribute_list().drop(37)['name'].tolist()) #attr 37->LYR_URL causing null returns

    payload = {
                'Attribs': attrs,
                'Xmin': xmin,
                'Ymin': ymin,
                'Xmax': xmax,
                'Ymax': ymax,
                'EPSG': epsg,
        }

    url = EROS_INVENTORY_URL + '/return_Attributes_Download_Only'
    return _call_service(url, payload, as_dataframe)


def get_available_formats(product_key, as_dataframe=True):
    """retrieve list of data formats available for dataset

    Parameters
    ----------
    product_key : str
        dataset name. (see get_available_datasets for list)
    as_dataframe : ``True`` (default) or ``False``
        if ``True`` return pandas dataframe

    Returns
    -------
        available data formats
    """
    url = EROS_INVENTORY_URL + '/return_Download_Options'
    payload = {'ProductIDs': product_key}
    return _call_service(url, payload, as_dataframe)


def get_raster_availability(product_key, bbox, fmt=None):
    """retrieve metadata for raster tiles that cover the given bounding box 
    for the specified data layer. 

    Parameters
    ----------
    product_key : str
        dataset layer name. (see get_available_layers for list)
    bbox : (sequence of float|str)
        bounding box of in geographic coordinates of area to download tiles 
        in the format (min longitude, min latitude, max longitude, max latitude)
    fmt : str
        desired data format. if `None`, geotiff followed by img will be given preference
        
    Returns
    -------
    metadata : geojson FeatureCollection
        returns metadata including download urls as a FeatureCollection
    """

    xmin, ymin, xmax, ymax = [float(n) for n in bbox]
    layer, fmt = _layer_id(product_key, fmt)

    url = EROS_VALIDATION_URL % (ymax, ymin, xmin, xmax, layer)
    print('retrieving raster availability from %s' % url)
    r = requests.get(url)

    tiles = r.json()['REQUEST_SERVICE_RESPONSE']['PIECE']
    
    features = []
    for tile in tiles:         
        features.append(Feature(geometry=Polygon(_bbox2poly(tile['BBOX'])), id=tile['ID'], 
                    properties={'download url': _extract_url(tile['DOWNLOAD_URL']),'product_key': product_key, 'format': fmt}
                    ))
    
    return FeatureCollection(features)


def get_raster(product_key, bbox, fmt=None, path=None, check_modified=False, mosaic=False):
    """downloads National Elevation Dataset raster tiles that cover the given bounding box 
    for the specified data layer. 

    Parameters
    ----------
    product_key : str
        dataset name. (see get_available_datasets for list)
    bbox : (sequence of float|str)
        bounding box of in geographic coordinates of area to download tiles 
        in the format (min longitude, min latitude, max longitude, max latitude)
    fmt : ``None`` or str
        available formats vary in different datasets. If ``None``, preference will be given
        to geotiff and then img, followed by whatever fmt is available
    path : ``None`` or path
        if ``None`` default path will be used
    update_cache: ``True`` or ``False`` (default)
        if ``False`` then tiles will not be re-downloaded if they exist in the path
    check_modified: ``True`` or ``False`` (default)
        if tile exists in path, check if newer file exists online and download if available.  
    mosaic: ``True`` or ``False`` (default)
        if ``True``, mosaic and clip downloaded tiles to the extents of the bbox provided. Requires
        rasterio package and GDAL.
        
    Returns
    -------
    raster_tiles : geojson FeatureCollection
        metadata as a FeatureCollection. local url of downloaded data is in feature['properties']['file']
    """
    raster_tiles = _download_tiles(get_raster_availability(product_key, bbox, fmt),
        path, check_modified)

    if mosaic:
        if path is None:
            path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)
        util.mkdir_if_doesnt_exist(os.path.join(path, 'by_boundingbox'))
        uid = util.generate_raster_uid(product_key, xmin, ymin, xmax, ymax)
        output_path = os.path.join(path, 'by_boundingbox', uid + '.tif')

        if os.path.isfile(output_path) and not update_cache:
            return output_path

        raster_files = [tile['properties']['file'] for tile in raster_tiles['features']]
        util.mosaic_and_clip(raster_files, xmin, ymin, xmax, ymax, output_path)
        
        return [output_path]

    return raster_tiles


def get_themes(as_dataframe=True):
    """retrieve list of data themes available

    Parameters
    ----------
    as_dataframe : ``True`` (default) or ``False``
        if ``True`` return pandas dataframe

    Returns
    -------
        available data themes
    """
    url = EROS_INVENTORY_URL + '/return_Themes'
    return _call_service(url, {}, as_dataframe)


def _bbox2poly(bbox):
    xmin = bbox['LEFT']
    xmax = bbox['RIGHT']
    ymin = bbox['BOTTOM']
    ymax = bbox['TOP']

    return [[(xmin,ymin), (xmin,ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)]]


def _call_service(url, payload, as_dataframe):
    payload['callback'] = ''
    print('calling %s with payload %s' % (url, repr(payload)))
    r = requests.get(url, params=payload)
    if as_dataframe:
        df = pd.DataFrame(r.json()['items'])
        if df.empty:
            return df
        df.index = df['ID']
        del df['ID']
        return df
    else:
        return r.json()


def _download_tiles(tiles, path=None, check_modified=False):

    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    for tile in tiles['features']:

        metadata = tile['properties']
        layer_path = os.path.join(path, metadata['product_key'])
        tile['properties']['file'] = util.download_tiles(layer_path, metadata['download url'], metadata['format'], check_modified)[0]

    return tiles


def _extract_url(url):
    headers = requests.head(url).headers
    if 'location' in list(headers.keys()):
        url = headers['location']

    return url


def _layer_id(product_key, fmt=None):
    available_formats = get_available_formats(product_key)
    if not available_formats.empty:
        available_formats = available_formats['outputformat'][0].lower()
    else:
        available_formats = ''

    if fmt is None:
        if 'geotiff' in available_formats:
            fmt = 'geotiff'
        elif 'img' in available_formats:
            fmt = 'img'
        else:
            fmt = available_formats.split(',')[0].split('-')[-1]
    else:
        if fmt not in available_formats:
            raise ValueError('file format %s not available for product %s' % (fmt, product_key))

    pos = available_formats.find(fmt)
    layer_id = product_key + available_formats[pos-3:pos-1]

    return layer_id, ext[fmt]