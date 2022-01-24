"""Test suite for ``main.py``, internal normalization calculations."""

from hypothesis import given, strategies as st
import numpy as np
import pytest

from iniabu.utilities import get_all_stable_isos


# INTERNAL NORMALIZATION #


@pytest.mark.parametrize("law", ("exp", "lin"))
def test_iso_int_norm_zeros(ini_default, law):
    """Normalization isotopes return zero for internal normalization."""
    isos = ("Ni-58", "Ni-62")
    norm_isos = isos
    smp_values = (0.1, 0.3)
    norm_values = smp_values

    # do internal normalization
    retval = ini_default.iso_int_norm(isos, norm_isos, smp_values, norm_values, law=law)

    assert retval == pytest.approx(0, abs=1e-6)


@given(
    smp_value=st.floats(min_value=0, allow_infinity=False),
    smp_norm_values=st.tuples(
        st.floats(min_value=1e-50, max_value=1e50),
        st.floats(min_value=1e-50, max_value=1e50),
    ),
)
def test_iso_int_norm_exp_single(ini_default, smp_value, smp_norm_values):
    """Internal normalization using exponential law for one isotope, one value."""
    nominator_iso = "Ni-62"
    norm_isos = ("Ni-58", "Ni-60")

    # masses
    mass_nominator = ini_default.iso[nominator_iso].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # isotope ratios solar system
    iso_ratio_solar_norm = ini_default.iso_ratio(norm_isos[1], norm_isos[0])
    iso_ratio_solar = ini_default.iso_ratio(nominator_iso, norm_isos[0])

    # exponential law
    beta = np.log10(
        smp_norm_values[1] / smp_norm_values[0] / iso_ratio_solar_norm
    ) / np.log10(mass_norm_isos[1] / mass_norm_isos[0])
    corrected_ratio = (
        smp_value / smp_norm_values[0] / (mass_nominator / mass_norm_isos[0]) ** beta
    )
    retval_expected = (corrected_ratio / iso_ratio_solar - 1) * 10000

    retval_gotten = ini_default.iso_int_norm(
        nominator_iso, norm_isos, smp_value, smp_norm_values
    )
    assert retval_gotten == pytest.approx(retval_expected)


@given(
    smp_value=st.floats(min_value=0, allow_infinity=False),
    smp_norm_values=st.tuples(
        st.floats(min_value=1e-50, max_value=1e50),
        st.floats(min_value=1e-50, max_value=1e50),
    ),
)
def test_iso_int_norm_lin_single(ini_default, smp_value, smp_norm_values):
    """Internal normalization using linear law for one isotope, one value."""
    nominator_iso = "Ni-60"
    norm_isos = ("Ni-62", "Ni-61")

    # masses
    mass_nominator = ini_default.iso[nominator_iso].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # delta values for the sample and normalization
    delta_value_norm = ini_default.iso_delta(
        norm_isos[1],
        norm_isos[0],
        smp_norm_values[1] / smp_norm_values[0],
        delta_factor=10000,
    )
    delta_value_smp = ini_default.iso_delta(
        nominator_iso, norm_isos[0], smp_value / smp_norm_values[0], delta_factor=10000
    )
    # mass correction factor
    corr_fac = (mass_norm_isos[0] - mass_nominator) / (
        mass_norm_isos[0] - mass_norm_isos[1]
    )

    retval_expected = delta_value_smp - corr_fac * delta_value_norm

    if retval_expected < -10000:
        retval_expected = -10000.0

    retval_gotten = ini_default.iso_int_norm(
        nominator_iso, norm_isos, smp_value, smp_norm_values, law="lin"
    )
    assert retval_gotten == pytest.approx(retval_expected)


