"""
    ulmo.usgs.ned.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to the `National Elevation Dataset` provided by the `United States Geological
    Survey`_ `National Map`_ system.

    .. _National Elevation Dataset: http://ned.usgs.gov/
    .. _United States Geological Survey: http://www.usgs.gov/
    .. _National Map: http://nationalmap.gov

"""

import hashlib
import json
import logging
import numpy as np
import os
import pandas as pd
import requests
import subprocess
from ulmo import util



# NED ftp url.  
NED_FTP_URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/<layer>/IMG/'

# ScienceBase webservice url for IMG format NED tiles
# https://www.sciencebase.gov/catalog/items?fields=id,title,summary,body,tags,webLinks,dates,spatial&q=&filter=tags=National Elevation Dataset (NED) 1/9 arc-second&filter=spatialQuery=Polygon ((-95.26155638325938 40.07132704825149,-94.16292357075272 40.07132704825149,-94.16292357075272 40.594749211728654,-95.26155638325938 40.594749211728654,-95.26155638325938 40.07132704825149))&format=json
NED_WS_URL = 'https://www.sciencebase.gov/catalog/items?fields=webLinks&q=&filter=tags=National Elevation Dataset (NED) %s&filter=tags=IMG&filter=spatialQuery=Polygon ((%s))&format=json'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/ned/'

layer_dict = {
        'Alaska 2 arc-second': '2',
        '1 arc-second': '1',
        '1/3 arc-second': '13',
        '1/9 arc-second': '19',
    }

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



def get_file_index(path=None, update_cache=False):
    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    filename = os.path.join(path, 'index.json')

    if not os.path.exists(filename) or update_cache:
        for dirname in layer_dict.itervalues():
            layer_path = os.path.join(path, dirname, 'zip')
            if not os.path.exists(layer_path):
                os.makedirs(layer_path)

        _update_file_index(filename)

    with open(filename) as f:
        return json.load(f)


def get_tile_urls(layer, xmin, ymin, xmax, ymax, path=None, use_webservice=False):
    """
        Find tile urls corresponding to the given layer and bounding box
    """
    if use_webservice:
        polygon = ','.join([(repr(x) + ' ' + repr(y)) for x,y in [
            (xmin, ymax),
            (xmin, ymin), 
            (xmax, ymin), 
            (xmax, ymax), 
            (xmin, ymax)]])
        url = NED_WS_URL % (layer, polygon)
        r = requests.get(url)
        urls = []
        for tile in r.json()['items']:
            urls.append([x for x in tile['webLinks'] if x['type']=='download'][0]['uri'])

        return sorted(urls)

    base_url = NED_FTP_URL.replace('<layer>', layer_dict[layer])
    file_index = get_file_index(path=path)

    if layer in ['1 arc-second', '1/3 arc-second', 'Alaska 2 arc-second']:
        lats = np.arange(np.ceil(ymin), np.ceil(ymax)+1)
        lons = np.arange(np.floor(xmin), np.floor(xmax)+1)
        files = []
        fmt_lat = lambda x: 's%0d' % np.abs(x) if x<0 else 'n%0d' % x
        fmt_lon = lambda x: 'w%03d' % np.abs(x) if x<0 else 'e%03d' % x
        fmt = '%s%s.zip'
        for lat in lats:
            for lon in lons:
                files.append(fmt % (fmt_lat(lat), fmt_lon(lon)))

        available_files = list(set(file_index[layer]).intersection(set(files)))

        urls = [base_url + filename for filename in available_files]
        return sorted(urls)

    if layer=='1/9 arc-second':
        raise NotImplementedError("1/9 arc-second NED local tile determination not implemented yet")


def _update_file_index(filename):
    index = {}
    for name, layer in layer_dict.iteritems():
        print 'retrieving file index for NED layer - %s' % name
        url = NED_FTP_URL.replace('<layer>', layer)
        index[name] = sorted([line for line in util.dir_list(url) if 'zip' in line])
        
    with open(filename, 'wb') as outfile:
        json.dump(index, outfile)
        print 'ned raster file index saved in %s' % filename

    return filename


def get_raster(layer, xmin, ymin, xmax, ymax, path=None, update_cache=False, 
    check_modified=False):

    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    util.mkdir_if_doesnt_exist(os.path.join(path, 'by_boundingbox'))
    uid = util.generate_raster_uid(layer, xmin, ymin, xmax, ymax)
    output_path = os.path.join(path, 'by_boundingbox', uid + '.tif')

    layer_path = os.path.join(path, layer_dict[layer])

    if os.path.isfile(output_path) and not update_cache:
        return output_path

    print 'Downloading tiles needed for requested bounding box:'
    tile_urls = get_tile_urls(layer, xmin, ymin, xmax, ymax)
    tile_fmt = '.img'
    raster_tiles = util.download_tiles(layer_path, tile_urls, tile_fmt, check_modified)
    util.mosaic_and_clip(raster_tiles, xmin, ymin, xmax, ymax, output_path)

    return output_path
