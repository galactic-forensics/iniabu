"""Test suite for ``main.py``."""

import numpy as np
import pytest

import iniabu
import iniabu.data as data


def test_init_database_default(ini_default):
    """Load iniabu with default database."""
    assert ini_default._ele_dict == data.lodders09_elements
    assert ini_default._iso_dict == data.lodders09_isotopes
    assert ini_default.database == "lodders09"


def test_init_database_nist(ini_nist):
    """Load iniabu with nist database."""
    assert ini_nist._ele_dict == data.nist15_elements
    assert ini_nist._iso_dict == data.nist15_isotopes
    assert ini_nist.database == "nist"


def test_init_database_asplund():
    """Load iniabu with asplund database."""
    ini = iniabu.IniAbu(database="asplund09")
    assert ini._ele_dict == data.asplund09_elements
    assert ini._iso_dict == data.asplund09_isotopes
    assert ini.database == "asplund09"


def test_init_database_invalid(ini_nist):
    """Initialize with invalid database name."""
    with pytest.raises(ValueError):
        iniabu.IniAbu(database="not-valid-database")


def test_ele_dict(ini_default):
    """Return the elementary dictionary."""
    assert ini_default.ele_dict == data.lodders09_elements


def test_abundance_unit_default(ini_default):
    """Ensure that standard abundance unit is linear."""
    assert ini_default.abundance_unit == "lin"


def test_abundance_unit_log(ini_default):
    """Ensure logarithmic abundance unit is set correctly."""
    ini_default.abundance_unit = "log"
    assert ini_default.abundance_unit == "log"
    assert ini_default.element["H"].solar_abundance == 12.0


def test_abundance_unit_log_lin(ini_default):
    """Ensure linear abundance unit is set correctly after logarithmic (switch back)."""
    ini_default.abundance_unit = "log"
    ini_default.abundance_unit = "lin"
    assert ini_default.abundance_unit == "lin"
    assert ini_default.element["Si"].solar_abundance == pytest.approx(1e6, 1000.0)


def test_abundance_unit_after_new_database(ini_default):
    """Ensure abundance unit is reset to linear when new database is loaded."""
    ini_default.abundance_unit = "log"
    ini_default.database = "lodders09"
    assert ini_default.abundance_unit == "lin"
    assert ini_default.element["Si"].solar_abundance == pytest.approx(1e6, 1000.0)


def test_bracket_element(ini_default):
    """Calculate bracket notation for an element ratio."""
    assert ini_default.bracket_element("Ne", "Si", 33) == pytest.approx(
        1.0008802726402624, 0.001
    )


def test_bracket_element_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError):
        ini_default.bracket_element(["Ne", "Mg"], ["Si", "Si"], 33)


def test_bracket_isotope(ini_default):
    """Calculate bracket notation for an isotope ratio."""
    assert ini_default.bracket_isotope("Ne-21", "Ne-20", 2.397) == pytest.approx(
        2.9999700012616572, 0.001
    )


def test_bracket_isotope_shape_mismatch(ini_default):
    """Raise Value error on shape mismatch between nd arrays."""
    with pytest.raises(ValueError):
        ini_default.bracket_isotope(["Ne-21", "Mg-25"], "Si", 33)


def test_delta_element(ini_default):
    """Calculate delta-value for an element ratio in various units."""
    assert ini_default.delta_element("Ne", "Si", 3.4) == pytest.approx(
        32.39347210030586, 0.001
    )
    assert ini_default.delta_element(
        "Fe", "Ni", 10.0, delta_factor=10.0
    ) == pytest.approx(-4.2106628615903485, 0.001)


