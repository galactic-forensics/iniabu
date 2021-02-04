"""Test suite for ``isotopes.py``."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

import iniabu.data
import iniabu.isotopes
import iniabu.utilities


def test_isotopes_require_parent_class():
    """Test that class requires an appropriate parent class."""
    with pytest.raises(TypeError) as err_info:
        iniabu.isotopes.Isotopes(None, None)
    err_msg = err_info.value.args[0]
    assert err_msg == "Isotopes class must be initialized from IniAbu."


def test_isotopes_wrong_unit():
    """Raise NotImplementedError if a wrong unit is selected."""
    parent = iniabu.IniAbu()  # fake a correct parent
    unit = "random_unit"
    with pytest.raises(NotImplementedError) as err_info:
        iniabu.isotopes.Isotopes(parent, ["Si-28"], unit=unit)
    err_msg = err_info.value.args[0]
    assert err_msg == f"The chosen unit {unit} is currently not implemented."


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_isotopes_isos_list(ini_default, iso1, iso2):
    """Test that the isotope list is correctly initialized."""
    assert ini_default.iso[iso1]._isos == [iso1]
    assert ini_default.iso[[iso1, iso2]]._isos == [iso1, iso2]


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_a(ini_default, iso1, iso2):
    """Return mass number of isotope (what is actually put in already)."""
    ret_val = ini_default.iso[iso1].a
    assert isinstance(ret_val, np.int64)
    assert ret_val == int(iso1.split("-")[1])

    ret_val = ini_default.iso[[iso1, iso2]].a
    assert ret_val.dtype == np.int64
    np.testing.assert_equal(
        ret_val,
        np.array([int(iso1.split("-")[1]), int(iso2.split("-")[1])]),
    )


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_abu_rel(ini_default, iso1, iso2):
    """Test isotope relative abundance returner."""
    assert ini_default.iso[iso1].abu_rel == iniabu.data.lodders09_isotopes[iso1][0]
    left = ini_default.iso[[iso1, iso2]].abu_rel
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
def test_abu_solar(ini_default, iso1, iso2):
    """Test isotope solar abundance returner."""
    assert ini_default.iso[iso1].abu_solar == iniabu.data.lodders09_isotopes[iso1][1]
    left = ini_default.iso[[iso1, iso2]].abu_solar
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
def test_abu_solar_log(ini_default, iso1, iso2):
    """Test isotope solar abundance returner - log units."""
    ini_default.unit = "num_log"
    assert ini_default.iso[iso1].abu_solar == ini_default.iso_dict_log[iso1][1]
    left = ini_default.iso[[iso1, iso2]].abu_solar
    right = np.array(
        [ini_default.iso_dict_log[iso1][1], ini_default.iso_dict_log[iso2][1]]
    )
    np.testing.assert_equal(left, right)


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_abu_solar_mf(ini_default, iso1, iso2):
    """Test isotope solar abundance returner - mass fraction."""
    ini_default.unit = "mass_fraction"
    assert ini_default.iso[iso1].abu_solar == ini_default.iso_dict_mf[iso1][1]
    left = ini_default.iso[[iso1, iso2]].abu_solar
    right = np.array(
        [ini_default.iso_dict_mf[iso1][1], ini_default.iso_dict_mf[iso2][1]]
    )
    np.testing.assert_equal(left, right)


@given(
    iso1=st.sampled_from(list(iniabu.data.nist15_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.nist15_isotopes.keys())),
)
def test_abu_solar_nan(ini_nist, iso1, iso2):
    """Test isotope solar abundance returner if not available."""
    # check with database that does not contain this
    assert np.isnan(ini_nist.iso[iso1].abu_solar)
    assert np.isnan(ini_nist.iso[[iso1, iso2]].abu_solar).all()


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_mass(ini_default, iso1, iso2):
    """Get the mass of an isotope."""
    mass_expected = iniabu.data.isotopes_mass[iso1]
    assert ini_default.iso[iso1].mass == mass_expected

    masses_expected = np.array(
        [iniabu.data.isotopes_mass[iso1], iniabu.data.isotopes_mass[iso2]]
    )
    masses_gotten = ini_default.iso[[iso1, iso2]].mass
    np.testing.assert_equal(masses_gotten, masses_expected)


@given(iso=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())))
def test_name_single(ini_default, iso):
    """Return the name of a given isotope."""
    iso_name = ini_default.iso[iso].name
    assert iso_name == iso


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_name_multi(ini_default, iso1, iso2):
    """Return the names of multiple isotopes."""
    names_expected = [iso1, iso2]
    names_received = ini_default.iso[[iso1, iso2]].name
    assert names_received == names_expected


@given(ele=st.sampled_from(list(iniabu.data.lodders09_elements.keys())))
def test_name_all_ele(ini_default, ele):
    """Return the names of all isotopes if an element is passed on."""
    isos = iniabu.utilities.get_all_isos(ini_default, ele)
    assert ini_default.iso[ele].name == iniabu.utilities.return_list_simplifier(isos)


@given(
    ele1=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
    ele2=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_name_all_ele_multi(ini_default, ele1, ele2):
    """Return the names of all isotopes if elements are passed on."""
    isos = iniabu.utilities.get_all_isos(
        ini_default, ele1
    ) + iniabu.utilities.get_all_isos(ini_default, ele2)
    assert ini_default.iso[[ele1, ele2]].name == isos


@given(
    iso=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    ele=st.sampled_from(list(iniabu.data.lodders09_elements.keys())),
)
def test_name_all_iso_and_ele(ini_default, iso, ele):
    """Return the names of all isotopes for isotopes and element mixed."""
    isos = [iso] + iniabu.utilities.get_all_isos(ini_default, ele)
    assert ini_default.iso[[iso, ele]].name == isos


@given(
    iso1=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
    iso2=st.sampled_from(list(iniabu.data.lodders09_isotopes.keys())),
)
def test_z(ini_default, iso1, iso2):
    """Get the number of protons for element."""
    z_ele = iniabu.data.elements_z[iso1.split("-")[0]]
    ret_val = ini_default.iso[iso1].z
    assert isinstance(ret_val, np.int64)
    assert ret_val == z_ele

    # list
    z_eles = np.array([z_ele, iniabu.data.elements_z[iso2.split("-")[0]]])
    ret_val = ini_default.iso[[iso1, iso2]].z
    assert ret_val.dtype == np.int64
    np.testing.assert_equal(ret_val, z_eles)


def test_element(ini_default):
    """Return the elements of selected isotopes as strings."""
    assert ini_default.iso["H-2"]._element == ["H"]  # must be list
    assert ini_default.iso[["U-235", "Ne-21", "Ne-22"]]._element == ["U", "Ne", "Ne"]
