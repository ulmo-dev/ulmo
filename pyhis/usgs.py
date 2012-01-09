import cStringIO as StringIO
from datetime import datetime as dt, timedelta as td
import logging
from urllib import urlencode

import isodate
from lxml.etree import iterparse
import pytz
import requests
from sqlalchemy import and_
from sqlalchemy.orm import exc as sa_exc
from sqlalchemy.sql.expression import desc, func

import pyhis.cache as c
from pyhis import usgs_cache as uc

INSTANTANEOUS_URL = "http://waterservices.usgs.gov/nwis/iv?"
DAILY_URL = "http://waterservices.usgs.gov/nwis/dv?"
NS = "{http://www.cuahsi.org/waterML/1.1/}"

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


def get_sites(state_code, site_type=None, service="daily",
              use_cache=True):
    """returns a dict containing site code and site names; currently
    only supports queries by state_code
    """
    url = _get_service_url(service)

    if use_cache:
        log.debug(
            'checking cache for sites: %s {state_code: %s, site_type: %s}' %
            (url, state_code, site_type))
        sites = get_sites_from_cache(url, state_code, site_type)
    else:
        site_elements = get_sites_from_web_service(url, state_code, site_type)
        sites = dict([(key, source_info.find(NS + "siteCode").text)
                      for key, source_info in site_elements])

    return sites


def get_sites_from_web_service(url, state_code, site_type=None):
    """returns a dict containing site code and sourceInfo elements,
    fetches from USGS waterml service
    """
    url_params = {'format': 'waterml,1.1',
                  'stateCd': state_code}

    if site_type:
        url_params['siteType'] = site_type

    url += urlencode(url_params)

    log.info('making request for sites: %s' % url)
    req = requests.get(url)
    content_io = StringIO.StringIO(str(req.content))

    return dict(set([(ele.find(NS + "siteCode").text, ele)
                     for (event, ele) in iterparse(content_io)
                     if ele.tag == NS + "sourceInfo"]))


def get_sites_from_cache(url, state_code, site_type=None):
    """returns a sites dict by checking the cache"""
    service = c.query_or_new(c.db_session, uc.USGSService,
                           dict(url=url))
    cached_sites = c.db_session.query(uc.USGSSite)\
        .filter_by(service=service).all()

    if cached_sites:
        sites = dict([(cached_site.code, cached_site.name)
                      for cached_site in cached_sites])
    else:
        site_elements = get_sites_from_web_service(url, state_code, site_type)
        cache_sites(site_elements, service)
        sites = dict([(k, v.find(NS + 'siteName').text)
                      for k, v in site_elements.items()])

    return sites


def cache_sites(site_elements, service):
    """update cache to include sites"""
    for source_info in site_elements.values():
        site = uc.USGSSite(
            service=service, **site_dict_from_element(source_info))
        c.db_session.add(site)
    c.db_session.commit()


def get_site_data(site_code, parameter_code=None, date_range=None,
                  service="daily", use_cache=True):
    """returns a dict of  data for a site"""
    url = _get_service_url(service)

    if use_cache:
        log.debug(
            'checking cache for site data: %s' % site_code)
        data_dict = get_site_data_from_cache(url, site_code, parameter_code,
                                             date_range)
    if not use_cache or not data_dict:
        data_dict = get_site_data_from_web_service(
            url, site_code, parameter_code, date_range)

    return data_dict


def _get_cached_timeseries_list(url, site_code, parameter_code=None):
    service = c.query_or_new(c.db_session, uc.USGSService, dict(url=url))
    try:
        site = c.db_session.query(uc.USGSSite)\
            .filter_by(service=service, code=site_code).one()

    except sa_exc.NoResultFound:
        return

    if parameter_code:
        try:
            variable = c.db_session.query(uc.USGSVariable)\
                .filter_by(code=parameter_code, network=site.network).one()
            ts_list = [site.timeseries.filter_by(variable=variable).one()]
        except sa_exc.NoResultFound:
            return
    else:
        ts_list = site.timeseries.all()

    return ts_list