@given(delta_fct=st.floats(min_value=0, allow_infinity=False))
def test_iso_int_norm_exp_single_delta(ini_default, delta_fct):
    """Internal normalization using exponential law for different delta."""
    nominator_iso = "Ni-62"
    norm_isos = ("Ni-58", "Ni-60")

    # sample values
    smp_value = 3.0
    smp_norm_values = (0.1, 0.2)

    # masses
    mass_nominator = ini_default.iso[nominator_iso].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # isotope ratios solar system
    iso_ratio_solar_norm = ini_default.iso_ratio(norm_isos[1], norm_isos[0])
    iso_ratio_solar = ini_default.iso_ratio(nominator_iso, norm_isos[0])

    # exponential law
    beta = np.log10(
        smp_norm_values[1] / smp_norm_values[0] / iso_ratio_solar_norm
    ) / np.log10(mass_norm_isos[1] / mass_norm_isos[0])
    corrected_ratio = (
        smp_value / smp_norm_values[0] / (mass_nominator / mass_norm_isos[0]) ** beta
    )
    retval_expected = (corrected_ratio / iso_ratio_solar - 1) * delta_fct

    retval_gotten = ini_default.iso_int_norm(
        nominator_iso, norm_isos, smp_value, smp_norm_values, delta_factor=delta_fct
    )
    assert retval_gotten == pytest.approx(retval_expected)


@given(
    smp_values=st.tuples(
        st.floats(min_value=1e-50, max_value=1e50),  # Ni-58
        st.floats(min_value=0, max_value=1e50),  # Ni-60
        st.floats(min_value=0, max_value=1e50),  # Ni-61
        st.floats(min_value=1e-50, max_value=1e50),  # Ni-62
        st.floats(min_value=0, max_value=1e50),  # Ni-64
    )
)
def test_iso_int_norm_exp_multi_isos(ini_default, smp_values):
    """Internal normalization using exponential law for multiple isotopes."""
    nominator_ele = "Ni"
    nominator_isos = get_all_stable_isos(ini_default, nominator_ele)
    norm_isos_ind = (0, 3)
    norm_isos = (nominator_isos[norm_isos_ind[0]], nominator_isos[norm_isos_ind[1]])
    smp_values = np.array(smp_values)
    smp_norm_values = np.array([smp_values[0], smp_values[3]])

    # masses
    mass_nominator = ini_default.iso[nominator_isos].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # isotope ratios solar system
    iso_ratio_solar_norm = ini_default.iso_ratio(norm_isos[1], norm_isos[0])
    iso_ratio_solar = ini_default.iso_ratio(nominator_isos, norm_isos[0])

    # exponential law
    beta = np.log10(
        smp_norm_values[1] / smp_norm_values[0] / iso_ratio_solar_norm
    ) / np.log10(mass_norm_isos[1] / mass_norm_isos[0])
    corrected_ratio = (
        smp_values / smp_norm_values[0] / (mass_nominator / mass_norm_isos[0]) ** beta
    )
    retval_expected = (corrected_ratio / iso_ratio_solar - 1) * 10000

    retval_gotten = ini_default.iso_int_norm(
        nominator_ele, norm_isos, smp_values, smp_norm_values
    )
    assert retval_gotten == pytest.approx(retval_expected)


