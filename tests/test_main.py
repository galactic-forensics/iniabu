"""Test suite for ``main.py``."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu
import iniabu.data as data


# DATABASE SANITY CHECKS #


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


def test_ele_dict(ini_default):
    """Return the elementary dictionary."""
    assert ini_default.ele_dict == data.lodders09_elements


def test_abundance_unit_default(ini_default):
    """Ensure that standard abundance unit is linear."""
    assert ini_default.abundance_unit == "lin"


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_abundance_unit_log(ele):
    """Ensure logarithmic abundance unit is set correctly."""
    ini = iniabu.IniAbu()
    ini.abundance_unit = "log"
    assert ini.abundance_unit == "log"
    assert ini.element[ele].solar_abundance == ini.ele_dict_log[ele][0]


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_abundance_unit_log_lin(ele):
    """Ensure linear abundance unit is set correctly after logarithmic (switch back)."""
    ini = iniabu.IniAbu()
    ini.abundance_unit = "log"
    assert ini.element[ele].solar_abundance == ini.ele_dict_log[ele][0]
    ini.abundance_unit = "lin"
    assert ini.abundance_unit == "lin"
    assert ini.element[ele].solar_abundance == ini.ele_dict[ele][0]


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_abundance_unit_after_new_database(ele):
    """Ensure abundance unit is reset to linear when new database is loaded."""
    ini = iniabu.IniAbu()
    ini.abundance_unit = "log"
    ini.database = "lodders09"
    assert ini.abundance_unit == "lin"
    assert ini.element[ele].solar_abundance == data.lodders09_elements[ele][0]


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    value=st.floats(min_value=0, exclude_min=True),
)
def test_bracket_element(ini_default, ele1, ele2, value):
    """Calculate bracket notation for an element ratio."""
    val_exp = np.log10(value) - np.log10(
        ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    )
    val_get = ini_default.bracket_element(ele1, ele2, value)
    assert val_get == val_exp


def test_bracket_element_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.bracket_element(["Ne", "Mg"], ["Si", "Si"], 33)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested element ratios does not match length of "
        "provided values."
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    value=st.floats(min_value=0, exclude_min=True),
)
def test_bracket_isotope(ini_default, iso1, iso2, value):
    """Calculate bracket notation for an isotope ratio."""
    val_exp = np.log10(value) - np.log10(
        ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso2][0]
    )
    val_get = ini_default.bracket_isotope(iso1, iso2, value)
    assert val_get == val_exp


def test_bracket_isotope_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.bracket_isotope(["Ne-21", "Mg-25"], "Si", 33)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested isotope ratios does not match length of "
        "provided values."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    value=st.floats(min_value=0, exclude_min=True, max_value=1e6),
    factor=st.floats(min_value=0, exclude_min=True, max_value=1e9),
)
def test_delta_element(ini_default, ele1, ele2, value, factor):
    """Calculate delta-value for an element ratio in various units."""
    # default factor = 1000
    val_exp = (
        value / (ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]) - 1
    ) * 1000
    val_get = ini_default.delta_element(ele1, ele2, value)
    assert val_get == val_exp
    # with a factor
    val_exp_fct = (
        value / (ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]) - 1
    ) * factor
    val_get_fct = ini_default.delta_element(ele1, ele2, value, delta_factor=factor)
    assert val_get_fct == val_exp_fct


def test_delta_element_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between nd arrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.delta_element("Ne", "Si", [0.07, 0.09], delta_factor=10000)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested element ratios does not match length of "
        "provided values."
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    value=st.floats(min_value=0, exclude_min=True, max_value=1e6),
    factor=st.floats(min_value=0, exclude_min=True, max_value=1e9),
)
def test_delta_isotope(ini_default, iso1, iso2, value, factor):
    """Calculate delta-value for an isotope ratio."""
    # default factor = 1000
    val_exp = (
        value / (ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso2][0]) - 1
    ) * 1000
    val_get = ini_default.delta_isotope(iso1, iso2, value)
    assert val_get == val_exp
    # with a factor
    val_exp_fct = (
        value / (ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso2][0]) - 1
    ) * factor
    val_get_fct = ini_default.delta_isotope(iso1, iso2, value, delta_factor=factor)
    assert val_get_fct == val_exp_fct


def test_delta_isotope_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between the ndarrays."""
    with pytest.raises(ValueError) as err_info:
        ini_default.delta_isotope("Ne-22", "Ne-20", [0.07, 0.09], delta_factor=10000)
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested isotope ratios does not match length of "
        "provided values."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_ele_ele(ini_default, ele1, ele2):
    """Calculate element ratio for element vs. element."""
    val_exp = ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele2][0]
    assert ini_default.ratio_element(ele1, ele2) == val_exp


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_ele_ele_nist_db(ini_nist, ele1, ele2):
    """Calculate element ratio when not a number."""
    assert np.isnan(ini_nist.ratio_element(ele1, ele2))


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_ele_ele_from_log(ele1, ele2):
    """Calculate element ratio for element vs. element."""
    ini = iniabu.IniAbu()
    val_exp = ini.ele_dict[ele1][0] / ini.ele_dict[ele2][0]
    ini.abundance_unit = "log"
    assert ini.ratio_element(ele1, ele2) == val_exp


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    ele3=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_eles_ele(ini_default, ele1, ele2, ele3):
    """Calculate element ratio for elements vs. element."""
    val_exp = np.array(
        [
            ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele3][0],
            ini_default.ele_dict[ele2][0] / ini_default.ele_dict[ele3][0],
        ]
    )
    np.testing.assert_equal(ini_default.ratio_element([ele1, ele2], ele3), val_exp)


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
    ele3=st.sampled_from(list(data.lodders09_elements.keys())),
    ele4=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_eles_eles(ini_default, ele1, ele2, ele3, ele4):
    """Calculate element ratio for elements vs. elements."""
    val_exp = np.array(
        [
            ini_default.ele_dict[ele1][0] / ini_default.ele_dict[ele3][0],
            ini_default.ele_dict[ele2][0] / ini_default.ele_dict[ele4][0],
        ]
    )
    np.testing.assert_equal(
        ini_default.ratio_element([ele1, ele2], [ele3, ele4]), val_exp
    )


