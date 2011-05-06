import os

from attest import Assert, Tests, TestBase, test

import pyhis


TWDB_WSDL_URL = 'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL'

#TWDB_WSDL_URL = 'file://' + os.path.abspath('./twdb_wsdl.xml')
USGS_WSDL_URL = 'file://' + os.path.abspath('./usgs_wsdl.xml')

TEST_CACHE_DATABASE_PATH = '/tmp/pyhis_test_cache.db'


class TWDBTestBase(TestBase):
    """Base class for using TWDB dataset as a source"""

    @test
    def get_site(self):
        site = self.source.get_site('TWDBSondes', 'Aransas95_D1')
        assert Assert(site.latitude) == 28.06666667
        assert Assert(site.longitude) == -97.20333333
        assert Assert(site.description) == 'Upper Copano Bay'
        assert Assert(site.source.url) == TWDB_WSDL_URL

    @test
    def check_sites(self):
        assert Assert(len(self.source.get_all_sites())) == 74
        assert Assert(len(self.source.sites)) == 74

    @test
    def check_variables(self):
        assert Assert(len(self.source.sites['Aransas95_D1'].timeseries)) == 5
        assert Assert(len(self.source.sites['ULM95_3C'].timeseries)) == 5

    @test
    def check_dataframe(self):
        df = self.source.sites['Aransas95_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 725
        df2 = self.source.sites['ULM95_3C'].dataframe
        assert Assert(len(df['SAL001'])) == 725


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
