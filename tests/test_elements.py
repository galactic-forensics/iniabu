import iniabu.elements

import numpy as np
import pytest


def test_elements_require_parent_class():
    """Test that class requires an appropriate parent class."""
    # Parent class testing
    with pytest.raises(TypeError):
        iniabu.elements.Elements(None, None)


def test_elements_eles_list(ini_default):
    """Test that the element list is correctly initialized."""
    assert ini_default.element["Si"]._eles == ["Si"]
    assert ini_default.element[["Fe", "Ni"]]._eles == ["Fe", "Ni"]


def test_isotopes_a(ini_default):
    """Test isotope atomic number returner"""
    assert (ini_default.element["Si"].isotopes_a == np.array([28, 29, 30])).all()

    left = ini_default.element[["Si", "Fe"]].isotopes_a
    right = [
        np.array([28, 29, 30]),
        np.array([54, 56, 57, 58]),
    ]
    assert all([(i == j).all() for i, j in zip(left, right)])


def test_isotopes_relative_abundance(ini_default):
    """Test isotope relative abundance returner"""
    assert (
        ini_default.element["Si"].isotopes_relative_abundance
        == np.array([0.9223, 0.04683, 0.03087])
    ).all()

    left = ini_default.element[["Si", "Fe"]].isotopes_relative_abundance
    right = [
        np.array([0.9223, 0.04683, 0.03087]),
        np.array([0.058449999999999995, 0.91754, 0.021191, 0.002819]),
    ]
    assert all([(i == j).all() for i, j in zip(left, right)])


def test_isotopes_solar_abundance(ini_default):
    """Test isotope solar abundance returner."""
    assert (
        ini_default.element["Si"].isotopes_solar_abundance
        == np.array([922000.0, 46800.0, 30900.0])
    ).all()

    left = ini_default.element[["Si", "Fe"]].isotopes_solar_abundance
    right = [
        np.array([922000.0, 46800.0, 30900.0]),
        np.array([49600.0, 778000.0, 18000.0, 2390.0]),
    ]
    assert all([(i == j).all() for i, j in zip(left, right)])


def test_isotopes_solar_abundance_nan(ini_nist):
    """Test isotope solar abundance returner when not available."""
    # make sure np.nan is returned for other databases
    assert np.isnan(ini_nist.element["Si"].isotopes_solar_abundance).all()

    val = ini_nist.element[["Si", "Fe"]].isotopes_solar_abundance
    assert all([np.isnan(it).all() for it in val])


def test_solar_abundance(ini_default):
    """Test solar abundance property."""
    assert ini_default.element["Si"].solar_abundance == 999700.0
    assert (
        ini_default.element[["Fe", "Ni"]].solar_abundance
        == np.array([847990.0, 49093.0])
    ).all()


def test_solar_abundance_nan(ini_nist):
    """Test solar abundance property when not available."""
    assert np.isnan(ini_nist.element["Si"].solar_abundance)
    assert np.isnan(ini_nist.element[["Si", "Fe", "Ni"]].solar_abundance).all()
