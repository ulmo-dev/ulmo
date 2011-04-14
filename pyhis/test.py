from attest import Assert, Tests

import pyhis


twdb = Tests()
tceq = Tests()
tpwd = Tests()


@twdb.context
def get_twdb_client():
    source = pyhis.Source(
        'http://his.crwr.utexas.edu/TWDB_Sondes/cuahsi_1_0.asmx?WSDL')
    yield source


@twdb.test
def check_sites(source):
    assert Assert(len(source.sites)) == 74


@twdb.test
def check_variables(source):
    assert Assert(len(source.sites[0].variables)) == 5


@twdb.test
def check_dataframe(source):
    df = source.sites[0].dataframe
    assert Assert(len(df['SAL001'])) == 706


@twdb.test
def check_dataframe2(source):
    df = source.sites[0].dataframe
    assert Assert(len(df['SAL001'])) == 706


@tceq.context
def get_tceq_client():
    source = pyhis.Source(
        'http://www.twdb.state.tx.us/appws/histceqswqmis/cuahsi_1_0.asmx?WSDL')
    yield source


@tceq.test
def check_sites(source):
    assert Assert(len(source.sites)) == 8960


@tceq.test
def get_dataframe(source):
    df = source.sites[0].dataframe


if __name__ == '__main__':
    twdb.main()
