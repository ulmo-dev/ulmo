from attest import Assert, Tests
import pyhis


twdb = Tests()


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


if __name__ == '__main__':
    twdb.main()