def test_delta_element_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between nd arrays."""
    with pytest.raises(ValueError):
        ini_default.delta_element("Ne", "Si", [0.07, 0.09], delta_factor=10000)


def test_delta_isotope(ini_default):
    """Calculate delta-value for an isotope ratio in epsilon units."""
    assert ini_default.delta_isotope(
        "Ne-22", "Ne-20", 0.07, delta_factor=10000
    ) == pytest.approx(-480.0676021714623, 0.001)


def test_delta_isotope_shape_mismatch(ini_default):
    """Raise a ValueError on shape mismatch between the ndarrays."""
    with pytest.raises(ValueError):
        ini_default.delta_isotope("Ne-22", "Ne-20", [0.07, 0.09], delta_factor=10000)


def test_ratio_element_ele_ele(ini_default):
    """Calculate element ratio for element vs. element."""
    assert ini_default.ratio_element("H", "Si") == 25908.275482644793


def test_ratio_element_ele_ele_nist_db(ini_nist):
    """Calculate element ratio when not a number."""
    assert np.isnan(ini_nist.ratio_element("H", "Si"))


def test_ratio_element_ele_ele_from_log(ini_default):
    """Calculate element ratio for element vs. element."""
    ini_default.abundance_unit = "log"
    assert ini_default.ratio_element("H", "Si") == 25908.275482644793


def test_ratio_element_eles_ele(ini_default):
    """Calculate element ratio for elements vs. element."""
    assert (
        ini_default.ratio_element(["H", "He"], "Si")
        == np.array([25908.275482644793, 2511.7835350605183])
    ).all()


def test_ratio_element_eles_eles(ini_default):
    """Calculate element ratio for elements vs. elements."""
    assert (
        ini_default.ratio_element(["H", "He"], ["H", "Si"])
        == np.array([1.0, 2511.7835350605183])
    ).all()


def test_ratio_element_ele_eles_length_mismatch(ini_default):
    """Raise a ValueError if denominator has different length from nominator."""
    with pytest.raises(ValueError):
        ini_default.ratio_element("H", ["H", "Si"])


def test_ratio_element_ele_ele_mass_fraction(ini_default):
    """Calculate element ratio for element vs. element in mass fraction."""
    assert ini_default.ratio_element("H", "He", mass_fraction=True) == 40.96035314200997


def test_ratio_isotope_iso_iso(ini_default):
    """Calculate isotope ratio for one nominator and one denominator isotope."""
    assert ini_default.ratio_isotope("Ne-21", "Ne-20") == 0.0023971655776491205


def test_ratio_isotope_iso_iso_from_log(ini_default):
    """Calculate isotope ratio when database is in logarithmic state."""
    ini_default.abundance_unit = "log"
    assert ini_default.ratio_isotope("Ne-21", "Ne-20") == 0.0023971655776491205


def test_ratio_isotope_isos_iso(ini_default):
    """Calculate isotope ratio for several nominators and one denominator isotope."""
    assert (
        ini_default.ratio_isotope(["Ne-21", "Ne-22"], "Ne-20")
        == np.array([0.0023971655776491205, 0.07352993390579828])
    ).all()


def test_ratio_isotope_isos_isos(ini_default):
    """Calculate isotope ratios for several nominators and denominators."""
    assert (
        ini_default.ratio_isotope(["Ne-21", "Ne-22"], ["Ne-21", "Ne-22"])
        == np.array([1.0, 1.0])
    ).all()


def test_ratio_isotope_isos_isos_length_mismatch(ini_default):
    """Raise a ValueError if nominator and denominator have different lengths."""
    with pytest.raises(ValueError):
        ini_default.ratio_isotope(["Ne-21", "Ne-22"], ["Ne-20", "Ne-21", "Ne-22"])


def test_ratio_isotope_ele_iso(ini_default):
    """Calculae isotope ratios for all isotopes of an element versus one isotope."""
    assert (
        ini_default.ratio_isotope("Ne", "Ne-20")
        == np.array([1.0, 0.0023971655776491205, 0.07352993390579828])
    ).all()


def test_ratio_isotope_iso_iso_mass_fraction(ini_default):
    """Calculate isotope ratios for isotopes and element as mass fraction."""
    assert (
        ini_default.ratio_isotope("Ne-22", "Ne-20", mass_fraction=True)
        == 0.06684630354800906
    )


def test_ratio_isotope_isos_ele_mass_fraction(ini_default):
    """Calculate isotope ratios for isotopes and element as mass fraction."""
    assert (
        ini_default.ratio_isotope(["Ne-21", "Ne-22"], "Ne", mass_fraction=True)
        == np.array([0.0022828207770917114, 0.06684630354800906])
    ).all()


def test_ratio_isotope_iso_ele(ini_default):
    """Calculate isotope ratio for one isotope and an element (i.e., major isotope)."""
    assert ini_default.ratio_isotope("Ne-21", "Ne") == 0.0023971655776491205


def test_get_all_isotopes(ini_default):
    """Ensure appropriate isotope list is returned for a given element."""
    assert ini_default._get_all_isotopes("Si") == ["Si-28", "Si-29", "Si-30"]


def test_get_major_isotope(ini_default):
    """Ensure that the correct major isotope is returned."""
    assert ini_default._get_major_isotope("Si") == "Si-28"
