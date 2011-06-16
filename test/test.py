import os
import tempfile

from attest import Assert, Tests, TestBase, test

import pyhis


TWDB_WSDL_URL = 'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL'

#TWDB_WSDL_URL = 'file://' + os.path.abspath('./twdb_wsdl.xml')
USGS_WSDL_URL = 'file://' + os.path.abspath('./usgs_wsdl.xml')

TEST_CACHE_DATABASE_PATH = os.path.join(tempfile.gettempdir(),
                                        'pyhis_test_cache.db')


class TWDBTestBase(TestBase):
    """Base class for using TWDB dataset as a source"""

    @test
    def get_site(self):
        site = self.source.get_site('TWDBSondes', 'Aransas95_D1')
        assert Assert(site.latitude) == 28.06666667
        assert Assert(site.longitude) == -97.20333333
        assert Assert(site.name) == 'Upper Copano Bay'
        assert Assert(site.source.url) == TWDB_WSDL_URL

    @test
    def check_sites(self):
        assert Assert(len(self.source.get_all_sites())) == 74
        assert Assert(len(self.source.sites)) == 74

    @test
    def check_variables(self):
        assert Assert(len(self.source.sites['Aransas95_D1'].timeseries)) == 5
        assert Assert(len(self.source.sites['Christmas92_D1'].timeseries)) == 5

    @test
    def check_dataframe(self):
        df = self.source.sites['Aransas95_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 725
        df = self.source.sites['Christmas92_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 1044


class TWDBFreshCacheTests(TWDBTestBase):
    """
    Run tests with cache backend
    """

    def __context__(self):
        if os.path.exists(TEST_CACHE_DATABASE_PATH):
            os.remove(TEST_CACHE_DATABASE_PATH)
        pyhis.cache.init_cache(TEST_CACHE_DATABASE_PATH)

        self.source = pyhis.Source(
            TWDB_WSDL_URL,
            use_cache=True)
        yield
        del self.source


class TWDBCacheTests(TWDBTestBase):
    """
    Run tests with cache backend
    """

    def __context__(self):
        pyhis.cache.init_cache(TEST_CACHE_DATABASE_PATH)
        self.source = pyhis.Source(
            TWDB_WSDL_URL,
            use_cache=True)
        yield
        del self.source

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
            self.source.sites['Aransas95_D1'].timeseries['CON001'])

        cached_ts.values = cached_ts.values[:4]
        cache.db_session.commit()

        # test that the db has been altered
        del cache._cache['timeseries'][(TWDB_WSDL_URL, 'TWDBSondes',
                                              'Aransas95_D1', 'CON001')]

        # query timseries so that it gets set up in the cache
        cached_ts = cache.CacheTimeSeries(
            self.source.sites['Aransas95_D1'].timeseries['CON001'])
        assert Assert(cached_ts.values.count()) == 4

        # test that check_for_updates sucessfully updates the
        # timeseries values
        del cache._cache['timeseries'][(TWDB_WSDL_URL, 'TWDBSondes',
                                        'Aransas95_D1', 'CON001')]

        test_ts = self.source.sites['Aransas95_D1'].timeseries['CON001']
        series, quantity = cache.get_series_and_quantity_for_timeseries(
            test_ts, check_for_updates=True)
        assert Assert(len(series)) == 725


class TWDBNoCacheTests(TWDBTestBase):
    """
    Run tests without cache backend
    """

    def __context__(self):
        self.source = pyhis.Source(
            TWDB_WSDL_URL,
            use_cache=False)
        yield
        del self.source


if __name__ == '__main__':
    # suite = Tests([TWDBFreshCacheTests(),
    #                TWDBCacheTests(),
    #                TWDBNoCacheTests()])
    suite = Tests([
        TWDBFreshCacheTests(),
        TWDBCacheTests(),
        TWDBNoCacheTests(),
        ])

    suite.run()
