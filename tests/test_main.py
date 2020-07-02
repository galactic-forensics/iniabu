import iniabu
import iniabu.data as data
import pytest


def test_auto_loading():
    """
    Ensure that the lodders09 is loaded by default. This is what the docs say.
    """
    assert iniabu.ini._database == "lodders09"


def test_init_database():
    """
    Test loading iniabu with all available databases
    """
    # test nist15 database
    ini = iniabu.IniAbu(database="nist")
    assert ini._ele_dict == data.nist15_elements
    assert ini._iso_dict == data.nist15_isotopes

    # test lodders09 database
    ini = iniabu.IniAbu(database="lodders09")
    assert ini._ele_dict == data.lodders09_elements
    assert ini._iso_dict == data.lodders09_isotopes

    # test that wrong database raises a ValueError
    with pytest.raises(ValueError):
        iniabu.IniAbu(database="not-valid-database")
