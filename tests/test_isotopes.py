"""Test suite for ``isotopes.py``."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data
import iniabu.isotopes


def test_isotopes_require_parent_class():
    """Test that class requires an appropriate parent class."""
    with pytest.raises(TypeError) as err_info:
        iniabu.isotopes.Isotopes(None, None)
    err_msg = err_info.value.args[0]
    assert err_msg == "Isotopes class must be initialized from IniAbu."


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_isotopes_isos_list(ini_default, iso1, iso2):
    """Test that the isotope list is correctly initialized."""
    assert ini_default.isotope[iso1]._isos == [iso1]
    assert ini_default.isotope[[iso1, iso2]]._isos == [iso1, iso2]


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_mass(ini_default, iso1, iso2):
    """Get the mass of an isotope."""
    mass_expected = iniabu.data.isotopes_mass[iso1]
    assert ini_default.isotope[iso1].mass == mass_expected

    masses_expected = np.array(
        [iniabu.data.isotopes_mass[iso1], iniabu.data.isotopes_mass[iso2]]
    )
    masses_gotten = ini_default.isotope[[iso1, iso2]].mass
    np.testing.assert_equal(masses_gotten, masses_expected)


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_relative_abundance(ini_default, iso1, iso2):
    """Test isotope relative abundance returner."""
    assert (
        ini_default.isotope[iso1].relative_abundance
        == iniabu.data.lodders09_isotopes[iso1][0]
    )
    left = ini_default.isotope[[iso1, iso2]].relative_abundance
    right = np.array(
        [
            iniabu.data.lodders09_isotopes[iso1][0],
            iniabu.data.lodders09_isotopes[iso2][0],
        ]
    )
    np.testing.assert_equal(left, right)


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_solar_abundance(ini_default, iso1, iso2):
    """Test isotope solar abundance returner."""
    assert (
        ini_default.isotope[iso1].solar_abundance
        == iniabu.data.lodders09_isotopes[iso1][1]
    )
    left = ini_default.isotope[[iso1, iso2]].solar_abundance
    right = np.array(
        [
            iniabu.data.lodders09_isotopes[iso1][1],
            iniabu.data.lodders09_isotopes[iso2][1],
        ]
    )
    np.testing.assert_equal(left, right)


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_solar_abundance_log(ini_default, iso1, iso2):
    """Test isotope solar abundance returner."""
    ini_default.abundance_unit = "log"
    assert (
        ini_default.isotope[iso1].solar_abundance == ini_default.iso_dict_log[iso1][1]
    )
    left = ini_default.isotope[[iso1, iso2]].solar_abundance
    right = np.array(
        [ini_default.iso_dict_log[iso1][1], ini_default.iso_dict_log[iso2][1]]
    )
    np.testing.assert_equal(left, right)


@given(
    iso1=st.sampled_from(list(iniabu.data.nist15_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.nist15_isotopes.keys())),
)
def test_solar_abundance_nan(ini_nist, iso1, iso2):
    """Test isotope solar abundance returner if not available."""
    # check with database that does not contain this
    assert np.isnan(ini_nist.isotope[iso1].solar_abundance)
    assert np.isnan(ini_nist.isotope[[iso1, iso2]].solar_abundance).all()
