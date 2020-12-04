"""Test suite for ``__init__.py``."""

from iniabu import ini, inilog, inimf


def test_ini():
    """Ensure ``ini`` abundance has correct units and database."""
    assert ini.database == "lodders09"
    assert ini.unit == "num_lin"


def test_inimf():
    """Ensure ``inimf`` abundance has correct units and database."""
    assert inimf.database == "lodders09"
    assert inimf.unit == "mass_fraction"


def test_inilog():
    """Ensure ``inilog`` abundance has correct units and database."""
    assert inilog.database == "lodders09"
    assert inilog.unit == "num_log"