def get_site_data_from_cache(url, site_code, parameter_code=None,
                             date_range=None):
    ts_list = _get_cached_timeseries_list(url, site_code, parameter_code)

    date_range_clause = None
    if type(date_range) is dt:
        date_range_clause = (uc.USGSValue.datetime_utc >= date_range)
    elif type(date_range) is list or type(date_range) is tuple:
        date_range_clause = and_(uc.USGSValue.datetime_utc >= date_range[0],
                                 uc.USGSValue.datetime_utc <= date_range[1])
    elif type(date_range) is td:
        current_time = c.db_session.execute(func.now()).scalar()
        time_ago = current_time - date_range
        date_range_clause = (uc.USGSValue.datetime_utc >= time_ago)

    def values_query(values):
        if date_range_clause or date_range == 'all':
            return values.filter(date_range_clause).all()
        else:
            val = values.order_by(desc(uc.USGSValue.datetime_utc)).first()
            if val:
                return [val]
            else:
                return []

    return dict([(ts.variable.code,
                  [dict(datetime_utc=value.datetime_utc,
                        value=value.value,
                        qualifiers=value.qualifiers)
                   for value in values_query(ts.values)])
                 for ts in ts_list])


def get_site_data_from_web_service(url, site_code, parameter_code=None,
                                   date_range=None):
    url_params = {'format': 'waterml,1.1',
                  'site': site_code}
    if parameter_code:
        url_params['parameterCd'] = parameter_code

    url_params.update(date_range_url_params(date_range, url))

    url += urlencode(url_params)

    log.info('making request for site data: %s' % url)
    req = requests.get(url)
    content_io = StringIO.StringIO(str(req.content))

    return parse_site_data_from_waterml(content_io, url)


def parse_site_data_from_waterml(content_io, url, cache_values=True):
    data_dict = {}
    if cache_values:
        service = c.query_or_new(c.db_session, uc.USGSService, dict(url=url))

    for (event, ele) in iterparse(content_io):
        if ele.tag == NS + "timeSeries":
            values_element = ele.find(NS + 'values')
            values = values_from_element(values_element)
            var_element = ele.find(NS + 'variable')
            code = var_element.find(NS + 'variableCode').text
            data_dict[code] = values
            if cache_values:
                source_info_element = ele.find(NS + 'sourceInfo')
                site = c.query_or_new(
                    c.db_session, uc.USGSSite,
                    dict(site_dict_from_element(source_info_element).items() + [('service_id', service.id)]))
                variable = c.query_or_new(
                    c.db_session, uc.USGSVariable,
                    variable_dict_from_element(var_element))
                timeseries = c.query_or_new(
                    c.db_session, uc.USGSTimeSeries,
                    {'variable': variable, 'site': site})
                bulk_upsert_values(values, timeseries)
    return data_dict


def _get_service_url(service):
    if service in ('daily', 'dv'):
        return DAILY_URL
    elif service in ('instantaneous', 'iv'):
        return INSTANTANEOUS_URL
    else:
        raise "service must be either 'daily' ('dv') or 'instantaneous' ('iv')"


def date_range_url_params(date_range, url):
    if date_range is None:
        return {}
    if type(date_range) is dt:
        return dict(startDT=isodate.datetime_isoformat(date_range))
    if type(date_range) is list or type(date_range) is tuple:
        return dict(startDT=isodate.datetime_isoformat(date_range[0]),
                    endDT=isodate.datetime_isoformat(date_range[1]))
    if type(date_range) is td:
        return dict(duration=isodate.duration_isoformat(date_range))
    if date_range == 'all' and 'iv' in url:
        return dict(period=isodate.duration_isoformat(td(days=120)))
    if date_range == 'all' and 'dv' in url:
        return dict(startDT=isodate.datetime_isoformat(dt(1851, 1, 1)))

    raise(TypeError,
          "date_range must be either a datetime, a 2-tuple of "
          "datetimes, a timedelta object, or 'all'")


