"""Element handler.

This class manages the elements. It must be called from :class:`iniabu.IniAbu`.
"""


import numpy as np

from . import data
from .utilities import return_list_simplifier


class Elements:
    """Class representing the elements.

    This is mainly a list to easily interact with the `parent._ele_dict` dictionary.

    Example:
        >>> from iniabu import ini
        >>> ini.unit
        'num_lin'
        >>> element = ini.ele["Si"]
        >>> element.abu_solar
        999700.0

    .. warning:: This class should NOT be manually created by the user. It is
        designed to be initialized by :class:`iniabu.IniAbu`.
    """

    def __init__(self, parent, eles, unit="num_lin", *args, **kwargs):
        """Initialize the Elements class.

        Checks for initialization from the proper parent class and sets up the required
        dictionaries to be used later.

        :param parent: Parent class.
        :type parent: class:`iniabu.IniAbu`
        :param eles: Elements to process.
        :type eles: list(str)
        :param unit: Units used for return.
        :type unit: str
        :param *args: Variable length argument list.
        :param **kwargs: Arbitrary keyword arguments.

        :raises TypeError: The class was not initialized with :class:`iniabu.IniAbu`
            as the parent.
        :raises NotImplementedError: An unavailable unit was selected.
        """
        # check for correct parent
        if parent.__class__.__name__ != "IniAbu":
            raise TypeError("Elements class must be initialized from IniAbu.")

        # set the variables
        self._eles = eles
        if unit == "num_lin":
            self._ele_dict = parent.ele_dict
        elif unit == "num_log":
            self._ele_dict = parent.ele_dict_log
        elif unit == "mass_fraction":
            self._ele_dict = parent.ele_dict_mf
        else:
            raise NotImplementedError(
                f"The chosen unit {unit} is currently not implemented."
            )

    # PROPERTIES #

    @property
    def abu_solar(self):
        """Get solar abundance of element(s).

        Returns the solar abundance of the selected element(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: Not all databases contain
        this information. If the information is not available, these values will be
        filled with ``np.nan``.

        :return: Solar abundance of element(s)
        :rtype: float,ndarray
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(self._ele_dict[ele][0])
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def iso_a(self):
        """Get the atomic number(s) of all isotopes.

        Returns the atomic number(s) of all isotopes of this element as a numpy integer
        ndarray. If more than one element is selected, a list of numpy integer arrays
        is returned.

        :return: Atomic numbers of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][1], dtype=np.int))
        return return_list_simplifier(ret_arr)

    @property
    def iso_abu_rel(self):
        """Get relative abundance of all isotopes.

        Returns a list with the relative abundances of all isotopes of the given
        element. If more than one element is selected, a list of numpy float ndarrays is
        returned. Note: All relative abundances sum up up to unity. If you are using
        "mass_fractions" as units, relative abundances will also be in mass fractions.

        :return: Relative abundance of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][2], dtype=np.float))
        return return_list_simplifier(ret_arr)

    @property
    def iso_abu_solar(self):
        """Get solar abundances of all isotopes.

        Returns a list with the solar abundances of all isotopes of the given element.
        If more than one element is selected, a list of numpy float ndarrays is
        returned. Note: Not all databases contain this information. If the information
        is not available, these values will be filled with ``np.nan``.

        :return: Relative abundance of all isotopes
        :rtype: ndarray,list<ndarray>
        """
        ret_arr = []
        for ele in self._eles:
            ret_arr.append(np.array(self._ele_dict[ele][3], dtype=np.float))
        return return_list_simplifier(ret_arr)

    @property
    def mass(self):
        """Get the mass of an element.

        Returns the mass of an element depending on the specified composition. The mass
        is calculated as the weighted sum of the individual isotope masses, weighted
        by there respective abundances.

        :return: Mass of an element.
        :rtype: float,ndarray<float>
        """
        ret_arr = []
        for ele in self._eles:
            isos = [f"{ele}-{a}" for a in self._ele_dict[ele][1]]
            isos_abu = np.array([abu for abu in self._ele_dict[ele][2]])
            isos_mass = np.array([data.isotopes_mass[iso] for iso in isos])
            ret_arr.append(np.sum(isos_abu * isos_mass))
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def name(self):
        """Get the name of an element.

        :return: Name of the set element(s).
        :rtype: str, list(str)
        """
        return return_list_simplifier(self._eles)

    @property
    def z(self):
        """Get the number of protons for the element.

        :return: Number of protons for the set element(s).
        :rtype: int, ndarray<int>
        """
        ret_arr = np.zeros(len(self._eles), dtype=int)
        for it, ele in enumerate(self._eles):
            ret_arr[it] = data.elements_z[ele]
        return return_list_simplifier(ret_arr)
