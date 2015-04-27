import pytest
import ulmo
import test_util
import tempfile
import filecmp

def test_get_attributes():
	with test_util.mocked_urls('usgs/eros/attributes.json'):
		attrs = ulmo.usgs.eros.get_attribute_list()
		assert len(attrs) == 38


def test_get_themes():
	with test_util.mocked_urls('usgs/eros/themes.json'):
		themes = ulmo.usgs.eros.get_themes()
		assert len(themes) == 22


def test_get_available_datasets():
	with test_util.mocked_urls('usgs/eros/datasets.json'):
		bbox = (-78, 32, -76, 36)
		datasets = ulmo.usgs.eros.get_available_datasets(bbox, attrs='AREA_NAME')
		assert len(datasets) >= 30

test_sets = [
 	{'product_key': 'L1L',
 	 'bbox': (-78, 32, -76, 36),
 	 'number_of_tiles': 2,
 	 'file': 'usgs/eros/availability_bbox_test_set_1.json',
 	},
]


def test_get_raster_availability():
 	for dataset in test_sets:
 		with test_util.mocked_urls(dataset['file']):
 			locs = ulmo.usgs.eros.get_raster_availability(dataset['product_key'], dataset['bbox'])
 			assert len(locs['features'])==dataset['number_of_tiles']


def test_get_raster():
 	product_key = 'NCP'
	bbox = (-97.992, 31.991, -97.991, 31.992)
	path = tempfile.gettempdir()
	#availability_url = 'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp?TOP=31.992&BOTTOM=31.991&LEFT=-97.992&RIGHT=-97.991&LAYER_IDS=NCP&JSON=true'
	#jp2_url = 'http://tdds2.cr.usgs.gov/lta5/ortho/naip/compressed/TX/2012/201204_texas_naip_1x0000m_cnir/31097/m_3109701_nw_14_1_20120725_20121015.jp2'
	format_url = 'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx*'
	availability_url = 'http://extract.cr.usgs.gov/*'
	jp2_url = 'http://tdds2.cr.usgs.gov/lta5/ortho/*'
	url_files = {
		format_url: 'usgs/eros/'
		availability_url: 'usgs/eros/get_raster_test_availability.json',
		jp2_url: 'usgs/eros/m_3109701_nw_14_1_20120725_20121015.jp2',
	}

	with test_util.mocked_urls(url_files):
		locs = ulmo.usgs.eros.get_raster(product_key, bbox, path=path)
		raster_tile = locs['features'][0]['properties']['file']
		assert filecmp.cmp(raster_tile, 'files/usgs/eros/m_3109701_nw_14_1_20120725_20121015.jp2')
