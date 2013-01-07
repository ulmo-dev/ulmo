from ulmo.waterml import common

WATERML_V1_1_NAMESPACE = "{http://www.cuahsi.org/waterML/1.1/}"


def parse_site_infos(content_io):
    """parses site_infos out of a waterml file; content_io should be a file-like object"""
    return common.parse_site_infos(
        content_io, WATERML_V1_1_NAMESPACE, site_info_names=['siteInfo', 'sourceInfo'])


def parse_site_values(content_io, query_isodate):
    return common.parse_site_values(
        content_io, WATERML_V1_1_NAMESPACE, query_isodate)