@given(
    smp_values=st.tuples(
        st.floats(min_value=1e-50, max_value=1e50),  # Ni-58
        st.floats(min_value=0, max_value=1e50),  # Ni-60
        st.floats(min_value=0, max_value=1e50),  # Ni-61
        st.floats(min_value=1e-50, max_value=1e50),  # Ni-62
        st.floats(min_value=0, max_value=1e50),  # Ni-64
    )
)
def test_iso_int_norm_lin_multi(ini_default, smp_values):
    """Internal normalization using linear law for multiple isotopes."""
    nominator_ele = "Ni"
    nominator_isos = get_all_stable_isos(ini_default, nominator_ele)
    norm_isos_ind = (0, 3)
    norm_isos = (nominator_isos[norm_isos_ind[0]], nominator_isos[norm_isos_ind[1]])
    smp_values = np.array(smp_values)
    smp_norm_values = np.array([smp_values[0], smp_values[3]])

    # masses
    mass_nominator = ini_default.iso[nominator_isos].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # delta values for the sample and normalization
    delta_value_norm = ini_default.iso_delta(
        norm_isos[1],
        norm_isos[0],
        smp_norm_values[1] / smp_norm_values[0],
        delta_factor=10000,
    )
    delta_value_smp = ini_default.iso_delta(
        nominator_isos,
        norm_isos[0],
        smp_values / smp_norm_values[0],
        delta_factor=10000,
    )
    # mass correction factor
    corr_fac = (mass_norm_isos[0] - mass_nominator) / (
        mass_norm_isos[0] - mass_norm_isos[1]
    )

    retval_expected = delta_value_smp - corr_fac * delta_value_norm

    for it, val in enumerate(retval_expected):
        if val < -10000:
            retval_expected[it] = -10000.0

    retval_gotten = ini_default.iso_int_norm(
        nominator_ele, norm_isos, smp_values, smp_norm_values, law="lin"
    )
    assert retval_gotten == pytest.approx(retval_expected)


def test_iso_int_norm_exp_multi_values(ini_default):
    """Internal normalization using exponential law for one isotope, multiple value."""
    nominator_iso = "Ni-60"
    norm_isos = ("Ni-58", "Ni-62")

    # sample values - enough hypothesis already
    smp_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    smp_norm_values = np.array([10.0, 2.0])

    # masses
    mass_nominator = ini_default.iso[nominator_iso].mass
    mass_norm_isos = ini_default.iso[norm_isos].mass

    # isotope ratios solar system
    iso_ratio_solar_norm = ini_default.iso_ratio(norm_isos[1], norm_isos[0])
    iso_ratio_solar = ini_default.iso_ratio(nominator_iso, norm_isos[0])

    # exponential law
    beta = np.log10(
        smp_norm_values[1] / smp_norm_values[0] / iso_ratio_solar_norm
    ) / np.log10(mass_norm_isos[1] / mass_norm_isos[0])
    corrected_ratio = (
        smp_values / smp_norm_values[0] / (mass_nominator / mass_norm_isos[0]) ** beta
    )
    retval_expected = (corrected_ratio / iso_ratio_solar - 1) * 10000

    retval_gotten = ini_default.iso_int_norm(
        nominator_iso, norm_isos, smp_values, smp_norm_values
    )
    assert retval_gotten == pytest.approx(retval_expected)


def test_iso_int_norm_input_mismatch(ini_default):
    """Raise ValueError input values are mismatched."""
    nominator_iso = "Ni"
    norm_isos = ("Ni-58", "Ni-62")

    # sample values - enough hypothesis already
    smp_value = 1.0
    smp_norm_values = np.array([10.0, 2.0])

    bad_law = "tmp"

    with pytest.raises(ValueError) as err_info:
        _ = ini_default.iso_int_norm(
            nominator_iso, norm_isos, smp_value, smp_norm_values, law=bad_law
        )
    err_msg = err_info.value.args[0]
    assert (
        err_msg == "Length of requested isotope ratios does not match length of "
        "provided values."
    )


def test_iso_int_norm_unlawful(ini_default):
    """Raise ValueError if wrong law is selected."""
    nominator_iso = "Ni-60"
    norm_isos = ("Ni-58", "Ni-62")

    # sample values - enough hypothesis already
    smp_value = 1.0
    smp_norm_values = np.array([10.0, 2.0])

    bad_law = "tmp"

    with pytest.raises(ValueError) as err_info:
        _ = ini_default.iso_int_norm(
            nominator_iso, norm_isos, smp_value, smp_norm_values, law=bad_law
        )
    err_msg = err_info.value.args[0]
    assert (
        err_msg == f"The selected law {bad_law} is invalid. Please select either "
        f"'exp' for an exponential law or 'lin' for a linear law."
    )
