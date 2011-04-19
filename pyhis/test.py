import os

from attest import Assert, Tests, TestBase, test

import pyhis


class TWDBTestBase(TestBase):
    """Base class for using TWDB dataset as a source"""

    @test
    def check_sites(self):
        assert Assert(len(self.source.sites)) == 74

    @test
    def check_variables(self):
        assert Assert(len(self.source.sites['Aransas95_D1'].variables)) == 5

    @test
    def check_dataframe(self):
        df = self.source.sites['Aransas95_D1'].dataframe
        assert Assert(len(df['SAL001'])) == 706


class TWDBFreshCacheTests(TWDBTestBase):
    """
    Run tests with cache backend
    """

    def __context__(self):
        if os.path.exists(pyhis.cache.CACHE_DATABASE_FILE):
            os.remove(pyhis.cache.CACHE_DATABASE_FILE)
        self.source = pyhis.Source(
            'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL',
            use_cache=True)
        yield
        del self.source


class TWDBCacheTests(TWDBTestBase):
    """
    Run tests with cache backend
    """

    def __context__(self):
        self.source = pyhis.Source(
            'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL',
            use_cache=True)
        yield
        del self.source


class TWDBNoCacheTests(TWDBTestBase):
    """
    Run tests without cache backend
    """

    def __context__(self):
        self.source = pyhis.Source(
            'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL',
            use_cache=False)
        yield
        del self.source


if __name__ == '__main__':
    suite = Tests([TWDBFreshCacheTests(),
                   TWDBCacheTests(),
                   TWDBNoCacheTests()])
    suite.run()
