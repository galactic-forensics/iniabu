"""Test suite for ``main.py``."""

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


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    value=st.floats(min_value=0, exclude_min=True),
)
def test_ele_bracket(ini_default, ele1, ele2, value):
    """Calculate bracket notation for an element ratio."""
    val_exp = np.log10(value) - np.log10(
        ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    )
    val_get = ini_default.ele_bracket(ele1, ele2, value)
    assert val_get == val_exp


def test_ele_bracket_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.ele_bracket(["Ne", "Mg"], ["Si", "Si"], 33)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested element ratios does not match length of "
        "provided values."
    )


def test_ele_bracket_many_values(ini_default):
    """Calculate element delta-values for many given measurements / model values."""
    ele1 = "Si"
    ele2 = "Ne"
    # "measured / modeled" values
    values = np.array([0.1, 0.2, 0.3])
    val_expected = np.log10(values) - np.log10(
        ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    )

    np.testing.assert_array_almost_equal(
        ini_default.ele_bracket(ele1, ele2, values), val_expected
    )


# ISOTOPE BRACKET #


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    value=st.floats(min_value=0, exclude_min=True),
)
def test_iso_bracket(ini_default, iso1, iso2, value):
    """Calculate bracket notation for an isotope ratio."""
    val_exp = np.log10(value) - np.log10(
        ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]
    )
    val_get = ini_default.iso_bracket(iso1, iso2, value)
    assert val_get == val_exp


def test_iso_bracket_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.iso_bracket(["Ne-21", "Mg-25"], "Si", 33)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested isotope ratios does not match length of "
        "provided values."
    )


def test_iso_bracket_many_values(ini_default):
    """Calculate bracket-values for many given measurements / model isotope values."""
    iso1 = "Si-29"
    iso2 = "Si-28"
    # "measured / modeled" values
    values = np.array([0.1, 0.2, 0.3])
    val_expected = np.log10(values) - np.log10(
        ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]
    )

    np.testing.assert_array_almost_equal(
        ini_default.iso_bracket(iso1, iso2, values), val_expected
    )


# ELEMENT DELTA #


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    value=st.floats(min_value=0, exclude_min=True, max_value=1e6),
    factor=st.floats(min_value=0, exclude_min=True, max_value=1e9),
)
def test_ele_delta(ini_default, ele1, ele2, value, factor):
    """Calculate delta-value for an element ratio in various units."""
    # default factor = 1000
    val_exp = (
        value / (ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]) - 1
    ) * 1000
    val_get = ini_default.ele_delta(ele1, ele2, value)
    assert val_get == val_exp
    # with a factor
    val_exp_fct = (
        value / (ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]) - 1
    ) * factor
    val_get_fct = ini_default.ele_delta(ele1, ele2, value, delta_factor=factor)
    assert val_get_fct == val_exp_fct


