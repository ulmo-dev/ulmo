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

import logging
import os
import pandas as pd
import requests
from ulmo import util


# eros services base urls
EROS_INVENTORY_URL = 'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx'
EROS_VALIDATION_URL = 'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp?TOP=%s&BOTTOM=%s&LEFT=%s&RIGHT=%s&LAYER_IDS=%s&JSON=true'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/eros/'

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_attribute_list(as_dataframe=True):
    url = EROS_INVENTORY_URL + '/return_Attribute_List'
    return _call_service(url, {}, as_dataframe)


def get_available_datasets(xmin, ymin, xmax, ymax, epsg=4326, attrs=None, as_dataframe=True):
    if epsg != 4326:
        raise NotImplementedError

    if attrs is None:
        attrs = ','.join(list_attributes()['name'].tolist())

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
    url = EROS_INVENTORY_URL + '/return_Download_Options'
    payload = {'ProductIDs': product_key}
    return _call_service(url, payload, as_dataframe)


def get_raster(product_key, xmin, ymin, xmax, ymax, fmt=None, type='tiled', path=None):

    if type!='tiled':
        raise NotImplementedError

    available_formats = get_available_formats(product_key)['outputformat'][0].lower()
    if fmt is None:
        if 'geotiff' in available_formats:
            fmt = 'geotiff'
        elif 'img' in available_formats:
            fmt = 'img'
        else:
            fmt = available_formats.split('-')[0]
    else:
        if fmt not in available_formats:
            raise ValueError, 'file format %s not available for product %s' % (fmt, product_key)

    pos = available_formats.find(fmt)
    layer_id = product_key + available_formats[pos-3:pos-1]
    
    url = EROS_VALIDATION_URL % (ymax, ymin, xmin, xmax, layer_id)
    r = requests.get(url)

    tiles = r.json()['REQUEST_SERVICE_RESPONSE']['PIECE']

    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    if not os.path.exists(path):
        os.makedirs(path)

    for i, tile in enumerate(tiles):
        url = tile['DOWNLOAD_URL']
        filename = os.path.split(url)[-1].split('&')[0]
        full_path = os.path.join(path, filename)
        print 'downloading tile %s of %s: saved as %s (file format - %s) \n url: %s' % (i+1, len(tiles), full_path, fmt, url)
        util.download_if_new(url, full_path, check_modified=True)


def get_themes(as_dataframe=True):
    url = EROS_INVENTORY_URL + '/return_Themes'
    return _call_service(url, {}, as_dataframe)


def _call_service(url, payload, as_dataframe):
    payload['callback'] = ''
    r = requests.get(url, params=payload)
    if as_dataframe:
        df = pd.DataFrame(r.json()['items'])
        df.index = df['ID']
        del df['ID']
        return df
    else:
        return r.json()