def site_dict_from_element(source_info_element):
    code = source_info_element.find(NS + 'siteCode')
    site_properties = dict([
        (site_prop.attrib['name'], site_prop.text)
        for site_prop in source_info_element.findall(NS + 'siteProperty')])

    return {
        'name': source_info_element.find(NS + 'siteName').text,
        'code': code.text,
        'network': code.attrib['network'],
        'agency': code.attrib['agencyCode'],
        'latitude': source_info_element.find(
            '%(ns)sgeoLocation/%(ns)sgeogLocation/%(ns)slatitude' % {'ns': NS}).text,
        'longitude': source_info_element.find(
            '%(ns)sgeoLocation/%(ns)sgeogLocation/%(ns)slongitude' % {'ns': NS}).text,
        'site_type': site_properties['siteTypeCd'],
        'huc': site_properties['hucCd'],
        'state': site_properties['stateCd'],
        'county': site_properties['countyCd'],
        }


def variable_dict_from_element(variable_element):
    code = variable_element.find(NS + 'variableCode')
    variable_code = code.text
    variable_name = variable_element.find(NS + 'variableName').text
    variable_description = variable_element.find(NS + 'variableDescription').text
    option = variable_element.find('%(ns)soptions/%(ns)soption' % {'ns': NS})

    if option is not None:
        variable_code += ':' + option.attrib['optionCode']
        if option.text:
            variable_name = option.text + ' ' + variable_name
            variable_description = option.text + ' ' + variable_description

    return {
        'name': variable_name,
        'code': variable_code,
        'network': code.attrib['network'],
        'vocabulary': code.attrib['vocabulary'],
        'description': variable_description,
        'type': variable_element.find(NS + 'valueType').text,
        'unit': variable_element.find('%(ns)sunit/%(ns)sunitCode' % {'ns': NS}).text,
        'no_data_value': variable_element.find(NS + 'noDataValue').text,
        }


def values_from_element(values_element):
    def parse_datetime(datetime_str):
        datetime = isodate.parse_datetime(datetime_str)
        if datetime.tzinfo is not None:
            return datetime.astimezone(tz=pytz.utc).replace(tzinfo=None)
        else:
            return datetime

    return [{'datetime_utc': parse_datetime(value.attrib['dateTime']),
             'value': value.text,
             'qualifiers': value.attrib['qualifiers']}
            for value in values_element.findall(NS + 'value')]


def bulk_upsert_values(value_dicts, timeseries):
    """inserts/updates values"""
    db_values = c.db_session.query(uc.USGSValue)\
        .filter_by(timeseries=timeseries).all()

    db_value_dict = dict([
            (db_value.datetime_utc, (db_value.value, db_value.qualifiers))
            for db_value in db_values])
    insert_dicts = tuple(
        [dict(value_dict.items() + [('timeseries_id', timeseries.id)])
         for value_dict in value_dicts
         if value_dict['datetime_utc'] not in db_value_dict])
    update_dicts = tuple(
        [dict(value_dict.items() + [('timeseries_id', timeseries.id)])
         for value_dict in value_dicts
         if value_dict['datetime_utc'] in db_value_dict \
             and not db_value_dict[value_dict['datetime_utc']] == \
             (value_dict['value'], value_dict['qualifiers'])])

    if insert_dicts:
        uc.USGSValue.__table__.insert(bind=c.db_session.bind)\
            .execute(insert_dicts)
    for update_dict in update_dicts:
        uc.USGSValue.__table__.update()\
            .where(and_(
                uc.USGSValue.datetime_utc == update_dict['datetime_utc'],
                uc.USGSValue.timeseries_id == update_dict['timeseries_id']))\
            .values(update_dict).execute()

    c.db_session.commit()


def cache_all_sites(state_code, service):
    sites = get_sites(state_code, service=service)

    for site_code in sites.keys():
        update_site_cache(site_code, service)


def update_site_cache(site_code, service):
    url = _get_service_url(service)
    ts_list = _get_cached_timeseries_list(url, site_code)
    if not ts_list:
        site_data = get_site_data(site_code, service=service, date_range='all')

    for ts in ts_list:
        if ts.values.count() == 0:
            site_data = get_site_data(site_code, service=service, date_range='all')
        else:
            #XXX: do update stuff here
            pass
