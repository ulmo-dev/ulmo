from ulmo.waterml import common

WATERML_V1_1_NAMESPACE = "{http://www.cuahsi.org/waterML/1.1/}"


def parse_site_infos(content_io):
    """parses site_infos out of a waterml file; content_io should be a file-like object"""
    return common.parse_site_infos(
        content_io, WATERML_V1_1_NAMESPACE, site_info_names=['siteInfo', 'sourceInfo'])


def parse_site_values(content_io, query_isodate=None, methods=None):
    """parses values out of a waterml file; content_io should be a file-like object"""
    return common.parse_site_values(
        content_io, WATERML_V1_1_NAMESPACE, query_isodate=query_isodate,
        methods=methods)


def parse_sites(content_io):
    """parses sites out of a waterml file; content_io should be a file-like object"""
    return common.parse_sites(content_io, WATERML_V1_1_NAMESPACE)


def parse_variables(content_io):
    """parses variables out of a waterml file; content_io should be a file-like object"""
    return common.parse_variables(content_io, WATERML_V1_1_NAMESPACE)
