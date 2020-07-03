import iniabu
import iniabu.isotopes
from iniabu import ini

import numpy as np
import pytest


def test_isotopes():
    """Test class initialization"""
    # Parent class testing
    with pytest.raises(TypeError):
        iniabu.isotopes.Isotopes(None, None)

    assert ini.isotope["Si-28"]._isos == ["Si-28"]
    assert ini.isotope[["Fe-54", "Ni-58"]]._isos == ["Fe-54", "Ni-58"]


def test_relative_abundance():
    """Test isotope relative abundance returner"""
    assert ini.isotope["Si-29"].relative_abundance == 0.04683
    assert (
        ini.isotope[["Si-29", "Ni-64"]].relative_abundance
        == np.array([0.04683, 0.009256])
    ).all()


def test_solar_abundance():
    """Test isotope relative abundance returner"""
    # test valid values
    assert ini.isotope["Si-29"].solar_abundance == 46800.0
    assert (
        ini.isotope[["Si-29", "Ni-64"]].solar_abundance
        == np.array([46800.0, 454.0])
    ).all()

    # check with database that does not contain this
    ini2 = iniabu.IniAbu(database="nist")
    assert np.isnan(ini2.isotope["Si-29"].solar_abundance)
    assert np.isnan(ini2.isotope[["Si-29", "Ni-64"]].solar_abundance).all()
