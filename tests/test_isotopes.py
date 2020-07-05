"""Test suite for ``isotopes.py``."""

import numpy as np
import pytest

import iniabu
import iniabu.isotopes


def test_isotopes_require_parent_class():
    """Test that class requires an appropriate parent class."""
    with pytest.raises(TypeError):
        iniabu.isotopes.Isotopes(None, None)


def test_isotopes_isos_list(ini_default):
    """Test that the isotope list is correctly initialized."""
    assert ini_default.isotope["Si-28"]._isos == ["Si-28"]
    assert ini_default.isotope[["Fe-54", "Ni-58"]]._isos == ["Fe-54", "Ni-58"]


def test_relative_abundance(ini_default):
    """Test isotope relative abundance returner."""
    assert ini_default.isotope["Si-29"].relative_abundance == 0.04683
    assert (
        ini_default.isotope[["Si-29", "Ni-64"]].relative_abundance
        == np.array([0.04683, 0.009256])
    ).all()


def test_solar_abundance(ini_default):
    """Test isotope solar abundance returner."""
    # test valid values
    assert ini_default.isotope["Si-29"].solar_abundance == 46800.0
    assert (
        ini_default.isotope[["Si-29", "Ni-64"]].solar_abundance
        == np.array([46800.0, 454.0])
    ).all()


def test_solar_abundance_nan(ini_nist):
    """Test isotope solar abundance returner if not available."""
    # check with database that does not contain this
    assert np.isnan(ini_nist.isotope["Si-29"].solar_abundance)
    assert np.isnan(ini_nist.isotope[["Si-29", "Ni-64"]].solar_abundance).all()
