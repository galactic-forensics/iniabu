import iniabu.data as data
import pytest
import numpy as np


def test_elements_mass():
    """
    Test the nist15 elements_mass dictionary
    """
    # type check
    assert isinstance(data.elements_mass, dict)

    # data check
    assert data.elements_mass["Fe"] == 55.845144433865904
    assert data.elements_mass["Lv"] is np.nan

    # non-existent entry
    with pytest.raises(KeyError):
        data.elements_mass["Sj"]


def test_elements_z():
    """
    Test the nist15 elements_z dictionary
    """
    # type check
    assert isinstance(data.elements_z, dict)

    # data check
    assert data.elements_z["Ne"] == 10
    assert data.elements_z["Pt"] == 78

    # non-existent entry
    with pytest.raises(KeyError):
        data.elements_z["Sj"]


def test_isotopes_mass():
    """
    Test the nist15 isotopes_mass dictionary
    """
    # type check
    assert isinstance(data.isotopes_mass, dict)

    # data check
    assert data.isotopes_mass["Ti-48"] == 47.94794198
    assert data.isotopes_mass["Tc-98"] == 97.9072124

    # non-existent entry
    with pytest.raises(KeyError):
        data.isotopes_mass["Sj-28"]


def test_nist15_elements():
    """
    Test the nist15 element dictionary
    """
    # type check
    assert isinstance(data.nist15_elements, dict)

    # data tests
    assert data.nist15_elements["H"] == [
        np.nan,
        [1, 2, 3],
        [0.999885, 0.000115, 0.0],
        [np.nan, np.nan, np.nan],
    ]
    assert data.nist15_elements["Lv"] == [np.nan, [293], [0.0], [np.nan]]

    # non-existent entry
    with pytest.raises(KeyError):
        data.nist15_elements["Sj"]

    # test sum of abundances is equal to 1 or 0 (for radioactive-only elements)
    for element in data.nist15_elements.keys():
        abu_sum = np.array(data.nist15_elements[element][2]).sum()
        assert abu_sum == pytest.approx(1.0, 0.001) or abu_sum == 0.0


def test_nist15_isotopes():
    """
    Test the nist15 isotope dictionary
    """
    # type check
    assert isinstance(data.nist15_elements, dict)

    # data atests
    assert data.nist15_isotopes["Sc-45"] == [1.0, np.nan]
    assert data.nist15_isotopes["U-238"] == [0.992742, np.nan]

    # non-existent entry
    with pytest.raises(KeyError):
        data.nist15_isotopes["Sj-29"]
