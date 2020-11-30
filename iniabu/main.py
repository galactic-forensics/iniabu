"""IniAbu class - the heart of the package.

This file contains the main `IniAbu` class.
"""

import numpy as np

from . import data
from . import utilities
from .elements import Elements
from .isotopes import Isotopes
from .utilities import ProxyList, return_as_ndarray, return_string_as_list


class IniAbu(object):
    """Initialize the IniAbu class.

    By default, the ``lodders09`` database is read in. Available databases are:

    - ``asplund09``: Asplund et al. (2009), doi: 10.1146/annurev.astro.46.060407.145222
    - ``lodders09``: Lodders et al. (2009), doi: 10.1007/978-3-540-88055-4_34
    - ``nist``: Current (as of 2020) NIST isotopic abundances.

    Todo Example
    """

    def __init__(self, database="lodders09", unit="num_lin"):
        """Initialize IniAbu.

        Load and set the default database.

        :param database: Database to initialize the class with, defaults to
            ``lodders09``.
        :type database: str
        :param unit: Units to use for initialization.
        :type unit: str
        """
        # init parameters
        self._database = None
        self._unit = unit

        # set database
        self.database = database

    # PROXY LISTS #

    @property
    def element(self):
        """Get information for a specific element.

        Calls the :class`iniabu.elements.Elements`. This handler represents a convenient
        way to dig through elemental information. More information and a full list of
        properties can be found in the :doc:`Elements </api/elements>` class.

        :return: Returns a ProxyList initialized with the required element
        :rtype: class

        Example:
            >>> from iniabu import ini
            >>> # get the solar abundance of silicon
            >>> ini.element["Si"].solar_abundance
            999700.0

            >>> # get a numpy array of the solar abundance of two elements
            >>> ini.element[["Fe", "Ni"]].solar_abundance
            array([847990.,  49093.])

            >>> # get a list of all atomic numbers for isotopes of helium
            >>> ini.element["He"].isotopes_a
            array([3, 4])

            >>> # similarly, query isotopes relative abundances, and solar abundances
            >>> ini.element["He"].isotopes_relative_abundance
            array([1.66000e-04, 9.99834e-01])
            >>> ini.element["He"].isotopes_solar_abundance
            array([1.03e+06, 2.51e+09])
        """
        return ProxyList(self, Elements, self._ele_dict.keys(), unit=self._unit)

    @property
    def isotope(self):
        """Get information for a specific isotope.

        Calls the :class`iniabu.isotopes.Isotopes`. This handler represents a convenient
        way to dig through isotopic information. More information and a full list of
        properties can be found in the :doc:`Isotopes </api/isotopes>` class.

        :return: Returns a ProxyList initialized with the required element
        :rtype: class

        Example:
            >>> from iniabu import ini
            >>> # get the solar abundance of Si-28
            >>> ini.isotope["Si-28"].solar_abundance
            922000.0

            >>> # get a numpy array of the solar abundance of two isotopes
            >>> ini.isotope[["Fe-56", "Ni-60"]].solar_abundance
            array([778000.,  12900.])

            >>> # similarly, query relative abundance(s) of isotope(s)
            >>> ini.isotope["He-4"].relative_abundance
            0.999834
            >>> ini.isotope[["H-2", "He-3"]].relative_abundance
            array([1.94e-05, 1.66e-04])
        """
        return ProxyList(self, Isotopes, self._iso_dict.keys(), unit=self._unit)

    # PROPERTIES #

    @property
    def database(self):
        """Get / Set the current database.

        :setter: Database to set.
        :type: str

        :return: Name of the loaded database.
        :rtype: str

        Example:
            >>> from iniabu import ini  # loads with default ("lodders09")
            >>> ini.database = "nist"  # change database to "nist"
            >>> ini.database
            'nist'
            >>> ini.database = "lodders09"  # simple switch back!
        """
        return self._database

    @database.setter
    def database(self, db):
        self._ele_dict, self._iso_dict = data.database_selector(db)
        (
            self._ele_dict_log,
            self._iso_dict_log,
        ) = utilities.make_log_abundance_dictionaries(self._ele_dict)
        self._ele_dict_mf, self._iso_dict_mf = utilities.make_mass_fraction_dictionary(
            self._ele_dict
        )

        # todo: remove next line -> keep the units
        self.unit = "num_lin"
        self._database = db

    @property
    def ele_dict(self):
        """Get the element dictionary.

        The dictionary keys are element symbols, e.g., "H". The entries for the element
        dictionary are a list containing the following entries (in order):

        - Solar abundance
        - ndarray with mass numbers of all isotopes
        - ndarray with relative abundances of all isotopes
        - ndarray with solar abundances of all isotopes

        :return: Element dictionary
        :rtype: dict
        """
        return self._ele_dict

    @property
    def ele_dict_log(self):
        """Get the element dictionary with logarithmic solar abundances.

        The dictionary keys are element symbols, e.g., "H". The entries for the element
        dictionary are a list containing the following entries (in order):

        - Solar abundance (log)
        - ndarray with mass numbers of all isotopes
        - ndarray with relative abundances of all isotopes
        - ndarray with solar abundances of all isotopes (log)

        :return: Element dictionary
        :rtype: dict
        """
        return self._ele_dict_log

    @property
    def iso_dict(self):
        """Get the isotope dictionary.

        The dictionary keys are isotope symbols, e.g., "H-1". The entries for the
        isotope dictionary are a list containing the following entries (in order):

        - Relative abundance
        - Solar abundance

        :return: Isotope dictionary
        :rtype: dict
        """
        return self._iso_dict

    @property
    def iso_dict_log(self):
        """Get the isotope dictionary with logarithmic solar abundances.

        The dictionary keys are isotope symbols, e.g., "H-1". The entries for the
        isotope dictionary are a list containing the following entries (in order):

        - Relative abundance
        - Solar abundance (log)

        :return: Isotope dictionary
        :rtype: dict
        """
        return self._iso_dict_log

    @property
    def unit(self):
        """Get / Set the unit for the solar abundances.

        Routine to easily switch the database between the **default** linear number
        abundances, normed to Si with an abundance of 1e6 (``num_lin``, typically used
        in cosmo- and geochemistry studies), the logarithmic (``num_log``, typically
        used in astronomy) abundance units, normed to H as 12, or mass fractions
        ``massf``, normed such that all elements sum up to unity.

        :setter: Unit to set, either "num_lin" (default), "num_log", or "mass_fraction".
        :type: str

        :return: Currently set unit.
        :rtype: str

        :raises ValueError: The unit being set is not valid.

        Example:
            >>> from iniabu import ini  # loads with default linear units
            >>> ini.unit
            'num_lin'

            >>> ini.unit = "num_log"  # set logarithmic abundance unit
            >>> ini.element["H"].solar_abundance
            12.0
        """
        return self._unit

    @unit.setter
    def unit(self, s):
        if s == "num_lin" or "num_log" or "mass_fraction":
            self._unit = s
        else:
            raise ValueError(f"Your selected unit {s} is not a valid unit.")

    # METHODS #

    def bracket_element(self, nominator, denominator, value, mass_fraction=False):
        """Calculate the bracket ratio for a given element ratio and a value.

        Bracket notation is defined as:

        result = log10(measured value) - log10(solar ratio)

        Nominator and denominator have the same restrictions as for the
        ``ratio_element`` method.
        The same number of values must be supplied as there are element ratios defined.

        :param nominator: Element(s) in nominator.
        :type nominator: str,list
        :param denominator: Element(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate bracket notation value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool

        :return: Bracket notation expression of given values with respect to the solar
            system abundances.
        :rtype: float,ndarray

        :raises ValueError: Number of element ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.bracket_element("Ne", "Si", 33)
            1.0008802726402624
        """
        solar_ratios = return_as_ndarray(
            self.ratio_element(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape:
            raise ValueError(
                "Length of requested element ratios does not match length of "
                "provided values."
            )

        return np.log10(value) - np.log10(solar_ratios)

    def bracket_isotope(self, nominator, denominator, value, mass_fraction=False):
        """Calculate the bracket ratio for a given isotope ratio and a value.

        Bracket notation is defined as:

        result = log10(measured value) - log10(solar ratio)

        Nominator and denominator have the same restrictions as for the
        ``ratio_element`` method.
        The same number of values must be supplied as there are element ratios defined.

        :param nominator: Isotope(s) in nominator.
        :type nominator: str,list
        :param denominator: Isotope(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate bracket notation value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool

        :return: Bracket notation expression of given values with respect to the solar
            system abundances.
        :rtype: float,ndarray

        :raises ValueError: Number of element ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.bracket_isotope("Ne-21", "Ne-20", 2.397)
            2.9999700012616572
        """
        solar_ratios = return_as_ndarray(
            self.ratio_isotope(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape:
            raise ValueError(
                "Length of requested isotope ratios does not match length of "
                "provided values."
            )

        return np.log10(value) - np.log10(solar_ratios)

    def delta_element(
        self, nominator, denominator, value, mass_fraction=False, delta_factor=1000.0
    ):
        """Calculate the delta-value for a given element ratio and a value.

        The delta-value is defined as:

        result = (measured value / solar ratio - 1)

        By default, the delta-value is multiplied by 1000, thus, expressing it in
        permil. Other factors can be chosen.

        Nominator and denominator have the same restrictions as for the
        ``ratio_element`` method.
        The same number of values must be supplied as there are element ratios defined.

        :param nominator: Element(s) in nominator.
        :type nominator: str,list
        :param denominator: Element(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate delta-value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool
        :param delta_factor: What value should the delta value be multiplied with?
            Defaults to 1000 to return results in permil.
        :param delta_factor: float

        :return: Delta-values of given values with respect to the solar system
            abundances, multiplied by delta_factor (by default, returns delta-values
            in permil).
        :rtype: float,ndarray

        :raises ValueError: Number of element ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.delta_element("Ne", "Si", 3.4)
            32.39347210030586
        """
        solar_ratios = return_as_ndarray(
            self.ratio_element(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape:
            raise ValueError(
                "Length of requested element ratios does not match length of "
                "provided values."
            )

        return (value / solar_ratios - 1) * delta_factor

    def delta_isotope(
        self, nominator, denominator, value, mass_fraction=False, delta_factor=1000.0
    ):
        """Calculate the delta-value for a given isotope ratio and a value.

        The delta-value is defined as:

        result = (measured value / solar ratio - 1)

        By default, the delta-value is multiplied by 1000, thus, expressing it in
        permil. Other factors can be chosen.

        Nominator and denominator have the same restrictions as for the
        ``ratio_element`` method.
        The same number of values must be supplied as there are isotope ratios defined.

        :param nominator: Isotope(s) in nominator.
        :type nominator: str,list
        :param denominator: Isotope(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate delta-value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool
        :param delta_factor: What value should the delta value be multiplied with?
            Defaults to 1000 to return results in permil.
        :param delta_factor: float

        :return: Delta-values of given values with respect to the solar system
            abundances, multiplied by delta_factor (by default, returns delta-values
            in permil).
        :rtype: float,ndarray

        :raises ValueError: Number of isotope ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.delta_isotope("Ne-22", "Ne-20", 0.07, delta_factor=10000)
            -480.0676021714623

            >>> # For more than 1 ratio
            >>> nominator_isos = ["Ne-21", "Ne-22"]
            >>> values = [0.01, 0.07]  # values to compare with
            >>> ini.delta_isotope(nominator_isos, "Ne-20", values, delta_factor=10000)
            array([31715.93357271,  -480.06760217])
        """
        solar_ratios = return_as_ndarray(
            self.ratio_isotope(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape:
            raise ValueError(
                "Length of requested isotope ratios does not match length of "
                "provided values."
            )

        return (value / solar_ratios - 1) * delta_factor

    def ratio_element(self, nominator, denominator, mass_fraction=False):
        """Get the ratios of given elements.

        Nominator and denominator can be element names or lists of element names (if
        more than one ratio should be calculated). If the denominator is a list, its
        length must be identical to the list in the nominator.

        :param nominator: Element or list of elements in nominator of ratio.
        :type nominator: str,list
        :param denominator: Element or list of elements in denominator of ratio.
        :type denominator: str,list
        :param mass_fraction: Should mass fractions be returned? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool

        :return: The element ratio or a numpy array of the requested ratios.
        :rtype: float,ndarray

        :raises ValueError: Denominator is a list with more than one entry and does not
            have the same length as the nominator.

        Example:
            >>> from iniabu import ini
            >>> # Calculate H/He ratio
            >>> ini.ratio_element("H", "He")
            10.314692775474606

            >>> # Calculate same ratio as mass fraction
            >>> ini.ratio_element("H", "He", mass_fraction=True)
            40.96035314200997

            >>> # Calculate ratios with multiple elements
            >>> ini.ratio_element(["H", "He", "Al"], ["Si"])
            array([2.59082755e+04, 2.51178354e+03, 8.46253876e-02])

            >>> # Multiple ratios at the same time
            >>> ini.ratio_element(["H", "He"], ["He", "H"])
            array([10.31469278,  0.09694908])

            >>> # The result when the solar abundance of an element is not avaialble
            >>> ini.database = "nist"
            >>> ini.ratio_element("H", "He")
            nan

            >>> ini.database = "lodders09"  # set back to default and check again
            >>> ini.ratio_element("H", "He")
            10.314692775474606
        """
        # turn into string if necessary
        nominator = return_string_as_list(nominator)
        denominator = return_string_as_list(denominator)

        # check for equal length if nominator and denominator
        if len(nominator) != len(denominator) and len(denominator) != 1:
            raise ValueError(
                "The denominator contains more than one entry but "
                "has a different length from the nominator. This "
                "is not allowed."
            )

        # remember current unit of abundances, then set to linear
        current_abundance_unit = self.unit
        self.unit = "num_lin"

        # get the values back:
        nominator_value = self.element[nominator].solar_abundance
        denominator_value = self.element[denominator].solar_abundance

        # return database to previous state
        self.unit = current_abundance_unit

        ratio = nominator_value / denominator_value

        # correct if mass_fraction is true
        if mass_fraction:
            # get masses
            nominator_masses = [data.elements_mass[ele] for ele in nominator]
            denominator_masses = [data.elements_mass[ele] for ele in denominator]
            # correct ratio
            corr_factor = utilities.return_list_simplifier(
                np.array(denominator_masses) / np.array(nominator_masses)
            )
            ratio *= corr_factor

        return ratio

    def ratio_isotope(self, nominator, denominator, mass_fraction=False):
        """Get the ratios of given isotopes.

        Grabs the isotope ratios for nominator / denominator. By default, number
        fractions are returned, however, mass fractions return is possible by setting
        "mass_fraction=True".
        If a list of nominator isotopes is given but only one denominator isotope,
        the ratio with that denominator is formed for each isotope. If both parameters
        are given as lists, they must be of equal length.

        :param nominator: Isotope / List of isotopes for nominator, in form: "Si-29".
            If an element is given, all isotopes of this element are used. Lists of
            elements are not allowed.
        :type nominator: str,list
        :param denominator: Isotope / List of isotopes for denominator, in form:
            "Si-29". Alternatively, an element can be given, i.e., "Si". In that case,
            the most abundant isotope is chosen. Lists of elements are not allowed.
        :type denominator: str,list
        :param mass_fraction: Should mass fractions be returned? Defaults to False
            (i.e., number fractions are returned).
        :type mass_fraction: bool

        :return: The isotope ratio or a numpy array of the requested ratios.
        :rtype: float,ndarray

        :raises ValueError: Denominator is a list with more than one entry and does not
            have the same length as the nominator.

        Example:
            >>> from iniabu import ini
            >>> # calculate Ne-21 / Ne-20 isotope ratio
            >>> ini.ratio_isotope("Ne-21", "Ne-20")
            0.0023971655776491205

            >>> # calculate isotope ratios for all Ne isotopes versus Ne-20
            >>> ini.ratio_isotope("Ne", "Ne-20")
            array([1.        , 0.00239717, 0.07352993])

            >>> # Isotope ratios for Ne-21 and Ne-22 versus most abundant Ne isotope
            >>> ini.ratio_isotope(["Ne-21", "Ne-22"], "Ne")
            array([0.00239717, 0.07352993])

            >>> # repeat this calculation assuming mass fractions
            >>> ini.ratio_isotope(["Ne-21", "Ne-22"], "Ne", mass_fraction=True)
            array([0.00228282, 0.0668463 ])
        """
        # check for equal length if nominator and denominator are lists
        if not isinstance(nominator, str) and not isinstance(denominator, str):
            if len(nominator) != len(denominator) and len(denominator) != 1:
                raise ValueError(
                    "The denominator contains more than one entry but "
                    "has a different length from the nominator. This "
                    "is not allowed."
                )

        # check if elements are in nominator / denominator
        if isinstance(nominator, str) and nominator in self._ele_dict.keys():
            nominator = self._get_all_isotopes(nominator)

        if isinstance(denominator, str) and denominator in self._ele_dict.keys():
            denominator = self._get_major_isotope(denominator)

        # remember current unit of abundances, then set to linear
        current_abundance_unit = self.unit
        self.unit = "num_lin"

        # get the values back:
        nominator_value = self.isotope[nominator].relative_abundance
        denominator_value = self.isotope[denominator].relative_abundance

        # return database to previous state
        self.unit = current_abundance_unit

        ratio = nominator_value / denominator_value

        # correct if mass_fraction is true
        if mass_fraction:
            # turn into list if necessary
            nominator = return_string_as_list(nominator)
            denominator = return_string_as_list(denominator)
            # get masses
            nominator_masses = [data.isotopes_mass[iso] for iso in nominator]
            denominator_masses = [data.isotopes_mass[iso] for iso in denominator]
            # correct ratio
            corr_factor = utilities.return_list_simplifier(
                np.array(denominator_masses) / np.array(nominator_masses)
            )
            ratio *= corr_factor

        return ratio

    # PRIVATE METHODS #

    def _get_all_isotopes(self, element):
        """Get all isotopes for a given element.

        :param element: Element.
        :type element: str

        :return: List of isotopes.
        :rtype: list
        """
        isotopes = self.element[element].isotopes_a
        ret_val = ["{}-{}".format(element, isotope) for isotope in isotopes]
        return ret_val

    def _get_major_isotope(self, element):
        """Get the most abundant isotope for a given element.

        :param element: Element.
        :type element: str

        :return: Isotope.
        :rtype: str
        """
        isotopes = self.element[element].isotopes_a
        abus = self.element[element].isotopes_relative_abundance
        return "{}-{}".format(element, isotopes[abus.argmax()])
