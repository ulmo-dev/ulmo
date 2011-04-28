import os

from attest import Assert, Tests, TestBase, test

import pyhis


#TWDB_WSDL_URL = 'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL'

TWDB_WSDL_URL = 'file://' + os.path.abspath('./twdb_wsdl.xml')
USGS_WSDL_URL = 'file://' + os.path.abspath('./usgs_wsdl.xml')


class TWDBTestBase(TestBase):
    """Base class for using TWDB dataset as a source"""

    @test
    def check_sites(self):
        assert Assert(len(self.source.sites)) == 74

    @test
    def check_variables(self):
        assert Assert(len(self.source.sites['Aransas95_D1'].variables)) == 5
        assert Assert(len(self.source.sites['ULM95_3C'].variables)) == 5

    @test
    def check_dataframe(self):
        df = self.source.sites['Aransas95_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 706
        df2 = self.source.sites['ULM95_3C'].dataframe
        assert Assert(len(df['SAL001'])) == 706


class TWDBFreshCacheTests(TWDBTestBase):
    """
    Run tests with cache backend
    """

    def __context__(self):
        if os.path.exists(pyhis.cache.CACHE_DATABASE_FILE):
            os.remove(pyhis.cache.CACHE_DATABASE_FILE)
        pyhis.cache.init()
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
