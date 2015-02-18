# -*- coding: utf-8 -*-
"""

    ulmo.noaa.estuarine_bathymetry.core
    ~~~~~~~~~~~~~~~~~~~~~

    This module provides access to data provided by the `NOAA Estuaring Bathymetry
    Data Sets`_ web site.

Created on Mon Feb 02 15:00:04 2015

@author: RDITLANM
"""


from bs4 import BeautifulSoup
from geojson import Feature, FeatureCollection
from ulmo import util
import fiona
import logging
import os
import requests
import ulmo
import zipfile

NOAA_BATHYMETRY_BASE_URL = 'http://estuarinebathymetry.noaa.gov/%s'
NOAA_BATHYMETRY_DATA_URL = 'http://estuarinebathymetry.noaa.gov/finddata.html'

dem_format_dict = {
        '1 arc-second': '_B30.zip',
        '3 arc-second': '_B90.zip',
    }

# configure logging
LOG_FORMAT = '%(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_data_locations(path):
  
     url_region_dict = _fetch_region_url()
    
     bathymetry_estuary_list = []      
     features = []
 
     if (os.path.exists(path)): 
   
         for regionKey in url_region_dict:
             url = NOAA_BATHYMETRY_BASE_URL % url_region_dict[regionKey]
             temp_estuary_list = _fetch_url(url, regionKey)
             count = 0
             for estuary in temp_estuary_list:
                 bathymetry_estuary_list.append(estuary)
                 count+=1
                 #print estuary['text'], estuary['zip_url'] #estuary['href'], estuary['region'], estuary['id']
                 print '... downloading %s estuary shapefile archive %s of %s from %s' % (estuary['region'], count, len(temp_estuary_list), estuary['zip_url'])

                 # retrieve zip file name portion from the zip file url
                 filename = os.path.split(estuary['zip_url'])[-1]  
                
                 zip_path = os.path.join(path, 'zip', filename)
                 
                 # download zip archive from the NOAA estuarine bathymetry site
                 util.misc.download_if_new(estuary['zip_url'], zip_path, check_modified=True)    
                 
         count = 0  
         for estuary in bathymetry_estuary_list:
            count+=1
            # check to see if the zip path is a valid file format
            # if the zip path is valid, read the shape file from the zip archive
            if (zipfile.is_zipfile(zip_path) and os.path.exists(zip_path)):  
                print '... reading estuary shapefile archive %s of %s - (%s)' % (count, len(bathymetry_estuary_list), zip_path)
                feature = _read_shape_zipfile(estuary['id'], zip_path)
                features.append(feature)
            else:
                print '%s is not a valid zip file!' % zip_path
  
     else:
         print '%s does not exist' % path  
  
     return FeatureCollection(features)
    
def get_data(estuary_id, path, dem_format):  

    if (os.path.exists(path)):   
       
       if (dem_format in dem_format_dict.keys()):
        
           dem_format_value = dem_format_dict.get(dem_format)
           zip_url = estuary_id + '/' + estuary_id + dem_format_value
     
           dem_zip_url = NOAA_BATHYMETRY_BASE_URL % zip_url
           
           # retrieve zip file name portion from the zip file url
           filename = os.path.split(dem_zip_url)[-1]  
          
           zip_path = os.path.join(path, 'zip_dem', filename)
           
           util.misc.download_if_new(dem_zip_url, zip_path, check_modified=True)

       else:
           print 'The following dem formats are supported 1 arc-second or 3 arc-second, not %s' % dem_format
     
    else:
        print 'The following path does not exist: %s' % path        
     
def _read_shape_zipfile(estuary_id, zip_path):
    
    with fiona.open('/', vfs='zip://%s' % zip_path) as c:
         f = next(c)
         #print f['geometry']['type']
         #print f['properties']
         
         feature = Feature(geometry=f['geometry'], id=estuary_id, 
                   properties=f['properties']) 
        
    return feature      
    
def _fetch_url(url, region):
    
    """
    This function uses the Beautiful Soup module to parse the estuaries info (name, url link page) 
    from a particular region that NOAA has screated.

    url : str, 
        This parameter represents the url for a particular region that NOAA has screated. 

    region : str,
        This parameter represents a particular region that has an estuary. 
    """

    r = requests.get(url)
    
    if r.status_code == 200:    
        
        log.info('data requested using url: %s\n' % r.url)
        soup = BeautifulSoup(r.text)
        message = soup.find('form').select('p > a')

        bathymetry_estuaries = []
        url_dict = {}    
    
        for text in message:
            
            temp_text = text.get_text().split(" ")
            code = temp_text[len(temp_text) - 1].replace("(","").replace(")","")
            zip_url = NOAA_BATHYMETRY_BASE_URL % (code + '/' + code + '_extent.zip')            
            
            url_dict = { 'href' : text.get('href'), 
                         'text' : text.get_text(), 
                         'region' : region, 
                         'id' : code, 
                         'zip_url' : zip_url }

            bathymetry_estuaries.append(url_dict)
    
        if not message:
            log.info('No data found\n')
            bathymetry_estuaries = []
    else:
        log.info('could not connect using url: %s, status code =%s\n' % (r.url, r.status_code))
     
    return bathymetry_estuaries

def _fetch_region_url():
    r = requests.get(NOAA_BATHYMETRY_DATA_URL)
    
    url_region_dict = {}     
    
    if r.status_code == 200:
        
        log.info('data requested using url: %s\n' % r.url)
        soup = BeautifulSoup(r.text)
        message = soup.find('p', class_="smalltext").select('a')

        for text in message:            
            temp_text = text.get_text().strip()            

            if "\n" in temp_text:
                temp_text = temp_text.split("\r\n")
                temp_text = temp_text[0].strip() + " " + temp_text[1].strip()
                
            url_region_dict[temp_text] = text.get('href')

    else:
         log.info('could not connect using url: %s, status code =%s\n' % (r.url, r.status_code))   
    
    return url_region_dict   
