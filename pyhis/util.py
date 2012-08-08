"""
   pyhis.util
   ~~~~~~~~~~

   Collection of useful functions for common use cases
"""
import os

import appdirs
import pandas

import pyhis


#http://midgewater.twdb.state.tx.us/tpwd/soap/wateroneflow.wsdl
#http://midgewater.twdb.state.tx.us/tceq/soap/wateroneflow.wsdl
#http://midgewater.twdb.state.tx.us/cbi/soap/wateroneflow.wsdl


def get_default_h5file():
    default_dir = get_pyhis_dir()
    return os.path.join(default_dir, "pyhis.h5")


def get_pyhis_dir():
    return_dir = appdirs.user_data_dir('pyhis', 'pyhis')
    _mkdir_if_doesnt_exist(return_dir)
    return return_dir


def get_parameter_within_polygon(wsdl_list, param_code_list, verts, merge='BySource'):
    """given a list of service wsdl urls and list of service specific
    param codes and a list of polygon vertices returns pandas.DataFrame of data.
    optional flags
        merge = False : Each site timeseries is a column in dataframe
        merge = 'BySource' : each column in dataframe corresponds to a service
        merge = True : single pandas.timeseries

    Note: merging averages across values that occur at the same timestamp.
    """

    dataframe = pandas.DataFrame()
    for wsdl_url, param_code in zip(wsdl_list, param_code_list):
        source = pyhis.Source(wsdl_url)
        sites = source.get_sites_within_polygon(verts)
        ts_dict = {}
        for site in sites:
            if param_code in sites.timeseries:
                ts_dict[''.join((ts.site.network,':',ts.site.code))] = ts.data
                #ts_list.append(site.timeseries[param_code])
        pd = pandas.Dataset(ts_dict)
        if merge.lower()=='BySource':
            pd = pandas.DataSet({site.network:pd.mean(axis=1)})
        dataframe.append(pd)

    if merge is True:
        dataframe = dataframe.mean(axis=1)

    return dataframe


def get_or_create_group(h5file, path, title):
    return _get_or_create_node('createGroup', h5file, path, title)


def get_or_create_table(h5file, path, table_definition, title):
    return _get_or_create_node('createTable', h5file, path, table_definition,
            title)


def _get_or_create_node(method_name, h5file, path, *args, **kwargs):
    try:
        node = h5file.getNode(path)
    except NoSuchNodeError:
        where, name = path.rsplit('/', 1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            create_method = getattr(h5file, method_name)
            node = create_method(*args, **kwargs)
    return node


def _mkdir_if_doesnt_exist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