def test_ele_delta_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between nd arrays if more than one ratio."""
    with pytest.raises(ValueError) as err_info:
        ini_default.ele_delta(
            ["He", "Ne"], "Si", [0.07, 0.08, 0.09], delta_factor=10000
        )
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested element ratios does not match length of "
        "provided values."
    )


def test_ele_delta_many_values(ini_default):
    """Calculate element delta-values for many given measurements / model values."""
    ele1 = "Si"
    ele2 = "Ne"
    # "measured / modeled" values
    values = np.array([0.1, 0.2, 0.3])
    val_expected = (
        values / (ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]) - 1
    ) * 1000.0
    np.testing.assert_array_almost_equal(
        ini_default.ele_delta(ele1, ele2, values), val_expected
    )


# ISOTOPE DELTA #


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    value=st.floats(min_value=0, exclude_min=True, max_value=1e6),
    factor=st.floats(min_value=0, exclude_min=True, max_value=1e9),
)
def test_iso_delta(ini_default, iso1, iso2, value, factor):
    """Calculate delta-value for an isotope ratio."""
    # default factor = 1000
    val_exp = (
        value / (ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]) - 1
    ) * 1000
    val_get = ini_default.iso_delta(iso1, iso2, value)
    assert val_get == val_exp
    # with a factor
    # fixme next line can be simplified by just adjusting val_exp / 1000 * factor
    val_exp_fct = (
        value / (ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]) - 1
    ) * factor
    val_get_fct = ini_default.iso_delta(iso1, iso2, value, delta_factor=factor)
    assert val_get_fct == val_exp_fct


def test_iso_delta_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between the ndarrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.iso_delta("Ne", "Ne-20", [0.07, 0.09], delta_factor=10000)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested isotope ratios does not match length of "
        "provided values."
    )


def test_iso_delta_many_values(ini_default):
    """Calculate delta-values for many given measurements / model values."""
    iso1 = "Si-29"
    iso2 = "Si-28"
    # "measured / modeled" values
    values = np.array([0.1, 0.2, 0.3])
    val_expected = (
        values / (ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]) - 1
    ) * 1000.0
    np.testing.assert_array_almost_equal(
        ini_default.iso_delta(iso1, iso2, values), val_expected
    )


# RATIOS ELEMENT #


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele(ini_default, ele1, ele2):
    """Calculate element ratio for element vs. element."""
    val_exp = ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    assert ini_default.ele_ratio(ele1, ele2) == val_exp


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele_nist_db(ini_nist, ele1, ele2):
    """Calculate element ratio when not a number."""
    assert np.isnan(ini_nist.ele_ratio(ele1, ele2))


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele_from_log(ele1, ele2):
    """Calculate element ratio for element vs. element."""
    ini = iniabu.IniAbu()
    val_exp = ini.ele_dict[ele1][0] / ini.ele_dict[ele2][0]
    ini.unit = "num_log"
    assert ini.ele_ratio(ele1, ele2) == val_exp
    assert ini.ele_ratio(ele1, ele2, mass_fraction=False) == val_exp


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    ele3=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_eles_ele(ini_default, ele1, ele2, ele3):
    """Calculate element ratio for elements vs. element."""
    val_exp = np.array(
        [
            ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele3][0],
            ini_default.ele_dict[ele2][0] / ini_default.ele_dict[ele3][0],
        ]
    )
    np.testing.assert_equal(ini_default.ele_ratio([ele1, ele2], ele3), val_exp)


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    ele3=st.sampled_from(list(data.lodders09_elements.keys())),
    ele4=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_eles_eles(ini_default, ele1, ele2, ele3, ele4):
    """Calculate element ratio for elements vs. elements."""
    val_exp = np.array(
        [
            ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele3][0],
            ini_default.ele_dict[ele2][0] / ini_default.ele_dict[ele4][0],
        ]
    )
    np.testing.assert_equal(ini_default.ele_ratio([ele1, ele2], [ele3, ele4]), val_exp)


def test_ele_ratio_ele_eles_length_mismatch(ini_default):
    """Raise a ValueError if denominator has different length from nominator."""
    with pytest.raises(ValueError) as err_info:
        ini_default.ele_ratio("H", ["H", "Si"])
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "The denominator contains more than one entry but has a "
        "different length from the nominator. This is not allowed."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele_mass_fraction_true(ini_default, ele1, ele2):
    """Calculate element ratio for num values in mass fraction."""
    val_exp = (
        ini_default.ele_dict[ele1][0]
        * data.elements_mass[ele1]
        / (ini_default.ele_dict[ele2][0] * data.elements_mass[ele2])
    )
    assert ini_default.ele_ratio(ele1, ele2, mass_fraction=True) == pytest.approx(
        val_exp
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele_mf_notation_mf(ini_mf, ele1, ele2):
    """Calculate element ratio in mass_fraction with mass fraction notation."""
    val_exp = ini_mf.ele_dict_mf[ele1][0] / ini_mf.ele_dict_mf[ele2][0]
    assert ini_mf.ele_ratio(ele1, ele2, mass_fraction=True) == pytest.approx(val_exp)
    assert ini_mf.ele_ratio(ele1, ele2, mass_fraction=None) == pytest.approx(val_exp)


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ele_ratio_ele_ele_mf_notation_no_mf(ini_mf, ini_default, ele1, ele2):
    """Calculate element ratio for element vs. element in mass fraction notation."""
    val_exp = ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    assert ini_mf.ele_ratio(ele1, ele2, mass_fraction=False) == pytest.approx(val_exp)


# RATIOS ISOTOPES #


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_iso_iso(ini_default, iso1, iso2):
    """Calculate isotope ratio for one nominator and one denominator isotope."""
    val_exp = ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso2][1]
    assert ini_default.iso_ratio(iso1, iso2) == val_exp


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_iso_iso_from_log(iso1, iso2):
    """Calculate isotope ratio when database is in logarithmic state."""
    ini = iniabu.IniAbu()
    val_exp = ini.iso_dict[iso1][1] / ini.iso_dict[iso2][1]
    ini.unit = "num_log"
    assert ini.iso_ratio(iso1, iso2) == val_exp


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso3=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_isos_iso(ini_default, iso1, iso2, iso3):
    """Calculate isotope ratio for several nominators and one denominator isotope."""
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso3][1],
            ini_default.iso_dict[iso2][1] / ini_default.iso_dict[iso3][1],
        ]
    )
    np.testing.assert_equal(ini_default.iso_ratio([iso1, iso2], iso3), val_exp)


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso3=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso4=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_isos_isos(ini_default, iso1, iso2, iso3, iso4):
    """Calculate isotope ratios for several nominators and denominators."""
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][1] / ini_default.iso_dict[iso3][1],
            ini_default.iso_dict[iso2][1] / ini_default.iso_dict[iso4][1],
        ]
    )
    np.testing.assert_equal(ini_default.iso_ratio([iso1, iso2], [iso3, iso4]), val_exp)


def test_iso_ratio_isos_isos_length_mismatch(ini_default):
    """Raise a ValueError if nominator and denominator have different lengths."""
    with pytest.raises(ValueError) as err_info:
        ini_default.iso_ratio(["Ne-21", "Ne-22"], ["Ne-20", "Ne-21", "Ne-22"])
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "The denominator contains more than one entry but has a "
        "different length from the nominator. This is not allowed."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_ele_iso(ini_default, ele1, iso2):
    """Calculae isotope ratios for all isotopes of an element versus one isotope."""
    all_isos = ini_default._get_all_isos(ele1)
    val_exp = np.empty(len(all_isos))
    for it, iso in enumerate(all_isos):
        val_exp[it] = ini_default.iso_dict[iso][1] / ini_default.iso_dict[iso2][1]
    np.testing.assert_equal(ini_default.iso_ratio(ele1, iso2), val_exp)


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_iso_iso_mass_fraction_true(ini_default, iso1, iso2):
    """Calculate isotope ratio as mass fraction from num_lin units."""
    val_exp = (
        ini_default.iso_dict[iso1][1]
        * data.isotopes_mass[iso1]
        / (ini_default.iso_dict[iso2][1] * data.isotopes_mass[iso2])
    )
    np.testing.assert_allclose(
        ini_default.iso_ratio(iso1, iso2, mass_fraction=True), val_exp
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_iso_iso_mf_mass_fraction(ini_mf, iso1, iso2):
    """Calculate isotope ratio as mass fraction from mass_fraction units."""
    val_exp = ini_mf.iso_dict_mf[iso1][1] / ini_mf.iso_dict_mf[iso2][1]
    np.testing.assert_allclose(
        ini_mf.iso_ratio(iso1, iso2, mass_fraction=True), val_exp
    )
    np.testing.assert_allclose(
        ini_mf.iso_ratio(iso1, iso2, mass_fraction=None), val_exp
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_iso_ratio_iso_iso_mf_num_fraction(ini_mf, iso1, iso2):
    """Calculate isotope ratio as number fraction from mass_fraction units."""
    val_exp = ini_mf.iso_dict[iso1][1] / ini_mf.iso_dict[iso2][1]
    np.testing.assert_allclose(
        ini_mf.iso_ratio(iso1, iso2, mass_fraction=False), val_exp
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    ele=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_iso_ratio_isos_ele_mass_fraction_true(ini_default, iso1, iso2, ele):
    """Calculate isotope ratios as mass fraction from num_lin units."""
    iso_denominator = ini_default._get_major_iso(ele)
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][1]
            * data.isotopes_mass[iso1]
            / (
                ini_default.iso_dict[iso_denominator][1]
                * data.isotopes_mass[iso_denominator]
            ),
            ini_default.iso_dict[iso2][1]
            * data.isotopes_mass[iso2]
            / (
                ini_default.iso_dict[iso_denominator][1]
                * data.isotopes_mass[iso_denominator]
            ),
        ]
    )
    val_get = ini_default.iso_ratio([iso1, iso2], ele, mass_fraction=True)
    np.testing.assert_allclose(val_get, val_exp)


@given(
    iso=st.sampled_from(list(data.lodders09_isotopes.keys())),
    ele=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_iso_ratio_iso_ele(ini_default, iso, ele):
    """Calculate isotope ratio for one isotope and an element (i.e., major isotope)."""
    iso_denominator = ini_default._get_major_iso(ele)
    val_exp = ini_default.iso_dict[iso][1] / ini_default.iso_dict[iso_denominator][1]
    assert ini_default.iso_ratio(iso, ele) == val_exp


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
