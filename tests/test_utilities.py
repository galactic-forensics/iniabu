"""Test suite for ``utilities.py``."""

import copy

from hypothesis import given, strategies as st
import numpy as np
import pytest

from iniabu import ini
import iniabu.data
import iniabu.elements
import iniabu.utilities
from iniabu.utilities import (
    make_isotope_dictionary,
    make_log_abundance_dictionaries,
    make_mass_fraction_dictionary,
    return_as_ndarray,
    return_list_simplifier,
    return_string_as_list,
)


def test_proxy_list_index_error(ini_default):
    """Test ProxyList with invalid element."""
    # entry not in list
    item = "invalid"
    with pytest.raises(IndexError) as err_info:
        ini_default.element[item]
    err_msg = err_info.value.args[0]
    assert (
        err_msg
        == f"Item {item} out of range. Must be in {ini_default._ele_dict.keys()}."
    )


def test_proxy_list_tuple_initialization(ini_default):
    """Test initialization of ProxyList with tuple."""
    # elements to test for
    elements = ("Fe", "Ni")
    # expected result
    val_exp = np.empty(len(elements))
    for it, ele in enumerate(elements):
        val_exp[it] = iniabu.data.lodders09_elements[ele][0]
    # result from routine to be tested
    val_get = ini_default.element[elements].solar_abundance
    np.testing.assert_equal(val_exp, val_get)


def test_proxy_list_generator(ini_default):
    """Test that generator of ProxyList returns the correct object type."""
    gen = ini_default.element.__iter__()
    val = next(gen)
    assert isinstance(val, iniabu.elements.Elements)


def test_proxy_list_length(ini_default):
    """Test that length of the ProxyList."""
    # test proxy list length
    length = len(ini_default.ele_dict.keys())
    assert ini.element.__len__() == length


@given(abu_x=st.floats(min_value=0.001, allow_infinity=False))
def test_make_isotope_dictionary(abu_x):
    """Create an isotope dictionary form an elementary dictionary."""
    ele_dict = {
        "H": [10000.0, [1, 2], [0.8, 0.2], [8000.0, 2000.0]],
        "X": [abu_x, [10], [1.0], [abu_x]],
    }
    iso_dict_expected = {
        "H-1": [0.8, 8000.0],
        "H-2": [0.2, 2000.0],
        "X-10": [1.0, abu_x],
    }
    assert make_isotope_dictionary(ele_dict) == iso_dict_expected


@given(abu_x=st.floats(min_value=0.001, allow_infinity=False))
def test_make_log_abundance_dictionaries(abu_x):
    """Ensure that logarithmic abundance dictionaries are made in correct form."""
    ele_dict_lin = {
        "H": [10000.0, [1, 2], [0.8, 0.2], [8000.0, 2000.0]],
        "X": [abu_x, [10], [1.0], [abu_x]],
    }
    # get logarithmic dictionaries
    ele_dict_log, iso_dict_log = make_log_abundance_dictionaries(ele_dict_lin)
    # assert elements
    abu_h = ele_dict_lin["H"][0]
    assert ele_dict_log["H"][0] == 12.0
    assert ele_dict_log["X"][0] == np.log10(abu_x / abu_h) + 12.0
    assert ele_dict_log["H"][3][0] == np.log10(0.8) + 12.0
    assert ele_dict_log["H"][3][1] == np.log10(0.2) + 12.0
    # assert isotopes
    assert iso_dict_log["H-1"][1] == np.log10(0.8) + 12.0
    assert iso_dict_log["H-2"][1] == np.log10(0.2) + 12.0
    assert iso_dict_log["X-10"][1] == np.log10(abu_x / abu_h) + 12.0


