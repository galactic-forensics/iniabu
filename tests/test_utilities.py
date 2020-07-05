"""Test suite for ``utilities.py``."""

import numpy as np
import pytest

from iniabu import ini
import iniabu.elements
import iniabu.utilities
from iniabu.utilities import return_value_simplifier


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


def test_return_value_simplifier():
    """Test return value simplifier routine."""
    assert return_value_simplifier([]) is None
    assert return_value_simplifier([3.14]) == 3.14
    assert return_value_simplifier([1, 2, 3]) == [1, 2, 3]
