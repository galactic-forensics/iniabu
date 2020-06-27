import iniabu
import pytest

ini = iniabu.IniAbu()


def test_init_bad_database():
    """
    Test loading iniabu without a database
    :return:
    """
    with pytest.raises(Exception) as e_info:
        iniabu.IniAbu("not_a_database_test")


def test_temp():
    """
    Tests the temporary function
    :return:
    """
    assert ini.temp(4) == 5