def test_make_mass_fraction_dictionaries():
    """Ensure that mass fraction dictionaries are made in correct form."""
    ele_dict = {
        "H": [10000.0, [1, 2], [0.8, 0.2], [8000.0, 2000.0]],
        "He": [200.0, [3, 4], [0.01, 0.99], [2.0, 198.0]],
    }
    # create mass fraction dictionary that is expected
    all_sum = 0.0
    for key in ele_dict.keys():
        for it, iso in enumerate(ele_dict[key][1]):
            all_sum += iniabu.data.isotopes_mass[f"{key}-{iso}"] * ele_dict[key][3][it]
    ele_dict_expected = {
        "H": [
            None,
            [1, 2],
            [0.8, 0.2],
            [
                8000.0 * iniabu.data.isotopes_mass["H-1"] / all_sum,
                2000.0 * iniabu.data.isotopes_mass["H-2"] / all_sum,
            ],
        ],
        "He": [
            None,
            [3, 4],
            [0.01, 0.99],
            [
                2.0 * iniabu.data.isotopes_mass["He-3"] / all_sum,
                198.0 * iniabu.data.isotopes_mass["He-4"] / all_sum,
            ],
        ],
    }
    # add element abundances
    ele_dict_expected["H"][0] = sum(ele_dict_expected["H"][3])
    ele_dict_expected["He"][0] = sum(ele_dict_expected["He"][3])
    # isotope dict expected
    iso_dict_expected = make_isotope_dictionary(ele_dict_expected)
    # test
    ele_dict_gotten, iso_dict_gotten = make_mass_fraction_dictionary(ele_dict)
    assert ele_dict_gotten == ele_dict_expected
    assert iso_dict_gotten == iso_dict_expected


def test_make_mass_fraction_dictionaries_ele_dict_untouched():
    """Ensure that mass_fraction_dictionary routine does not overwrite input.

    This simply makes sure that a deepcopy is made and not just a simple copy for the
    dictionary. Will trigger elsewhere too, however, this test is better and faster
    to recognize the problem with deepcopy versus copy.
    """
    ele_dict = {
        "H": [10000.0, [1, 2], [0.8, 0.2], [8000.0, 2000.0]],
        "He": [200.0, [3, 4], [0.01, 0.99], [2.0, 198.0]],
    }
    ele_dict_backup = copy.deepcopy(ele_dict)
    # run the routine
    _ = make_mass_fraction_dictionary(ele_dict)
    assert ele_dict == ele_dict_backup


@given(value=st.floats(allow_nan=False))
def test_return_number_as_ndarray_number(value):
    """Turn number into a ndarray."""
    assert (return_as_ndarray(value) == np.array(value)).all()


@given(value=st.floats(allow_nan=False))
def test_return_number_as_ndarray_list(value):
    """Turn number into a ndarray."""
    assert (return_as_ndarray(value) == np.array(value)).all()


@given(value=st.lists(st.floats(allow_nan=False), min_size=2))
def test_return_number_as_ndarray_list_vals(value):
    """Turn number into a ndarray."""
    assert (return_as_ndarray(value) == np.array(value)).all()


@given(value=st.lists(st.floats(allow_nan=False), min_size=2))
def test_return_number_as_ndarray_ndarray(value):
    """Turn number into a ndarray."""
    arr = np.array(value)
    assert (return_as_ndarray(arr) == arr).all()


@given(
    value=st.text(
        alphabet=st.characters(blacklist_characters="\n", blacklist_categories=("Cs",))
    )
)
def test_return_string_as_list_string(value):
    """Ensures a string is turned into a list."""
    assert return_string_as_list(value) == [value]


@given(
    value=st.lists(
        st.text(
            alphabet=st.characters(
                blacklist_characters="\n", blacklist_categories=("Cs",)
            )
        ),
        min_size=2,
    )
)
def test_return_string_as_list_list(value):
    """Ensures a list stays a list."""
    assert return_string_as_list(value) == value


@given(
    value_single=st.lists(st.floats(allow_nan=False), min_size=1, max_size=1),
    value_arr=st.lists(st.floats(allow_nan=False), min_size=2),
)
def test_return_value_simplifier(value_single, value_arr):
    """Test return value simplifier routine."""
    assert return_list_simplifier([]) is None
    assert return_list_simplifier(value_single) == value_single[0]
    assert return_list_simplifier(value_arr) == value_arr
