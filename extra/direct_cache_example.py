
from datetime import datetime

import pandas
import pyhis

CACHE_FILE = '/home/wilsaj/tpwd_pyhis_cache.db'

pyhis.cache.init_cache(CACHE_FILE)

from pyhis.cache import *


def get_values(variable_name, begin_date, end_date):
    variable = db_session.query(DBVariable).filter_by(name=variable_name).first()

    variable_timeseries = db_session.query(DBTimeSeries).filter_by(variable=variable).all()

    site_list = ((ts.site.name, values_in_range(ts, begin_date, end_date))
                 for ts in variable_timeseries)

    site_list = [site_tuple for site_tuple in site_list if site_tuple[1] != None]
    site_dict = dict(site_list)
    
    return site_dict


def values_in_range(ts, begin_date, end_date):
    db_values = ts.values.filter(begin_date < DBValue.timestamp ).filter(DBValue.timestamp < end_date).all()
    if not len(db_values):
        return None

    dates = [db_value.timestamp for db_value in db_values]
    value_list = [db_value.value for db_value in db_values]
    return pandas.Series(value_list, index=dates)


if __name__ == '__main__':
    site_dict = get_values('Salinity', datetime(1900, 12, 15), datetime(2001, 1, 10))
    import pdb; pdb.set_trace()





# how to use:
#sites_in_poly {'blasite': <PyhisSite>,
#               ...}

#lots_of_values = get_values('Salinity', yesterday, today)
# lots_of_values = {'blasite': PandasSeries,
#                   ...}
               


