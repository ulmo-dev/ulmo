import isodate

from lxml import etree
from past.builtins import basestring

from ulmo import util


def parse_site_values(content_io, namespace, query_isodate=None, methods=None):
    """parses values out of a waterml file; content_io should be a file-like object"""
    data_dict = {}
    metadata_elements = [
        # (element name, name of collection,
        #   key from element dict to use as for a key in the collections dict)
        ('censorCode', 'censor_codes', 'censor_code'),
        ('method', 'methods', 'id'),
        ('offset', 'offsets', 'id'),
        ('qualifier', 'qualifiers', 'id'),
        ('qualityControlLevel', 'quality_control_levels', 'id'),
        ('source', 'sources', 'id')
    ]
    for (event, ele) in etree.iterparse(content_io):
        if ele.tag == namespace + "timeSeries":
            source_info_element = ele.find(namespace + 'sourceInfo')
            site_info = _parse_site_info(source_info_element, namespace)
            var_element = ele.find(namespace + 'variable')
            variable = _parse_variable(var_element, namespace)
            values_elements = ele.findall(namespace + 'values')
            code = variable['code']
            if isinstance(methods, basestring):
                method = methods
            elif isinstance(methods, dict):
                method = methods.get(code, None)
            else:
                method = None
            if 'statistic' in variable:
                code += ":" + variable['statistic']['code']

            if method is None:
                if len(values_elements) > 1:
                    raise ValueError(
                        'found more than one method for %s. need to specify'
                        'specify code or "all".' % variable['code'])
                values_element = values_elements[0]
                values = _parse_values(values_element, namespace)
                data_dict[code] = {
                    'site': site_info,
                    'variable': variable,
                }
                data_dict[code].update({'values': values})
                metadata = _parse_metadata(
                        values_element, metadata_elements, namespace)
                data_dict[code].update(metadata)
                if query_isodate:
                    data_dict[code]['last_refresh'] = query_isodate
            elif method == 'all':
                for values_element in values_elements:
                    values = _parse_values(values_element, namespace)
                    metadata = _parse_metadata(
                            values_element, metadata_elements, namespace)
                    if len(values_elements) > 1:
                        updated_code = code + ':' + str(
                            list(metadata['methods'].values())[0]['id'])
                    else:
                        updated_code = code
                    data_dict[updated_code] = {
                        'site': site_info.copy(),
                        'variable': variable,
                    }
                    data_dict[updated_code].update({'values': values})
                    data_dict[updated_code].update(metadata)
                    if query_isodate:
                        data_dict[updated_code]['last_refresh'] = query_isodate
            else:
                for values_element in values_elements:
                    if values_element.find(
                            namespace + 'method[@methodID="%s"]' % method)\
                            is not None:
                        values = _parse_values(values_element, namespace)
                        metadata = _parse_metadata(
                            values_element, metadata_elements, namespace)
                        data_dict[code] = {
                            'site': site_info,
                            'variable': variable,
                        }
                        data_dict[code].update({'values': values})
                        data_dict[code].update(metadata)
                        if query_isodate:
                            data_dict[code]['last_refresh'] = query_isodate

    return data_dict


def parse_site_infos(content_io, namespace, site_info_names):
    """parses information contained in site info elements out of a waterml file;
    content_io should be a file-like object
    """
    site_infos = {}
    for site_info_name in site_info_names:
        content_io.seek(0)
        site_info_elements = [
            element
            for (event, element) in etree.iterparse(content_io)
            if element.tag == namespace + site_info_name
        ]
        site_info_dicts = [
            _parse_site_info(site_info_element, namespace)
            for site_info_element in site_info_elements
        ]
        site_infos.update(dict([(d['code'], d) for d in site_info_dicts]))
    return site_infos


def parse_sites(content_io, namespace):
    """parses information contained in site elements (including seriesCatalogs)
    out of a waterml file; content_io should be a file-like object
    """
    content_io.seek(0)
    site_elements = [
        ele for (event, ele) in etree.iterparse(content_io)
        if ele.tag == namespace + 'site']
    site_dicts = [
        _parse_site(site_element, namespace)
        for site_element in site_elements]
    sites = dict(
        [(site_dict['code'], site_dict)
         for site_dict in site_dicts])
    return sites


def parse_variables(content_io, namespace):
    """parses information contained in variables elements out of a waterml file;
    content_io should be a file-like object
    """
    content_io.seek(0)
    variable_elements = [
        element
        for (event, element) in etree.iterparse(content_io)
        if element.tag == namespace + 'variable'
    ]
    variable_dicts = [
        _parse_variable(variable_element, namespace)
        for variable_element in variable_elements
    ]
    variables = dict([
        (variable_dict['code'], variable_dict)
        for variable_dict in variable_dicts
    ])
    return variables


