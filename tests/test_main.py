"""Test suite for ``main.py``.

Calculations for delta-values, bracket notation, internal normalizations, and ratios
can be found in their respective separate test files.
"""

import builtins

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu
import iniabu.data as data


# DATABASE CHECKS #


def test_init_database_default(ini_default):
    """Load iniabu with default database."""
    assert ini_default._ele_dict == data.lodders09_elements
    assert ini_default._iso_dict == data.lodders09_isotopes
    assert ini_default.database == "lodders09"


def test_init_database_nist(ini_nist):
    """Load iniabu with nist database."""
    assert ini_nist._ele_dict == data.nist15_elements
    assert ini_nist._iso_dict == data.nist15_isotopes
    assert ini_nist.database == "nist"


def test_init_database_asplund():
    """Load iniabu with asplund database."""
    ini = iniabu.IniAbu(database="asplund09")
    assert ini._ele_dict == data.asplund09_elements
    assert ini._iso_dict == data.asplund09_isotopes
    assert ini.database == "asplund09"


def test_init_database_invalid():
    """Initialize with invalid database name."""
    invalid_db = "invalid"
    with pytest.raises(ValueError) as err_info:
        iniabu.IniAbu(database=invalid_db)
    err_msg = err_info.value.args[0]
    assert (
        err_msg
        == f"The database {invalid_db} could not be found. Make sure it is a valid "
        f"option or choose one of the available ones."
    )


@pytest.mark.parametrize("unit", ("num_lin", "num_log", "mass_fraction"))
def test_database_print(unit, mocker):
    """Ensure message is print out when database is changed."""
    ini = iniabu.IniAbu()
    spy_print = mocker.spy(builtins, "print")  # put spy on print
    # change unit
    ini.unit = unit
    # now load the nist database for example
    db_new = "nist"
    ini.database = db_new

    spy_print.assert_called_with(
        f"iniabu loaded database: '{db_new}', current " f"units: '{unit}'"
    )


# TEST THE DICTIONARIES #


def test_ele_dict(ini_default):
    """Return the elementary dictionary."""
    assert ini_default.ele_dict == data.lodders09_elements


# TEST UNITS USED #


def test_unit_default(ini_default):
    """Ensure that standard abundance unit is linear."""
    assert ini_default.unit == "num_lin"


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_unit_log(ele):
    """Ensure logarithmic abundance unit is set correctly."""
    ini = iniabu.IniAbu()
    ini.unit = "num_log"
    assert ini.unit == "num_log"
    assert ini.ele[ele].abu_solar == ini.ele_dict_log[ele][0]


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_unit_mf(ele):
    """Ensure mass fraction unit is set correctly."""
    ini = iniabu.IniAbu()
    ini.unit = "mass_fraction"
    assert ini.unit == "mass_fraction"
    assert ini.ele[ele].abu_solar == ini.ele_dict_mf[ele][0]


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_unit_log_lin(ele):
    """Ensure linear abundance unit is set correctly after logarithmic (switch back)."""
    ini = iniabu.IniAbu()
    ini.unit = "num_log"
    assert ini.ele[ele].abu_solar == ini.ele_dict_log[ele][0]
    ini.unit = "num_lin"
    assert ini.unit == "num_lin"
    assert ini.ele[ele].abu_solar == ini.ele_dict[ele][0]


def test_unit_invalid(ini_default):
    """Raise a ValueError if invalid unit is set."""
    unit = "invalid_unit"
    with pytest.raises(ValueError) as err_info:
        ini_default.unit = unit
    err_msg = err_info.value.args[0]
    assert err_msg == f"Your selected unit {unit} is not a valid unit."


# PRIVATE ROUTINES


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_get_all_isos(ini_default, ele):
    """Ensure appropriate isotope list is returned for a given element."""
    iso_list = []
    for iso in ini_default.ele_dict[ele][1]:
        iso_list.append(f"{ele}-{iso}")
    assert ini_default._get_all_isos(ele) == iso_list


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_get_major_iso(ini_default, ele):
    """Ensure that the correct major isotope is returned."""
    index = np.array(ini_default.ele_dict[ele][2]).argmax()
    maj_iso = f"{ele}-{ini_default.ele_dict[ele][1][index]}"
    assert ini_default._get_major_iso(ele) == maj_iso
