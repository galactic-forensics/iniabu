"""Isotope handler.

This class manages the isotopes. It must be called from :class:`iniabu.IniAbu`.
"""


import numpy as np

from . import data
from .utilities import return_list_simplifier


class Isotopes(object):
    """Class representing the isotopes.

    This is mainly a list to easily interact with the `parent._iso_dict` dictionary.

    Example:
        >>> from iniabu import ini
        >>> isotope = ini.isotope["Si-28"]
        >>> isotope.relative_abundance
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
        :param isos: Isotope dictionary.
        :type isos: dict
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
    def mass(self):
        """Get the mass of an isotope.

        :return: Mass of an isotope.
        :rtype: float,ndarray<float>
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(data.isotopes_mass[iso])
        return return_list_simplifier(ret_arr)

    @property
    def relative_abundance(self):
        """Get relative abundance of isotope(s).

        Returns the relative abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: All relative abundances
        sum up up to unity.

        :return: Relative abundance of isotope(s)
        :rtype: float,ndarray
        """
        ret_arr = []
        for iso in self._isos:
            ret_arr.append(self._iso_dict[iso][0])
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def solar_abundance(self):
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
