"""
Todo License information
"""


import numpy as np

from .utilities import return_value_simplifier


class Elements(object):

    """
    Class representing the elements. This is mainly a list to easily interact with
    the `parent._ele_dict` dictionary.

    .. warning:: This class should NOT be manually created by the user. It is
        designed to be initialized by the ``IniAbu`` class
    """

    def __init__(self, parent, eles):
        """Initialize the Elements class."""
        # check for correct parent
        if parent.__class__.__name__ != "IniAbu":
            raise TypeError("Elements class must be initialized from IniAbu.")

        # set the variables
        self._eles = eles
        self._ele_dict = parent.ele_dict

    # PROPERTIES #

    @property
    def isotopes_a(self):
        """
        Gets the atomic number of all isotopes of this element and returns it as a
        numpy integer array. If more than one element is selected, a list of numpy
        integer arrays is returned.

        :return: Atomic numbers of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][1], dtype=np.int))
        return return_value_simplifier(ret_arr)

    @property
    def isotopes_relative_abundance(self):
        """
        Gets the relative abundances of all isotopes of this elements and returns a list
        of them. If more than one element is selected, a list of np.arrays<float> is
        returned.

        Note: All relative abundances sum up up to unity.

        :return: Relative abundance of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][2], dtype=np.float))
        return return_value_simplifier(ret_arr)

    @property
    def isotopes_solar_abundance(self):
        """
        Gets the solar abundances of all isotopes of this elements and returns a list
        of them. If more than one element is selected, a list of np.arrays<float> is
        returned.

        Note: Not all databases contain this information, which will return `np.nan's`

        :return: Relative abundance of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][3], dtype=np.float))
        return return_value_simplifier(ret_arr)

    @property
    def solar_abundance(self):
        """
        Gets the total solar abundance of an element in the selected database. Returns
        an `np.nan` if the value is not in the database. If more than one element is
        selected, a `np.array` is returned

        :return: Solar abundance of the specified element / elements
        :rtype: float,ndarray
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(self._ele_dict[ele][0])
        ret_arr = np.array(ret_arr)
        return return_value_simplifier(ret_arr)
