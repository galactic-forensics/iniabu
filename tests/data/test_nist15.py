"""Test suite for ``data/nist15.py``."""

import numpy as np
import pytest

import iniabu.data as data


def test_elements_mass_type_check():
    """Test the nist15 elements_mass dictionary type."""
    assert isinstance(data.elements_mass, dict)


def test_elements_mass_data_check():
    """Test the nist15 elements_mass dictionary data."""
    assert data.elements_mass["Fe"] == 55.845144433865904
    assert data.elements_mass["Lv"] is np.nan


def test_elements_mass_data_na():
    """Test the nist15 elements_mass dictionary data that do not exist."""
    with pytest.raises(KeyError):
        data.elements_mass["Sj"]


def test_elements_z_type_check():
    """Test the nist15 elements_z dictionary type."""
    assert isinstance(data.elements_z, dict)


def test_elements_z_data_check():
    """Test the nist15 elements_z dictionary data."""
    assert data.elements_z["Ne"] == 10
    assert data.elements_z["Pt"] == 78


def test_elements_z_data_na():
    """Test the nist15 elements_z dictionary data that do not exist."""
    with pytest.raises(KeyError):
        data.elements_z["Sj"]


def test_nist15_isotopes_mass_type_check():
    """Test nist15 isotopes_mass dictionary type check."""
    assert isinstance(data.isotopes_mass, dict)


def test_nist15_isotopes_mass_data_check():
    """Test nist15 isotopes_mass dictionary data."""
    assert data.isotopes_mass["Ti-48"] == 47.94794198
    assert data.isotopes_mass["Tc-98"] == 97.9072124


def test_nist15_isotopes_mass_data_na():
    """Test nist15 isotopes_mass dictionary data not available."""
    with pytest.raises(KeyError):
        data.isotopes_mass["Sj-28"]


def test_nist15_elements_type_check():
    """Test nist15 elements dictionary type."""
    assert isinstance(data.nist15_elements, dict)


def test_nist15_elements_data_check():
    """Test nist15 elements dictionary data."""
    assert data.nist15_elements["H"] == [
        np.nan,
        [1, 2, 3],
        [0.999885, 0.000115, 0.0],
        [np.nan, np.nan, np.nan],
    ]
    assert data.nist15_elements["Lv"] == [np.nan, [293], [0.0], [np.nan]]


def test_nist15_elements_data_na():
    """Test nist15 elements dictionary not available entry."""
    with pytest.raises(KeyError):
        data.nist15_elements["Sj"]


def test_nist15_elements_si_normalization():
    """Test that Si is normed to 1e6."""
    for element in data.nist15_elements.keys():
        abu_sum = np.array(data.nist15_elements[element][2]).sum()
        assert abu_sum == pytest.approx(1.0, 0.001) or abu_sum == 0.0


def test_nist15_isotopes_type_check():
    """Test nist15 isotopes dictionary type check."""
    assert isinstance(data.nist15_elements, dict)


def test_nist15_isotopes_data_check():
    """Test nist15 isotopes dictionary data."""
    assert data.nist15_isotopes["Sc-45"] == [1.0, np.nan]
    assert data.nist15_isotopes["U-238"] == [0.992742, np.nan]


def test_nist15_isotopes_data_na():
    """Test nist15 isotopes dictionary data not available."""
    with pytest.raises(KeyError):
        data.nist15_isotopes["Sj-29"]
