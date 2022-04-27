"""Test suite for ``main.py``, ratio calculations."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu
import iniabu.data as data
from iniabu.utilities import get_all_stable_isos


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
    all_isos = get_all_stable_isos(ini_default, ele1)
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
    iso_denominator = ini_default._get_norm_iso(ele)
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
    iso_denominator = ini_default._get_norm_iso(ele)
    val_exp = ini_default.iso_dict[iso][1] / ini_default.iso_dict[iso_denominator][1]
    assert ini_default.iso_ratio(iso, ele) == val_exp


# TESTS FOR NIST RATIOS - USE RELATIVE IF THE SAME ELEMENT THROUGHOUT THE BOARD


def test_nist_ratio_iso_iso(ini_nist):
    """If NIST db, calculate isotope ratios (same element) from relative ratio."""
    iso1 = "Ne-21"
    iso2 = "Ne-22"
    expected = ini_nist.iso_dict[iso1][0] / ini_nist.iso_dict[iso2][0]
    assert ini_nist.iso_ratio(iso1, iso2) == expected


def test_nist_ratio_iso_iso_unequal(ini_nist):
    """Return nan if NIST db and isotope ratio of different elements requested."""
    iso1 = "He-3"
    iso2 = "Ne-21"
    assert np.isnan(ini_nist.iso_ratio(iso1, iso2))


def test_nist_ratio_isos_isos(ini_nist):
    """Assortment of tests for NIST db isoratio return."""
    nom = ["He-3", "Ne-21", "Ne-22", "Ar-36"]
    denom = ["Ne-20", "Ne-20", "He-4", "Ar-38"]
    expected = np.array(
        [
            np.nan,
            ini_nist.iso_dict[nom[1]][0] / ini_nist.iso_dict[denom[1]][0],
            np.nan,
            ini_nist.iso_dict[nom[3]][0] / ini_nist.iso_dict[denom[3]][0],
        ]
    )
    np.testing.assert_equal(ini_nist.iso_ratio(nom, denom), expected)
