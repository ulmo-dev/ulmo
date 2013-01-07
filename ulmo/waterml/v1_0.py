from ulmo.waterml import common

WATERML_V1_0_NAMESPACE= "{http://www.cuahsi.org/waterML/1.0/}"


def parse_site_infos(content_io):
    """parses site_infos out of a waterml file; content_io should be a file-like object"""
    return common.parse_site_infos(content_io, WATERML_V1_0_NAMESPACE,
            site_info_names=['siteInfo'])
