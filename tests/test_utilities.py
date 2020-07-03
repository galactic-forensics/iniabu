from iniabu import ini
import iniabu.elements
import iniabu.utilities
from iniabu.utilities import return_value_simplifier

import numpy as np
import pytest


def test_proxy_list():
    """Test the whole ProxyList class"""
    # entry not in list
    with pytest.raises(IndexError):
        val = ini.element["invalid"]

    # make sure initialization with tuple works
    val = ini.element[("Fe", "Ni")].solar_abundance
    assert (val == np.array([717133.4154099999, 26195.732864999998])).all()

    # ensure that the generator of the proxy list returns the correct object type
    gen = ini.element.__iter__()
    val = next(gen)
    assert isinstance(val, iniabu.elements.Elements)

    # test proxy list length
    length = len(ini.ele_dict.keys())
    assert ini.element.__len__() == length


def test_return_value_simplifier():
    """Test return value simplifier routine. This is not a property of the class"""
    assert return_value_simplifier([]) is None
    assert return_value_simplifier([3.14]) == 3.14
    assert return_value_simplifier([1, 2, 3]) == [1, 2, 3]
