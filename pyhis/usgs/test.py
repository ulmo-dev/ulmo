from __future__ import absolute_import
import pyhis

if __name__ == '__main__':
    pyhis.usgs.pytables.init_h5()
    pyhis.usgs.pytables.update_site_list('RI')
    sites = pyhis.usgs.pytables.get_sites()
    for site in sites:
        pyhis.usgs.pytables.update_site_data(site)
    #site = get_site_data('01116300')
    #import pdb; pdb.set_trace()
    pass


