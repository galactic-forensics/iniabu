import iniabu.data as data
import pytest
import numpy as np


def test_asplund09_elements():
    """
    Test asplund09 elements dictionary
    """
    # type check
    assert isinstance(data.asplund09_elements, dict)

    # entry tests
    assert data.asplund09_elements["Fe"] == [
        977237.2209558112,
        [54, 56, 57, 58],
        [0.058449999999999995, 0.91754, 0.02119, 0.0028199999999999996],
        [
            57119.51556486716,
            896654.239715795,
            20707.65671205364,
            2755.8089630953873,
        ],
    ]
    assert data.asplund09_elements["Mo"] == [
        2.3442288153199176,
        [92, 94, 95, 96, 97, 98, 100],
        [0.14525, 0.09151, 0.15838, 0.16672, 0.09599, 0.24391, 0.09824],
        [
            0.340499235425218,
            0.21452037888992564,
            0.3712789597703685,
            0.39082982809013667,
            0.2250225239825589,
            0.5717808503446811,
            0.23029703881702868,
        ],
    ]

    # non-existent entry
    with pytest.raises(KeyError):
        data.asplund09_elements["Sj"]

    # test si29 is equal to 1e6 within 1000
    assert data.asplund09_elements["Si"][0] == pytest.approx(1e6, 1000)

    # test sum of abundances is equal to 1
    for element in data.asplund09_elements.keys():
        abu_sum = np.array(data.asplund09_elements[element][2]).sum()
        assert abu_sum == pytest.approx(1.0, 0.001)


def test_asplund09_isotopes():
    """
    Test asplund09 isotopes dictionary
    """
    # type check
    assert isinstance(data.asplund09_isotopes, dict)

    # data check
    assert data.asplund09_isotopes["Si-28"] == [
        0.9222969999999999,
        922296.9999999999,
    ]
    assert data.asplund09_isotopes["U-238"] == [0.75712, np.nan]

    # non-existent entry
    with pytest.raises(KeyError):
        data.asplund09_isotopes["Sj"]
