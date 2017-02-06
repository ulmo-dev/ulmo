import pytest
import ulmo
import test_util
import filecmp


test_sets = [
	{'layer': '1 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	 'number_of_tiles': 7,
	 'file': 'usgs/ned/availability_bbox_test_set_1.json',
	},
	{'layer': '1/3 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	 'number_of_tiles': 7,
	 'file': 'usgs/ned/availability_bbox_test_set_2.json',
	},
	{'layer': 'Alaska 2 arc-second',
	 'bbox': (-150.4969, 60.7338, -148.4600, 61.5253),
	 'number_of_tiles': 6,
	 'file': 'usgs/ned/availability_bbox_test_set_3.json',
	},
]


def test_get_raster_availability():
	for dataset in test_sets:
		with test_util.mocked_urls(dataset['file']):
			locs = ulmo.usgs.ned.get_raster_availability(dataset['layer'], dataset['bbox'])
			assert len(locs['features'])==dataset['number_of_tiles']


def test_get_raster():
	layer = 'Alaska 2 arc-second'
	bbox = (-149.5, 60.5, -149.3, 60.7)
	#availability_url = 'https://www.sciencebase.gov/catalog/items?fields=webLinks,spatial,title&q=&filter=tags=National Elevation Dataset (NED) Alaska 2 arc-second&filter=tags=IMG&filter=spatialQuery=Polygon ((-149.5 60.7,-149.5 60.5,-149.3 60.5,-149.3 60.7,-149.5 60.7))&format=json&max=1000'
	#zip_url = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/NED/2/IMG/n61w150.zip'
	availability_url = 'https://www.sciencebase.gov/catalog/*'
	zip_url = 'ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/*'

	url_files = {
		availability_url: 'usgs/ned/get_raster_test_availability.json',
		zip_url: 'n61w150.zip',
	}

	test_file = test_util.get_test_file_path('usgs/ned/USGS_NED_2_n61w150_IMG.img')
	with test_util.temp_dir() as data_dir:
		#with test_util.mocked_urls(url_files):
		locs = ulmo.usgs.ned.get_raster(layer, bbox, path=data_dir)
		raster_tile = locs['features'][0]['properties']['file']
		assert filecmp.cmp(raster_tile, test_file)
