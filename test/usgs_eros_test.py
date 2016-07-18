import pytest
import ulmo
import test_util
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


def test_get_available_format():
    with test_util.mocked_urls('usgs/eros/formats_l1l.json'):
        formats = ulmo.usgs.eros.get_available_formats('L1L')
        assert len(formats) == 1


test_sets = [
    #{'product_key': 'LC6',
    # 'bbox': (-78, 32, -76, 36),
    # 'number_of_tiles': 5,
    #'fmt_file': 'usgs/eros/formats_l1l.json',
    #'file': 'usgs/eros/availability_bbox_test_set_1.json',
    #},
]


def test_get_raster_availability():
    for dataset in test_sets:
        #file_urls = {
        #    'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx/return_Download_Options': dataset['fmt_file'],
        #    'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp?TOP=36.0&BOTTOM=32.0&LEFT=-78.0&RIGHT=-76.0&LAYER_IDS=L1L02&JSON=true': dataset['file'],
        #}
        #with test_util.mocked_urls(file_urls):
        locs = ulmo.usgs.eros.get_raster_availability(dataset['product_key'], dataset['bbox'])
        assert len(locs['features'])==dataset['number_of_tiles']


def test_get_raster():
    product_key = 'NCP'
    bbox = (-97.992, 31.991, -97.991, 31.992)
    #availability_url = 'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp?TOP=31.992&BOTTOM=31.991&LEFT=-97.992&RIGHT=-97.991&LAYER_IDS=NCP&JSON=true'
    #jp2_url = 'http://tdds2.cr.usgs.gov/lta5/ortho/naip/compressed/TX/2012/201204_texas_naip_1x0000m_cnir/31097/m_3109701_nw_14_1_20120725_20121015.jp2'
    format_url = 'http://nimbus.cr.usgs.gov/index_service/Index_Service_JSON2.asmx'
    availability_url = 'http://extract.cr.usgs.gov/requestValidationServiceClient/sampleRequestValidationServiceProxy/getTiledDataDirectURLs2.jsp'
    jp2_url = 'http://tdds2.cr.usgs.gov/lta5/ortho/naip/compressed/TX/2012/201204_texas_naip_1x0000m_cnir/31097/m_3109701_nw_14_1_20120725_20121015.jp2'
    url_files = {
        format_url: 'usgs/eros/formats_ncp.json',
        availability_url: 'usgs/eros/get_raster_test_availability.json',
        jp2_url: 'usgs/eros/m_3109701_nw_14_1_20120725_20121015.jp2',
    }

    test_file = test_util.get_test_file_path('usgs/eros/m_3109701_nw_14_1_20120725_20121015.jp2')
    with test_util.temp_dir() as data_dir:
        with test_util.mocked_urls(url_files):
            locs = ulmo.usgs.eros.get_raster(product_key, bbox, path=data_dir)
            raster_tile = locs['features'][0]['properties']['file']
            assert filecmp.cmp(raster_tile, test_file)
