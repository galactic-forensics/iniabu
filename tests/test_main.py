import pytest

import iniabu
import iniabu.data as data


def test_init_database_default(ini_default):
    """Test loading iniabu with default database."""
    assert ini_default._ele_dict == data.lodders09_elements
    assert ini_default._iso_dict == data.lodders09_isotopes
    assert ini_default.database == "lodders09"


def test_init_database_nist(ini_nist):
    """Test loading iniabu with nist database."""
    assert ini_nist._ele_dict == data.nist15_elements
    assert ini_nist._iso_dict == data.nist15_isotopes
    assert ini_nist.database == "nist"


def test_init_database_asplund():
    """Test loading iniabu with asplund database."""
    ini = iniabu.IniAbu(database="asplund09")
    assert ini._ele_dict == data.asplund09_elements
    assert ini._iso_dict == data.asplund09_isotopes
    assert ini.database == "asplund09"


def test_init_database_invalid(ini_nist):
    """Test data base initialization with invalid database"""
    with pytest.raises(ValueError):
        iniabu.IniAbu(database="not-valid-database")


def test_ele_dict(ini_default):
    """Test returning the elementary dictionary"""
    assert ini_default.ele_dict == data.lodders09_elements
