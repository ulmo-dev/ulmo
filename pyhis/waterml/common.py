from lxml import etree




def parse_sites(content_io, namespace, site_info_name):
    """parses sites out of a waterml file; content_io should be a file-like object"""
    site_elements = dict(set([(ele.find(namespace + "siteCode").text, ele)
                    for (event, ele) in etree.iterparse(content_io)
                    if ele.tag == namespace + site_info_name]))
    sites = dict([(key, parse_site_info(source_info))
                    for key, source_info in site_elements.iteritems()])
    return sites
