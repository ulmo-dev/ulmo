"""
Example script that returns a list of USGS gages within Travis county area whose discharge is below
20th percentile.
"""

#Initialize pyhis
import pyhis

#Initialize some other python modules for plotting etc
import matplotlib.pyplot as plt

# Connect to the USGS NWIS Unit values and Daily values data services.
# The daily values service will be used to calculate historical percentiles
# and the unit values service provides 15 mn data

nwis_dv = pyhis.Service('http://river.sdsc.edu/wateroneflow/NWIS/DailyValues.asmx?WSDL')
nwis_uv = pyhis.Service('http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL')

# get sites within Travis county
travis_sites = nwis_uv.get_sites_within_shapefile('travis_county.shp')

# target percentile (this could be made into a input parameter)
target_percentile = 0.2 #(i.e. 20%)

# start with an empty list
list_of_critical_gages = [] 

# loop through the sites in Travis County
for site in travis_sites:
    print 'processing site: ', site
    #check if there is discharge data atthis site
    if '00060' in nwis_uv.sites[site].timeseries:
        print 'Discharge data available'
        # calculate the target quantile from historical daily value data
        threshold = nwis_dv.sites[site].timeseries['00060/DataType=Average'].data.quantile(target_percentile)
        print 'threshold value: ' , threshold
        
        
        #if the latest downloaded data is below threshold then add to list of critical gages
        if nwis_uv.sites[site].timeseries['00060'].data[-1] < threshold:
            print 'adding gage to critical gage list: ', site
            list_of_critical_gages.append(nwis_uv.sites[site])
        

#plot discharg at the critical gages
plt.figure()
for gage in list_of_critical_gages:
    gage.timeseries['00060'].data.plot(label=gage.name)

plt.legend()
plt.ylabel = 'Discharge (cfs)'
plt.title('Critical Gages in Travis County')
plt.savefig('travis_county_critical_gages.png')