def test_ratio_element_ele_eles_length_mismatch(ini_default):
    """Raise a ValueError if denominator has different length from nominator."""
    with pytest.raises(ValueError) as err_info:
        ini_default.ratio_element("H", ["H", "Si"])
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "The denominator contains more than one entry but has a "
        "different length from the nominator. This is not allowed."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_element_ele_ele_mass_fraction(ini_default, ele1, ele2):
    """Calculate element ratio for element vs. element in mass fraction."""
    val_exp = (
        ini_default.ele_dict[ele1][0]
        * data.elements_mass[ele2]
        / (ini_default.ele_dict[ele2][0] * data.elements_mass[ele1])
    )
    assert ini_default.ratio_element(ele1, ele2, mass_fraction=True) == pytest.approx(
        val_exp
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_iso_iso(ini_default, iso1, iso2):
    """Calculate isotope ratio for one nominator and one denominator isotope."""
    val_exp = ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso2][0]
    assert ini_default.ratio_isotope(iso1, iso2) == val_exp


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_iso_iso_from_log(iso1, iso2):
    """Calculate isotope ratio when database is in logarithmic state."""
    ini = iniabu.IniAbu()
    val_exp = ini.iso_dict[iso1][0] / ini.iso_dict[iso2][0]
    ini.abundance_unit = "log"
    assert ini.ratio_isotope(iso1, iso2) == val_exp


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso3=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_isos_iso(ini_default, iso1, iso2, iso3):
    """Calculate isotope ratio for several nominators and one denominator isotope."""
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso3][0],
            ini_default.iso_dict[iso2][0] / ini_default.iso_dict[iso3][0],
        ]
    )
    np.testing.assert_equal(ini_default.ratio_isotope([iso1, iso2], iso3), val_exp)


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso3=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso4=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_isos_isos(ini_default, iso1, iso2, iso3, iso4):
    """Calculate isotope ratios for several nominators and denominators."""
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][0] / ini_default.iso_dict[iso3][0],
            ini_default.iso_dict[iso2][0] / ini_default.iso_dict[iso4][0],
        ]
    )
    np.testing.assert_equal(
        ini_default.ratio_isotope([iso1, iso2], [iso3, iso4]), val_exp
    )


