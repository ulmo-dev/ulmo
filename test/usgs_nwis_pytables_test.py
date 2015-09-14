from builtins import str
import pytest

from ulmo.usgs import nwis


def test_pytables_raises_deprecation_warnings(recwarn):
    nwis.pytables.get_sites()
    w = recwarn.pop(DeprecationWarning)
    assert issubclass(w.category, DeprecationWarning)
    assert 'nwis.pytables module has moved' in str(w.message)


def test_hdf5_doesnt_raise_deprecation_warnings(recwarn):
    nwis.hdf5.get_sites()
    with pytest.raises(AssertionError):
        recwarn.pop(DeprecationWarning)
