"""Test suite for ``main.py``, bracket notation calculations."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data as data


# ELEMENT BRACKET #


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
