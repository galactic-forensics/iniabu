"""Test suite for ``elements.py``."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data
import iniabu.elements


def test_elements_require_parent_class():
    """Test that class requires an appropriate parent class."""
    # Parent class testing
    with pytest.raises(TypeError) as err_info:
        iniabu.elements.Elements(None, None)
    err_msg = err_info.value.args[0]
    assert err_msg == "Elements class must be initialized from IniAbu."


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_elements_eles_list(ini_default, ele1, ele2):
    """Test that the element list is correctly initialized."""
    assert ini_default.element[ele1]._eles == [ele1]
    assert ini_default.element[[ele1, ele2]]._eles == [ele1, ele2]


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_a(ini_default, ele1, ele2):
    """Test isotope atomic number returner."""
    assert (
        ini_default.element[ele1].isotopes_a
        == np.array(iniabu.data.lodders09_elements[ele1][1])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_a
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][1]),
        np.array(iniabu.data.lodders09_elements[ele2][1]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_relative_abundance(ini_default, ele1, ele2):
    """Test isotope relative abundance returner."""
    assert (
        ini_default.element[ele1].isotopes_relative_abundance
        == np.array(iniabu.data.lodders09_elements[ele1][2])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_relative_abundance
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][2]),
        np.array(iniabu.data.lodders09_elements[ele2][2]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_isotopes_solar_abundance(ini_default, ele1, ele2):
    """Test isotope solar abundance returner."""
    assert (
        ini_default.element[ele1].isotopes_solar_abundance
        == np.array(iniabu.data.lodders09_elements[ele1][3])
    ).all()

    left = ini_default.element[[ele1, ele2]].isotopes_solar_abundance
    right = [
        np.array(iniabu.data.lodders09_elements[ele1][3]),
        np.array(iniabu.data.lodders09_elements[ele2][3]),
    ]
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
)
def test_isotopes_solar_abundance_nan(ini_nist, ele1, ele2):
    """Test isotope solar abundance returner when not available."""
    # make sure np.nan is returned for other databases
    assert np.isnan(ini_nist.element[ele1].isotopes_solar_abundance).all()

    val = ini_nist.element[[ele1, ele2]].isotopes_solar_abundance
    assert all([np.isnan(it).all() for it in val])


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_solar_abundance(ini_default, ele1, ele2):
    """Test solar abundance property."""
    assert (
        ini_default.element[ele1].solar_abundance
        == iniabu.data.lodders09_elements[ele1][0]
    )
    left = ini_default.element[[ele1, ele2]].solar_abundance
    right = np.array(
        [
            iniabu.data.lodders09_elements[ele1][0],
            iniabu.data.lodders09_elements[ele2][0],
        ]
    )
    np.testing.assert_equal(left, right)


@given(
    ele1=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.nist15_elements.keys())),
)
def test_solar_abundance_nan(ini_nist, ele1, ele2):
    """Test solar abundance property when not available."""
    assert np.isnan(ini_nist.element[ele1].solar_abundance)
    assert np.isnan(ini_nist.element[[ele1, ele2]].solar_abundance).all()