def _element_dict(element, exclude_children=None, prepend_attributes=True):
    """converts an element to a dict representation with CamelCase tag names and
    attributes converted to underscores; this is a generic converter for cases
    where special parsing isn't necessary.  In most cases you will want to
    update with this dict. If prepend_element_name is True (default), then
    attributes and children will be prepended with the parent element's tag
    name.

    Note: does not handle sibling elements
    """
    if element is None:
        return {}

    if exclude_children is None:
        exclude_children = []

    element_dict = {}
    element_name = util.camel_to_underscore(element.tag.split('}')[-1])

    if len(element) == 0 and not element.text is None:
        element_dict[element_name] = element.text

    element_dict.update(dict([
        (_element_dict_attribute_name(key, element_name,
            prepend_element_name=prepend_attributes), value)
        for key, value in element.attrib.items()
        if value.split(':')[0] not in ['xsd', 'xsi']
    ]))

    for child in element.iterchildren():
        if not child.tag.split('}')[-1] in exclude_children:
            element_dict.update(_element_dict(child))

    return element_dict


def _element_dict_attribute_name(attribute_name, element_name,
        prepend_element_name=True):
    attribute_only = util.camel_to_underscore(attribute_name.split('}')[-1])
    if attribute_only.startswith(element_name) or not prepend_element_name:
        return attribute_only
    else:
        return element_name + '_' + attribute_only


def _find_unit(element, namespace):
    unit_element = element.find(namespace + 'unit')
    if unit_element is None:
        unit_element = element.find(namespace + 'units')
    return unit_element


def _parse_datetime(datetime_str):
    """returns an iso 8601 datetime string; USGS returns fractions of a second
    which are usually all 0s. ISO 8601 does not limit the number of decimal
    places but we have to cut them off at some point
    """
    #XXX: this could be sped up if need be
    #XXX: also, we need to document that we are throwing away fractions of
    #     seconds
    return isodate.datetime_isoformat(isodate.parse_datetime(datetime_str))


def _parse_geog_location(geog_location, namespace):
    """returns a dict representation of a geogLocation etree element"""
    return_dict = {
        'latitude': geog_location.find(namespace + 'latitude').text,
        'longitude': geog_location.find(namespace + 'longitude').text,
    }

    srs = geog_location.attrib.get('srs')
    if not srs is None:
        return_dict['srs'] = srs

    return return_dict


def _parse_metadata(values_element, metadata_elements, namespace):
    metadata = {}
    for tag, collection_name, key in metadata_elements:
        underscored_tag = util.camel_to_underscore(tag)
        collection = [
            _scrub_prefix(_element_dict(element, namespace),
                underscored_tag)
            for element in values_element.findall(namespace + tag)
        ]
        if len([x for x in collection if len(x)]):
            collection_dict = dict([
                (item[key], item)
                for item in collection
                if key in item
            ])
            metadata[collection_name] = collection_dict
    return metadata


def _parse_method(method, namespace):
    return _element_dict(method, namespace, prepend_attributes=False)


def _parse_series(series, namespace):
    include_elements = [
        'method',
        'Method',
        'source',
        'Source',
        'QualityControlLevel',
        'qualityControlLevel',
        'variableTimeInterval',
        'valueCount',
    ]
    series_dict = {}

    variable_element = series.find(namespace + 'variable')
    series_dict['variable'] = _parse_variable(variable_element, namespace)

    for include_element in include_elements:
        element = series.find(namespace + include_element)
        if not element is None:
            name = util.camel_to_underscore(element.tag)
            element_dict = _scrub_prefix(_element_dict(element), name)
            series_dict[name] = element_dict

    return series_dict


def _parse_site(site, namespace):
    """returns a dict representation of a site given an etree object
    representing a site element
    """
    site_dict = _parse_site_info(site.find(namespace + 'siteInfo'), namespace)
    series_elements = site.iter(namespace + 'series')
    site_dict['series'] = [
        _parse_series(series_element, namespace)
        for series_element in series_elements
    ]

    return site_dict


def _parse_site_info(site_info, namespace):
    """returns a dict representation of a site given an etree object
    representing a siteInfo element
    """
    site_code = site_info.find(namespace + "siteCode")

    return_dict = {
        'code': site_code.text,
        'name': site_info.find(namespace + "siteName").text,
        'network': site_code.attrib.get('network'),
    }

    agency = site_code.attrib.get('agencyCode')
    if agency:
        return_dict['agency'] = agency

    geog_location = site_info.find(
        namespace.join(["", "geoLocation/", "geogLocation"]))
    if not geog_location is None:
        return_dict['location'] = _parse_geog_location(geog_location, namespace)

    timezone_info = site_info.find(namespace + "timeZoneInfo")
    if not timezone_info is None:
        return_dict['timezone_info'] = _parse_timezone_info(timezone_info, namespace)

    elevation_m = site_info.find(namespace + 'elevation_m')
    if not elevation_m is None:
        return_dict['elevation_m'] = elevation_m.text

    # WaterML 1.0 notes
    notes = dict([
        (util.camel_to_underscore(note.attrib['title'].replace(' ', '')),
            note.text)
        for note in site_info.findall(namespace + 'note')
    ])
    if notes:
        return_dict['notes'] = notes

    # WaterML 1.1 siteProperties
    site_properties = dict([
        (util.camel_to_underscore(
            site_property.attrib['name'].replace(' ', '')),
        site_property.text)
        for site_property in site_info.findall(namespace + 'siteProperty')
    ])
    if site_properties:
        return_dict['site_property'] = site_properties

    return return_dict


