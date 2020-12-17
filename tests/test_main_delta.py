"""Test suite for ``main.py``, delta-value calculations."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data as data


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
