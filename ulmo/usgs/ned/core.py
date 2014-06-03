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
import zipfile


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


def get_raster(layer, xmin, ymin, xmax, ymax, path=None, use_cache=True):
    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(os.path.join(path, 'by_boundingbox')):
        os.makedirs(os.path.join(path, 'by_boundingbox'))

    uid = hashlib.md5(','.join([layer, repr(xmin), repr(ymin), repr(xmax), repr(ymax)])).hexdigest()
    output_path = os.path.join(path, 'by_boundingbox', uid + '.tif')

    if os.path.isfile(output_path):
        return output_path

    print 'Downloading tiles needed for requested bounding box:'
    raster_tiles = []
    tiles = get_tile_urls(layer, xmin, ymin, xmax, ymax)
    for i, url in enumerate(tiles):
        filename = os.path.split(url)[-1]
        zip_path = os.path.join(path, layer_dict[layer], 'zip', filename)

        print '... downloading tile %s of %s from %s' % (i+1, len(tiles), url)
        util.download_if_new(url, zip_path, check_modified=True)
        print '... ... zipfile saved at %s' % zip_path
        tile_path = zip_path.replace('/zip', '')
        raster_tiles.append(_extract_raster_from_zip(zip_path, tile_path))

    print 'Mosaic and clip to bounding box extents'
    tile_path = os.path.split(tile_path)[0]
    print subprocess.check_output(['gdalwarp', '-te', repr(xmin), repr(ymin), repr(xmax), repr(ymax)] + raster_tiles + [output_path])
    return output_path
   

def _extract_raster_from_zip(zip_path, tile_path):
    tile_path = os.path.splitext(tile_path)[0] + '.img'
    with zipfile.ZipFile(zip_path) as z:
        fname = [x for x in z.namelist() if '.img' in x][0]
        with open(tile_path, 'w') as f:
            f.write(z.read(fname))
            print '... ... .img format raster saved at %s' % (tile_path)

    return tile_path
