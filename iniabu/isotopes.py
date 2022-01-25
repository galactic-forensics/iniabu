"""Isotope handler.

This class manages the isotopes. It must be called from :class:`iniabu.IniAbu`.
"""

import itertools

import numpy as np

from . import data
from .utilities import (
    get_all_available_isos,
    get_all_stable_isos,
    return_list_simplifier,
)


class Isotopes:
    """Class representing the isotopes.

    This is mainly a list to easily interact with the `parent._iso_dict` dictionary.

    Example:
        >>> from iniabu import ini
        >>> isotope = ini.iso["Si-28"]
        >>> isotope.abu_rel
        0.9223

    .. note:: You can also call isotopes using alternative spellings, e.g.,
        "28Si" or "Si28".

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
        tmp_isos_stable = []
        tmp_isos_all = []
        for entry in isos:
            if entry in parent.ele_dict.keys():
                tmp_isos_stable.append(get_all_stable_isos(parent, entry))
                tmp_isos_all.append(get_all_available_isos(entry))
            else:  # for flattening list with itertools (std lib)
                tmp_isos_stable.append([entry])
                tmp_isos_all.append([entry])
        isos = list(itertools.chain(*tmp_isos_stable))
        isos_all = list(itertools.chain(*tmp_isos_all))

        # set the variables
        self._isos = isos
        self._isos_all = isos_all

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
        return self._a()

    @property
    def a_all(self):
        """Get total number of nucleons for all available isotope(s).

        Returns the total number of nucleons for the given isotope. Sure, this is
        already passed as an argument in the isotope name, however, might be useful
        for plotting to have a return for it.
        All available isotopes means stable and unstable.

        :return: Mass number of isotope
        :rtype: int, ndarray<int>
        """
        return self._a(all_av=True)

    def _a(self, all_av=False):
        """Get total number of nucleons for given isotope.

        Returns the total number of nucleons for the given isotope. Sure, this is
        already passed as an argument in the isotope name, however, might be useful
        for plotting to have a return for it.
        All available isotopes means stable and unstable.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Mass number of isotope
        :rtype: int, ndarray<int>
        """
        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos

        ret_arr = np.zeros(len(isos), dtype=int)
        for it, iso in enumerate(isos):
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
        return self._abu_rel()

    @property
    def abu_rel_all(self):
        """Get relative abundance of all available isotope(s).

        Returns the relative abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: All relative abundances
        sum up up to unity. If you are using "mass_fractions" as units, relative
        abundances will also be in mass fractions.
        All available isotopes means stable and unstable.

        :return: Relative abundance of isotope(s)
        :rtype: float,ndarray
        """
        return self._abu_rel(all_av=True)

    def _abu_rel(self, all_av=False):
        """Get relative abundance of isotope(s).

        Returns the relative abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: All relative abundances
        sum up up to unity. If you are using "mass_fractions" as units, relative
        abundances will also be in mass fractions.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Relative abundance of isotope(s)
        :rtype: float,ndarray
        """
        ret_arr = []

        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos

        for iso in isos:

            try:
                ret_arr.append(self._iso_dict[iso][0])
            except KeyError:
                ret_arr.append(0)  # isotope has no relative abundance - unstable
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
        return self._abu_solar()

    @property
    def abu_solar_all(self):
        """Get solar abundance of all available isotope(s).

        Returns the solar abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: Not all databases contain
        this information. If the information is not available, these values will be
        filled with ``np.nan``.
        All available isotopes means stable and unstable.

        :return: Solar abundance of isotope(s)
        :rtype: float,ndarray
        """
        return self._abu_solar(all_av=True)

    def _abu_solar(self, all_av=False):
        """Get solar abundance of isotope(s).

        Returns the solar abundance of the selected isotope(s). Returns the result
        either as a ``float`` or as a numpy ``ndarray``. Note: Not all databases contain
        this information. If the information is not available, these values will be
        filled with ``np.nan``.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Solar abundance of isotope(s)
        :rtype: float,ndarray
        """
        ret_arr = []

        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos

        for iso in isos:
            try:
                ret_arr.append(self._iso_dict[iso][1])
            except KeyError:
                ret_arr.append(0)  # isotope has no solar abundance - unstable
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def mass(self):
        """Get the mass of an isotope.

        :return: Mass of an isotope.
        :rtype: float,ndarray<float>
        """
        return self._mass()

    @property
    def mass_all(self):
        """Get the mass of all available isotopes.

        All available isotopes means stable and unstable.

        :return: Mass of an isotope.
        :rtype: float,ndarray<float>
        """
        return self._mass(all_av=True)

    def _mass(self, all_av=False):
        """Get the mass of an isotope.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Mass of an isotope.
        :rtype: float,ndarray<float>
        """
        ret_arr = []

        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos

        for iso in isos:
            try:
                ret_arr.append(data.isotopes_mass[iso])
            except KeyError:
                ret_arr.append(data.isotopes_mass_all[iso])  # unstable isotope
        ret_arr = np.array(ret_arr)
        return return_list_simplifier(ret_arr)

    @property
    def name(self):
        """Get the name of an isotope.

        If an alternative spelling was used to call the isotope, e.g., "Si28" or "28Si",
        the name will still be returned as "Si-28", which is the default for `iniabu`.

        :return: Name of the set isotope(s).
        :rtype: str, list(str)
        """
        return self._name()

    @property
    def name_all(self):
        """Get the names of all available isotope.

        If an alternative spelling was used to call the isotope, e.g., "Si28" or "28Si",
        the name will still be returned as "Si-28", which is the default for `iniabu`.
        All available isotopes means stable and unstable.

        :return: Name of the set isotope(s).
        :rtype: str, list(str)
        """
        return self._name(all_av=True)

    def _name(self, all_av=False):
        """Get the name of an isotope.

        If an alternative spelling was used to call the isotope, e.g., "Si28" or "28Si",
        the name will still be returned as "Si-28", which is the default for `iniabu`.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Name of the set isotope(s).
        :rtype: str, list(str)
        """
        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos
        return return_list_simplifier(isos)

    @property
    def z(self):
        """Get the number of protons for the isotopes.

        :return: Number of protons for the set isotope(s).
        :rtype: int, ndarray<int>
        """
        return self._z()

    @property
    def z_all(self):
        """Get the number of protons for the isotopes.

        All available isotopes means stable and unstable.

        :return: Number of protons for the set isotope(s).
        :rtype: int, ndarray<int>
        """
        return self._z(all_av=True)

    def _z(self, all_av=False):
        """Get the number of protons for the isotopes.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Number of protons for the set isotope(s).
        :rtype: int, ndarray<int>
        """
        eles = self._element(all_av=all_av)
        ret_arr = np.zeros(len(eles), dtype=int)
        for it, ele in enumerate(eles):
            ret_arr[it] = data.elements_z[ele]
        return return_list_simplifier(ret_arr)

    # private properties and functions

    def _element(self, all_av=False):
        """Return the elements associated with the isotope.

        :param all_av: Use all available isotopes, stable and unstable?
        :type all_av: bool

        :return: Name of element(s).
        :rtype: str, list(str)
        """
        ret_arr = []

        if all_av:
            isos = self._isos_all
        else:
            isos = self._isos

        for iso in isos:
            ret_arr.append(iso.split("-")[0])
        return ret_arr
