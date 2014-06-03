import pytest
import ulmo
import test_util


test_sets = [
	{'layer': '1 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	},
	{'layer': '1/3 arc-second',
	 'bbox': (-79.68433821243661, 32.81417227179455, -77.42742156945509, 34.798064728936754),
	},
	{'layer': 'Alaska 2 arc-second',
	 'bbox': (-150.4969, 60.7338, -148.4600, 61.5253),
	},
]

def test_get_tile_urls_local():
	# note: there it looks like ymax is rounded up when greater than .98 
	# at that point some extra tiles are downloaded. Ignoring this issue 
	# for now since all the required tiles are being downloaded.
	# note: 2 arc-second coverage is Alaska only
	for dataset in test_sets:
		urls_from_webservice = ulmo.usgs.ned.get_tile_urls(
			dataset['layer'], 
			*dataset['bbox'], 
			use_webservice=True)
		urls_from_local = ulmo.usgs.ned.get_tile_urls(
			dataset['layer'], 
			*dataset['bbox'], 
			use_webservice=False)

		assert set(urls_from_webservice) == set(urls_from_local)