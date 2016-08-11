"""
    ulmo.usgs.ned.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to the `National Elevation Dataset` provided by the `United States Geological
    Survey`_ `National Map`_ system.

    .. _National Elevation Dataset: http://ned.usgs.gov/
    .. _United States Geological Survey: http://www.usgs.gov/
    .. _National Map: http://nationalmap.gov

"""
from __future__ import print_function
from past.builtins import basestring

from geojson import Feature, FeatureCollection, Polygon
import logging
import os
import requests
from ulmo import util


# NED ftp url.
NED_FTP_URL = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/<layer>/IMG/'

# default file path (appended to default ulmo path)
DEFAULT_FILE_PATH = 'usgs/ned/'

layer_dict = {
        'Alaska 2 arc-second': '4f70aaece4b058caae3f8de9',
        '1 arc-second': '4f70aa71e4b058caae3f8de1',
        '1/3 arc-second': '4f70aa9fe4b058caae3f8de5',
        '1/9 arc-second': '4f70aac4e4b058caae3f8de7',
    }

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_available_layers():
    """return list of available data layers
    """
    return list(layer_dict.keys())


def get_raster_availability(layer, bbox=None):
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

    base_url = 'https://www.sciencebase.gov/catalog/items'
    params = [
        ('parentId', layer_dict[layer]),
        ('filter', 'tags=IMG'),
        ('max', 1000),
        ('fields', 'webLinks,spatial,title'),
        ('format', 'json'),
    ]

    if bbox:
        xmin, ymin, xmax, ymax = [float(n) for n in bbox]
        polygon = 'POLYGON (({}))'.format(','.join([(repr(x) + ' ' + repr(y)) for x,y in [
            (xmin, ymax),
            (xmin, ymin),
            (xmax, ymin),
            (xmax, ymax),
            (xmin, ymax)]]))
        params.append(('filter', 'spatialQuery={{wkt:"{}",relation:"{}"}}'.format(polygon, 'intersects')))

    features = []
    url = base_url
    while url:
        r = requests.get(url, params)
        print('retrieving raster availability from %s' % r.url)
        params = []  # not needed after first request
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


def get_raster(layer, bbox, path=None, update_cache=False,
               check_modified=False, mosaic=False):
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
    update_cache: ``True`` or ``False`` (default)
        if ``False`` and output file already exists use it.
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
    _check_layer(layer)

    raster_tiles = _download_tiles(get_raster_availability(layer, bbox), path=path,
        check_modified=check_modified)

    if mosaic:
        if path is None:
            path = os.path.join(util.get_ulmo_dir(), DEFAULT_FILE_PATH)

        util.mkdir_if_doesnt_exist(os.path.join(path, 'by_boundingbox'))
        xmin, ymin, xmax, ymax = [float(n) for n in bbox]
        uid = util.generate_raster_uid(layer, xmin, ymin, xmax, ymax)
        output_path = os.path.join(path, 'by_boundingbox', uid + '.tif')

        if os.path.isfile(output_path) and not update_cache:
            return output_path

        raster_files = [tile['properties']['file'] for tile in raster_tiles['features']]
        util.mosaic_and_clip(raster_files, xmin, ymin, xmax, ymax, output_path)
        return [output_path]

    return raster_tiles

def _check_layer(layer):
    """
    make sure the passed layer name is one of the handled options
    """

    if not layer in get_available_layers():
        err_msg = "The specified layer parameter ({})".format(layer)
        err_msg += "\nis not in the available options:"
        err_msg += "\n\t".join(get_available_layers())
        raise ValueError(err_msg)


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
        layer = [a for a in list(layer_dict.keys()) if a in metadata['title']][0]
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
