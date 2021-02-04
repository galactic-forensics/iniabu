"""Isotope handler.

This class manages the isotopes. It must be called from :class:`iniabu.IniAbu`.
"""

import itertools

import numpy as np

from . import data
from .utilities import get_all_isos, return_list_simplifier


class Isotopes(object):
    """Class representing the isotopes.

    This is mainly a list to easily interact with the `parent._iso_dict` dictionary.

    Example:
        >>> from iniabu import ini
        >>> isotope = ini.iso["Si-28"]
        >>> isotope.abu_rel
        0.9223

    .. warning:: This class should NOT be manually created by the user. It is
        designed to be initialized by :class:`iniabu.IniAbu`
    """

    def __init__(self, parent, isos, unit="num_lin", *args, **kwargs):
        """Initialize the Isotopes class.

        Checks for initialization from the proper parent class and sets up the required
        dictionaries to be used later.

        :param parent: Parent class.
        :type parent: class:`iniabu.IniAbu`
        :param isos: Isotopes to process.
        :type isos: list(str)
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
            raise TypeError("Isotopes class must be initialized from IniAbu.")

        # create isotopes with elements and isotopes available
        tmp_isos = []
        for entry in isos:
            if entry in parent.ele_dict.keys():
                tmp_isos.append(get_all_isos(parent, entry))
            else:
                tmp_isos.append([entry])  # for flattening list with itertools (std lib)
        isos = list(itertools.chain(*tmp_isos))

        # set the variables
        self._isos = isos
        if unit == "num_lin":
            self._iso_dict = parent.iso_dict
        elif unit == "num_log":
            self._iso_dict = parent.iso_dict_log
        elif unit == "mass_fraction":
            self._iso_dict = parent.iso_dict_mf
        else:
            raise NotImplementedError(
                f"The chosen unit {unit} is currently not implemented."
            )

    # PROPERTIES #

    @property
    def a(self):
        """Get total number of nucleons for given isotope.

        Returns the total number of nucleons for the given isotope. Sure, this is
        already passed as an argument in the isotope name, however, might be useful
        for plotting to have a return for it.

        :return: Mass number of isotope
        :rtype: int, ndarray<int>
        """
        ret_arr = np.zeros(len(self._isos), dtype=int)
        for it, iso in enumerate(self._isos):
            ret_arr[it] = iso.split("-")[1]
        return return_list_simplifier(ret_arr)

    @property
    def abu_rel(self):
        """Get relative abundance of isotope(s).

        Returns the relative abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: All relative abundances
        sum up up to unity. If you are using "mass_fractions" as units, relative
        abundances will also be in mass fractions.

        :return: Relative abundance of isotope(s)
        :rtype: float,ndarray
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(self._iso_dict[iso][0])
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def abu_solar(self):
        """Get solar abundance of isotope(s).

        Returns the solar abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: Not all databases contain
        this information. If the information is not available, these values will be
        filled with ``np.nan``.

        :return: Solar abundance of isotope(s)
        :rtype: float,ndarray
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(self._iso_dict[iso][1])
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def mass(self):
        """Get the mass of an isotope.

        :return: Mass of an isotope.
        :rtype: float,ndarray<float>
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(data.isotopes_mass[iso])
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def name(self):
        """Get the name of an isotope.

        :return: Name of the set isotope(s).
        :rtype: str, list(str)
        """
        return return_list_simplifier(self._isos)

    @property
    def z(self):
        """Get the number of protons for the element.

        :return: Number of protons for the set element(s).
        :rtype: int, ndarray<int>
        """
        eles = self._element
        ret_arr = np.zeros(len(eles), dtype=int)
        for it, ele in enumerate(eles):
            ret_arr[it] = data.elements_z[ele]
        return return_list_simplifier(ret_arr)

    # private properties and functions

    @property
    def _element(self):
        """Return the elements associated with the isotope.

        :return: Name of element(s).
        :rtype: str, list(str)
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(iso.split("-")[0])
        return ret_arr
