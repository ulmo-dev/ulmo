import os
import tempfile

from attest import Assert, Tests, TestBase, test

import pyhis


TWDB_WSDL_URL = 'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL'

#TWDB_WSDL_URL = 'file://' + os.path.abspath('./twdb_wsdl.xml')
USGS_WSDL_URL = 'file://' + os.path.abspath('./usgs_wsdl.xml')

TEST_CACHE_DATABASE_PATH = os.path.join(tempfile.gettempdir(),
                                        'pyhis_test_cache.db')

TEST_SHAPEFILE_PATH = 'shapefiles/pyhis_test.shp'


class TWDBTestBase(TestBase):
    """Base class for using TWDB dataset as a service"""

    @test
    def get_site(self):
        site = self.service.get_site('TWDBSondes', 'Aransas95_D1')
        assert Assert(site.latitude) == 28.06666667
        assert Assert(site.longitude) == -97.20333333
        assert Assert(site.name) == 'Upper Copano Bay'
        assert Assert(site.service.url) == TWDB_WSDL_URL

    @test
    def check_sites(self):
        assert Assert(len(self.service.get_all_sites())) == 74
        assert Assert(len(self.service.sites)) == 74

    @test
    def check_variables(self):
        assert Assert(len(self.service.sites['Aransas95_D1'].timeseries)) == 5
        assert Assert(len(self.service.sites['Christmas92_D1'].timeseries)) == 5

    @test
    def check_dataframe(self):
        df = self.service.sites['Aransas95_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 725
        df = self.service.sites['Christmas92_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 1044


class TWDBFreshCacheTests(TWDBTestBase):
    """Run tests with cache backend"""

    def __context__(self):
        if os.path.exists(TEST_CACHE_DATABASE_PATH):
            os.remove(TEST_CACHE_DATABASE_PATH)
        pyhis.cache.init_cache(TEST_CACHE_DATABASE_PATH)

        self.service = pyhis.Service(
            TWDB_WSDL_URL,
            use_cache=True)
        yield
        del self.service


class TWDBCacheTests(TWDBTestBase):
    """Run tests with cache backend"""

    def __context__(self):
        pyhis.cache.init_cache(TEST_CACHE_DATABASE_PATH)
        self.service = pyhis.Service(
            TWDB_WSDL_URL,
            use_cache=True)
        yield
        del self.service

    @test
    def get_series_and_quantity_check_for_updates(self):
        """
        tests that cache.get_timeseries_dict_for_site()
        actually checks for updates when check_for_updates=True
        """
        from pyhis import cache
        cache_dict = cache._cache

        # query timseries so that it gets set up in the cache
        cached_ts = cache.CacheTimeSeries(
            self.service.sites['Aransas95_D1'].timeseries['CON001'])

        cached_ts.values = cached_ts.values[:4]
        cache.db_session.commit()

        # test that the db has been altered
        del cache._cache['timeseries'][(TWDB_WSDL_URL, 'TWDBSondes',
                                        'Aransas95_D1', 'CON001')]

        # query timseries so that it gets set up in the cache
        cached_ts = cache.CacheTimeSeries(
            self.service.sites['Aransas95_D1'].timeseries['CON001'])
        assert Assert(cached_ts.values.count()) == 4

        # test that check_for_updates sucessfully updates the
        # timeseries values
        del cache._cache['timeseries'][(TWDB_WSDL_URL, 'TWDBSondes',
                                        'Aransas95_D1', 'CON001')]

        test_ts = self.service.sites['Aransas95_D1'].timeseries['CON001']
        series, quantity = cache.get_series_and_quantity_for_timeseries(
            test_ts, check_for_updates=True)
        assert Assert(len(series)) == 725


class TWDBNoCacheTests(TWDBTestBase):
    """Run tests without cache backend"""

    def __context__(self):
        self.service = pyhis.Service(
            TWDB_WSDL_URL,
            use_cache=False)
        yield
        del self.service


class HISCentralTests(TestBase):
    @test
    def all_services(self):
        assert len(pyhis.his_central.services()) > 70


class ShapeTests(TestBase):
    def __context__(self):
        if os.path.exists(TEST_CACHE_DATABASE_PATH):
            os.remove(TEST_CACHE_DATABASE_PATH)
        pyhis.cache.init_cache(TEST_CACHE_DATABASE_PATH)

        self.service = pyhis.Service(
            TWDB_WSDL_URL,
            use_cache=True)
        yield
        del self.service

    @test
    def get_sites_within_shapefile(self):
        sites = self.service.get_sites_within_shapefile(TEST_SHAPEFILE_PATH)
        assert len(sites) == 13

if __name__ == '__main__':
    # suite = Tests([TWDBFreshCacheTests(),
    #                TWDBCacheTests(),
    #                TWDBNoCacheTests()])
    suite = Tests([
        TWDBFreshCacheTests(),
        TWDBCacheTests(),
        TWDBNoCacheTests(),
        HISCentralTests(),
        ShapeTests()
        ])

    suite.run()
