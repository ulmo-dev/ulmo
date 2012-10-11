from ulmo.waterml import common

WATERML_V1_0_NAMESPACE= "{http://www.cuahsi.org/waterML/1.0/}"


def parse_sites(content_io):
    """parses sites out of a waterml file; content_io should be a file-like object"""
    return common.parse_sites(content_io, WATERML_V1_0_NAMESPACE, site_info_name='siteInfo')
