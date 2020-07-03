import iniabu.data as data
import pytest
import numpy as np


def test_lodders09_elements():
    """
    Test lodders09 elements dictionary
    """
    # type check
    assert isinstance(data.lodders09_elements, dict)

    # entry tests
    assert data.lodders09_elements["Fe"] == [
        847990.0,
        [54, 56, 57, 58],
        [0.058449999999999995, 0.91754, 0.021191, 0.002819],
        [49600.0, 778000.0, 18000.0, 2390.0],
    ]
    assert data.lodders09_elements["Mo"] == [
        2.549,
        [92, 94, 95, 96, 97, 98, 100],
        [0.14525, 0.09151, 0.15838, 0.16672, 0.09599, 0.24391, 0.09824],
        [0.37, 0.233, 0.404, 0.425, 0.245, 0.622, 0.25],
    ]

    # non-existent entry
    with pytest.raises(KeyError):
        data.lodders09_elements["Sj"]

    # test si29 is equal to 1e6 within 1000
    assert data.lodders09_elements["Si"][0] == pytest.approx(1e6, 1000)

    # test sum of abundances is equal to 1
    for element in data.lodders09_elements.keys():
        abu_sum = np.array(data.lodders09_elements[element][2]).sum()
        assert abu_sum == pytest.approx(1.0, 0.001)


def test_lodders09_isotopes():
    """
    Test lodders09 isotopes dictionary
    """
    # type check
    assert isinstance(data.lodders09_isotopes, dict)

    # data check
    assert data.lodders09_isotopes["Si-28"] == [0.9223, 9.22e05]
    assert data.lodders09_isotopes["U-238"] == [0.75712, 0.0180]

    # non-existent entry
    with pytest.raises(KeyError):
        data.lodders09_isotopes["Sj"]
