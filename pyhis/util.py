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


def _get_pyhis_dir():
    return_dir = appdirs.user_data_dir('pyhis', 'pyhis')
    _mkdir_if_doesnt_exist(return_dir)
    return return_dir


def _mkdir_if_doesnt_exist(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
