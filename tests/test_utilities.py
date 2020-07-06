"""Test suite for ``utilities.py``."""

import numpy as np
import pytest

from iniabu import ini
import iniabu.elements
import iniabu.utilities
from iniabu.utilities import make_log_abundance_dictionaries, return_value_simplifier


def test_proxy_list_index_error(ini_default):
    """Test ProxyList with invalid element."""
    # entry not in list
    with pytest.raises(IndexError):
        ini_default.element["invalid"]


def test_proxy_list_tuple_initialization(ini_default):
    """Test initialization of ProxyList with tuple."""
    val = ini_default.element[("Fe", "Ni")].solar_abundance
    assert (val == np.array([847990.0, 49093.0])).all()


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


def test_make_log_abundance_dictionaries():
    """Ensure that logarithmic abundance dictionaries are made in correct form."""
    ele_dict_lin = {
        "H": [10000.0, [1, 2], [0.8, 0.2], [8000.0, 2000.0]],
        "X": [1000.0, [10], [1.0], [1000.0]],
    }
    # get logarithmic dictionaries
    ele_dict_log, iso_dict_log = make_log_abundance_dictionaries(ele_dict_lin)
    # assert elements
    assert ele_dict_log["H"][0] == 12.0
    assert ele_dict_log["X"][0] == np.log10(0.1) + 12.0
    assert ele_dict_log["H"][3][0] == np.log10(0.8) + 12.0
    assert ele_dict_log["H"][3][1] == np.log10(0.2) + 12.0
    # assert isotopes
    assert iso_dict_log["H-1"][1] == np.log10(0.8) + 12.0
    assert iso_dict_log["H-2"][1] == np.log10(0.2) + 12.0
    assert iso_dict_log["X-10"][1] == np.log10(0.1) + 12.0


def test_return_value_simplifier():
    """Test return value simplifier routine."""
    assert return_value_simplifier([]) is None
    assert return_value_simplifier([3.14]) == 3.14
    assert return_value_simplifier([1, 2, 3]) == [1, 2, 3]