def _parse_timezone_element(timezone_element):
    """returns a dict representation of a timezone etree element (either
    defaultTimeZone or daylightSavingsTimeZone)
    """
    return {
        'abbreviation': timezone_element.attrib.get('zoneAbbreviation'),
        'offset': timezone_element.attrib.get('zoneOffset'),
    }


def _parse_timezone_info(timezone_info, namespace):
    """returns a dict representation of a timeZoneInfo etree element"""
    return_dict = {}

    uses_dst_str = timezone_info.attrib.get('siteUsesDaylightSavingsTime', "false")
    if uses_dst_str == "true":
        return_dict['uses_dst'] = True
    else:
        return_dict['uses_dst'] = False

    dst_element = timezone_info.find(namespace + 'daylightSavingsTimeZone')
    if not dst_element is None:
        return_dict['dst_tz'] = _parse_timezone_element(dst_element)

    return_dict['default_tz'] = _parse_timezone_element(
         timezone_info.find(namespace + 'defaultTimeZone'))

    return return_dict


def _parse_time_info(time_info_element, namespace):
    """returns a dict that represents a parsed WOF 1.0 timeSupport or WOF 1.1
    timeScale element
    """
    return_dict = {}

    is_regular = time_info_element.attrib.get('isRegular')
    if not is_regular is None:
        if is_regular.lower() == 'true':
            is_regular = True
        elif is_regular.lower() == 'false':
            is_regular = False
        return_dict['is_regular'] = is_regular

    if '1.0' in namespace:
        interval_tag = 'timeInterval'
    elif '1.1' in namespace:
        interval_tag = 'timeSupport'

    interval_element = time_info_element.find(namespace + interval_tag)
    if not interval_element is None:
        return_dict['interval'] = interval_element.text

    unit_element = _find_unit(time_info_element, namespace)
    if not unit_element is None:
        return_dict['units'] = _parse_unit(unit_element, namespace)

    return return_dict


def _parse_unit(unit_element, namespace):
    """returns a list of dicts that represent the values for a given unit or
    units element
    """
    unit_dict = _element_dict(unit_element)
    tag_name = unit_element.tag.split('}')[-1]
    return_dict = {}

    if '1.0' in namespace:
        return_dict['name'] = unit_element.text

    keys = [
        'abbreviation',
        'code',
        'name',
        'type',
    ]
    for key in keys:
        dict_key = tag_name + '_' + key
        if dict_key in unit_dict:
            return_dict[key] = unit_dict[dict_key]

    return return_dict


def _parse_value(value_element, namespace):
    value_dict = _element_dict(value_element, prepend_attributes=False)
    datetime = _parse_datetime(value_dict.pop('date_time'))
    value_dict['datetime'] = datetime
    return value_dict


def _parse_values(values_element, namespace):
    """returns a list of dicts that represent the values for a given etree
    values element
    """

    return [
        _parse_value(value, namespace)
        for value in values_element.findall(namespace + 'value')
    ]


def _parse_variable(variable_element, namespace):
    """returns a dict that represents a variable for a given etree variable element"""
    return_dict = _element_dict(variable_element,
        exclude_children=['options', 'timeScale', 'timeSupport', 'unit', 'units',
            'variableCode', 'variableDescription', 'variableName'])
    variable_code = variable_element.find(namespace + 'variableCode')
    return_dict.update({
        'code': variable_code.text,
        'id': variable_code.attrib.get('variableID'),
        'name': variable_element.find(namespace + 'variableName').text,
        'vocabulary': variable_code.attrib.get('vocabulary'),
    })
    network = variable_code.attrib.get('network')
    if network:
        return_dict['network'] = network

    statistic = variable_element.find(namespace + 'options/' + namespace + "option[@name='Statistic']")
    if statistic is not None:
        return_dict['statistic'] = {
            'code': statistic.attrib.get('optionCode'),
            'name': statistic.text,
        }

    if '1.0' in namespace:
        time_info_name = 'timeSupport'
    elif '1.1' in namespace:
        time_info_name = 'timeScale'
    time_info_element = variable_element.find(namespace + time_info_name)
    if not time_info_element is None:
        return_dict['time'] = _parse_time_info(time_info_element, namespace)

    unit_element = _find_unit(variable_element, namespace)
    if not unit_element is None:
        return_dict['units'] = _parse_unit(unit_element, namespace)

    variable_description = variable_element.find(
            namespace + 'variableDescription')
    if not variable_description is None:
        return_dict['description'] = variable_description.text

    return return_dict


def _scrub_prefix(element_dict, prefix):
    "returns a dict with prefix scrubbed from the keys"
    return dict([
        (k.split(prefix + '_')[-1], v)
        for k, v in element_dict.items()
    ])