def test_ratio_isotope_isos_isos_length_mismatch(ini_default):
    """Raise a ValueError if nominator and denominator have different lengths."""
    with pytest.raises(ValueError) as err_info:
        ini_default.ratio_isotope(["Ne-21", "Ne-22"], ["Ne-20", "Ne-21", "Ne-22"])
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "The denominator contains more than one entry but has a "
        "different length from the nominator. This is not allowed."
    )


@given(
    ele1=st.sampled_from(list(data.lodders09_elements.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_ele_iso(ini_default, ele1, iso2):
    """Calculae isotope ratios for all isotopes of an element versus one isotope."""
    all_isos = ini_default._get_all_isotopes(ele1)
    val_exp = np.empty(len(all_isos))
    for it, iso in enumerate(all_isos):
        val_exp[it] = ini_default.iso_dict[iso][0] / ini_default.iso_dict[iso2][0]
    np.testing.assert_equal(ini_default.ratio_isotope(ele1, iso2), val_exp)


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
)
def test_ratio_isotope_iso_iso_mass_fraction(ini_default, iso1, iso2):
    """Calculate isotope ratios for isotopes and element as mass fraction."""
    val_exp = (
        ini_default.iso_dict[iso1][0]
        * data.isotopes_mass[iso2]
        / (ini_default.iso_dict[iso2][0] * data.isotopes_mass[iso1])
    )
    np.testing.assert_allclose(
        ini_default.ratio_isotope(iso1, iso2, mass_fraction=True), val_exp
    )


@given(
    iso1=st.sampled_from(list(data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(data.lodders09_isotopes.keys())),
    ele=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_isotope_isos_ele_mass_fraction(ini_default, iso1, iso2, ele):
    """Calculate isotope ratios for isotopes and element as mass fraction."""
    iso_denominator = ini_default._get_major_isotope(ele)
    val_exp = np.array(
        [
            ini_default.iso_dict[iso1][0]
            * data.isotopes_mass[iso_denominator]
            / (ini_default.iso_dict[iso_denominator][0] * data.isotopes_mass[iso1]),
            ini_default.iso_dict[iso2][0]
            * data.isotopes_mass[iso_denominator]
            / (ini_default.iso_dict[iso_denominator][0] * data.isotopes_mass[iso2]),
        ]
    )
    val_get = ini_default.ratio_isotope([iso1, iso2], ele, mass_fraction=True)
    np.testing.assert_allclose(val_get, val_exp)


@given(
    iso=st.sampled_from(list(data.lodders09_isotopes.keys())),
    ele=st.sampled_from(list(data.lodders09_elements.keys())),
)
def test_ratio_isotope_iso_ele(ini_default, iso, ele):
    """Calculate isotope ratio for one isotope and an element (i.e., major isotope)."""
    iso_denominator = ini_default._get_major_isotope(ele)
    val_exp = ini_default.iso_dict[iso][0] / ini_default.iso_dict[iso_denominator][0]
    assert ini_default.ratio_isotope(iso, ele) == val_exp


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_get_all_isotopes(ini_default, ele):
    """Ensure appropriate isotope list is returned for a given element."""
    iso_list = []
    for iso in ini_default.ele_dict[ele][1]:
        iso_list.append(f"{ele}-{iso}")
    assert ini_default._get_all_isotopes(ele) == iso_list


@given(ele=st.sampled_from(list(data.lodders09_elements.keys())))
def test_get_major_isotope(ini_default, ele):
    """Ensure that the correct major isotope is returned."""
    index = np.array(ini_default.ele_dict[ele][2]).argmax()
    maj_iso = f"{ele}-{ini_default.ele_dict[ele][1][index]}"
    assert ini_default._get_major_isotope(ele) == maj_iso
