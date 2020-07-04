"""
Todo License information
"""


import numpy as np

from .utilities import return_value_simplifier


class Isotopes(object):

    """
    Class representing the isotopes. This is mainly a list to easily interact with
    the `parent._iso_dict` dictionary.

    .. warning:: This class should NOT be manually created by the user. It is
        designed to be initialized by the ``IniAbu`` class
    """

    def __init__(self, parent, isos):
        """Initialize the Isotopes class."""
        # check for correct parent
        if parent.__class__.__name__ != "IniAbu":
            raise TypeError("Isotopes class must be initialized from IniAbu.")

        # set the variables
        self._isos = isos
        self._iso_dict = parent.iso_dict

    # PROPERTIES #

    @property
    def relative_abundance(self):
        """
        Gets the relative abundances of the isotope and returns a float with the value.
        If more than one isotope is selected, an np.array<float> is returned. If solar
        abundance is not part of the database, `np.nan` is returned

        :return: Solar abundance isotope / isotopes
        :rtype: float,ndarray
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(self._iso_dict[iso][0])
        ret_arr = np.array(ret_arr)
        return return_value_simplifier(ret_arr)

    @property
    def solar_abundance(self):
        """
        Gets the solar abundances of the isotope and returns a float with the value.
        If more than one isotope is selected, an np.array<float> is returned.

        Note: All relative abundances of an elements isotope sum to unity.

        :return: Relative abundance isotope / isotopes
        :rtype: float,ndarray
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(self._iso_dict[iso][1])
        ret_arr = np.array(ret_arr)
        return return_value_simplifier(ret_arr)
