"""
    ulmo.usgs.ned.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to the `National Elevation Dataset` provided by the `United States Geological
    Survey`_ `National Map`_ system.

    .. _National Elevation Dataset: http://ned.usgs.gov/
    .. _United States Geological Survey: http://www.usgs.gov/
    .. _National Map: http://nationalmap.gov

"""

from geojson import Feature, FeatureCollection, Polygon
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
NED_WS_URL = 'https://www.sciencebase.gov/catalog/items?fields=webLinks,spatial,title&q=&filter=tags=National Elevation Dataset (NED) %s&filter=tags=IMG&filter=spatialQuery=Polygon ((%s))&format=json&max=1000'
SCIENCEBASE_ITEM_URL = 'https://www.sciencebase.gov/catalog/item/%s?format=json'

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


def get_available_layers():
    """return list of available data layers
    """
    return layer_dict.keys()


def get_raster_availability(layer, bbox):
    """retrieve metadata for raster tiles that cover the given bounding box 
    for the specified data layer. 

    Parameters
    ----------
    layer : str
        dataset layer name. (see get_available_layers for list)
    bbox : (sequence of float|str)
        bounding box of in geographic coordinates of area to download tiles 
        in the format (min longitude, min latitude, max longitude, max latitude)
        
    Returns
    -------
    metadata : geojson FeatureCollection
        returns metadata including download urls as a FeatureCollection
    """
    xmin, ymin, xmax, ymax = [float(n) for n in bbox]
    polygon = ','.join([(repr(x) + ' ' + repr(y)) for x,y in [
        (xmin, ymax),
        (xmin, ymin), 
        (xmax, ymin), 
        (xmax, ymax), 
        (xmin, ymax)]])
    url = NED_WS_URL % (layer, polygon)
    
    features = []
    while url:
        print 'retrieving raster availability from %s' % url
        r = requests.get(url)
        content = r.json()
        for item in content['items']:
            feature = Feature(geometry=Polygon(_bbox2poly(item['spatial']['boundingBox'])), id=item['id'], 
                        properties={
                            'name': item['title'], 
                            'layer': layer,
                            'format': '.img',
                            'download url': [x for x in item['webLinks'] if x['type']=='download'][0]['uri']}
                    )
            features.append(feature)

        if content.get('nextlink'):
            url = content['nextlink']['url']
        else:
            break

    return FeatureCollection(features)


def get_raster(layer, bbox, path=None, check_modified=False, mosaic=False):
    """downloads National Elevation Dataset raster tiles that cover the given bounding box 
    for the specified data layer. 

    Parameters
    ----------
    layer : str
        dataset layer name. (see get_available_layers for list)
    bbox : (sequence of float|str)
        bounding box of in geographic coordinates of area to download tiles 
        in the format (min longitude, min latitude, max longitude, max latitude)
    path : ``None`` or path
        if ``None`` default path will be used
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
    raster_tiles = _download_tiles(get_raster_availability(layer, bbox), path=path, 
        check_modified=check_modified)

    if mosaic:
        if path is None:
            path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

        util.mkdir_if_doesnt_exist(os.path.join(path, 'by_boundingbox'))
        uid = util.generate_raster_uid(layer, xmin, ymin, xmax, ymax)
        output_path = os.path.join(path, 'by_boundingbox', uid + '.tif')

        if os.path.isfile(output_path) and not update_cache:
            return output_path

        raster_files = [tile['properties']['file'] for tile in raster_tiles['features']]
        util.mosaic_and_clip(raster_files, xmin, ymin, xmax, ymax, output_path)
        return [output_path]

    return raster_tiles



def _get_file_index(path=None, update_cache=False):
    """Non webservice approach for caching file index

    Experimental, not currently in use.
    """
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


def _get_tile_urls(layer, xmin, ymin, xmax, ymax, path=None):
    """Non webservice approach to identify tile urls corresponding to the given layer and bounding box

    Experimental, not currently in use.
    """

    base_url = NED_FTP_URL.replace('<layer>', layer_dict[layer])
    file_index = _get_file_index(path=path)

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
    """ Non webservice approach for caching file index

    Experimental, not currently in use.
    """
    index = {}
    for name, layer in layer_dict.iteritems():
        print 'retrieving file index for NED layer - %s' % name
        url = NED_FTP_URL.replace('<layer>', layer)
        index[name] = sorted([line for line in util.dir_list(url) if 'zip' in line])
        
    with open(filename, 'wb') as outfile:
        json.dump(index, outfile)
        print 'ned raster file index saved in %s' % filename

    return filename


def _download_features(feature_ids, path=None, check_modified=False,):
    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    if isinstance(feature_ids, basestring):
        feature_ids = [feature_ids]

    tiles =[]
    tile_fmt = '.img'
    for feature_id in feature_ids:
        url = SCIENCEBASE_ITEM_URL % feature_id
        metadata = requests.get(url).json()
        layer = [a for a in layer_dict.keys() if a in metadata['title']][0]
        layer_path = os.path.join(path, layer_dict[layer])
        tile_urls = [link['uri'] for link in metadata['webLinks'] if link['type']=='download']
        tiles.append({'feature_id': feature_id,
                      'tiles': util.download_tiles(layer_path, tile_urls, tile_fmt, check_modified),
                      })

    return tiles


def _bbox2poly(bbox):
    xmin = bbox['minX']
    xmax = bbox['maxX']
    ymin = bbox['minY']
    ymax = bbox['maxY']

    return [[(xmin,ymin), (xmin,ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)]]


def _download_tiles(tiles, path=None, check_modified=False):

    if path is None:
        path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

    for tile in tiles['features']:

        metadata = tile['properties']
        layer_path = os.path.join(path, layer_dict[metadata['layer']])
        tile['properties']['file'] = util.download_tiles(layer_path, metadata['download url'], metadata['format'], check_modified)[0]

    return tiles  