"""IniAbu class - the heart of the package.

This file contains the main `IniAbu` class.
"""


import numpy as np

from . import data
from . import utilities
from .elements import Elements
from .isotopes import Isotopes
from .utilities import (
    linear_units,
    ProxyList,
    return_as_ndarray,
    return_string_as_list,
)


class IniAbu:
    """Initialize the IniAbu class.

    By default, the ``lodders09`` database is read in. Available databases are:

    - ``asplund09``: Asplund et al. (2009), doi: 10.1146/annurev.astro.46.060407.145222
    - ``lodders09``: Lodders et al. (2009), doi: 10.1007/978-3-540-88055-4_34
    - ``nist``: Current (as of 2020) NIST isotopic abundances.

    For detailed examples, see: https://iniabu.readthedocs.io/

    Example:
        >>> from iniabu import ini
        >>> ini.iso["Ne"].name
        ['Ne-20', 'Ne-21', 'Ne-22']
        >>> ini.iso["Ne"].abu_solar
        array([3060000.,    7330.,  225000.])
        >>> ini.iso_delta("Si-30", "Si-28", 0.02)
        -403.23624595469255
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
        self._is_initializing = True  # to avoid message printing

        # set database
        self.database = database

        # set unit
        self.unit = unit

        # normalization isotopes - user defined
        self._norm_isos = {}

        # done with init
        self._is_initializing = False

    # PROXY LISTS #

    @property
    def ele(self):
        """Get information for a specific element.

        Calls the :class`iniabu.elements.Elements`. This handler represents a convenient
        way to dig through elemental information. More information and a full list of
        properties can be found in the :doc:`Elements </api/elements>` class.

        :return: Returns a ProxyList initialized with the required element
        :rtype: class

        Example:
            >>> from iniabu import ini
            >>> # get the solar abundance of silicon
            >>> ini.ele["Si"].abu_solar
            999700.0

            >>> # get a numpy array of the solar abundance of two elements
            >>> ini.ele[["Fe", "Ni"]].abu_solar
            array([847990.,  49093.])

            >>> # get a list of all atomic numbers for isotopes of helium
            >>> ini.ele["He"].iso_a
            array([3, 4])

            >>> # similarly, query isotopes relative abundances, and solar abundances
            >>> ini.ele["He"].iso_abu_rel
            array([1.66000e-04, 9.99834e-01])
            >>> ini.ele["He"].iso_abu_solar
            array([1.03e+06, 2.51e+09])
        """
        return ProxyList(self, Elements, self._ele_dict.keys(), unit=self._unit)

    @property
    def iso(self):
        """Get information for a specific isotope.

        Calls the :class`iniabu.isotopes.Isotopes`. This handler represents a convenient
        way to dig through isotopic information. More information and a full list of
        properties can be found in the :doc:`Isotopes </api/isotopes>` class.

        :return: Returns a ProxyList initialized with the required element
        :rtype: class

        Example:
            >>> from iniabu import ini
            >>> # get the solar abundance of Si-28
            >>> ini.iso["Si-28"].abu_solar
            922000.0

            >>> # get a numpy array of the solar abundance of two isotopes
            >>> ini.iso[["Fe-56", "Ni-60"]].abu_solar
            array([778000.,  12900.])

            >>> # similarly, query relative abundance(s) of isotope(s)
            >>> ini.iso["He-4"].abu_rel
            0.999834
            >>> ini.iso[["H-2", "He-3"]].abu_rel
            array([1.94e-05, 1.66e-04])
        """
        # valid_keys = list(self.iso_dict.keys()) + list(self.ele_dict.keys())
        valid_keys = list(data.isotopes_mass_all.keys()) + list(self.ele_dict.keys())
        return ProxyList(self, Isotopes, valid_keys, unit=self._unit)

    # PROPERTIES #

    @property
    def database(self):
        """Get / Set the current database.

        Setting a new database does not change the units that are currently loaded.
        You will get a message printed on what these units are.

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
        ) = utilities.make_log_abu_dict(self._ele_dict)
        self._ele_dict_mf, self._iso_dict_mf = utilities.make_mf_dict(self._ele_dict)

        self._database = db

        # print message on what was loaded:
        if not self._is_initializing:
            print(
                f"iniabu loaded database: '{self.database}', current units: "
                f"'{self.unit}'"
            )

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
    def ele_dict_mf(self):
        """Get the element dictionary with mass fractions.

        The dictionary keys are element symbols, e.g., "H". The entries for the element
        dictionary are a list containing the following entries (in order):

        - Solar abundance (mass fractions)
        - ndarray with mass numbers of all isotopes
        - ndarray with relative abundances of all isotopes
        - ndarray with solar abundances of all isotopes (mass fractions)

        :return: Element dictionary
        :rtype: dict
        """
        return self._ele_dict_mf

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
    def iso_dict_mf(self):
        """Get the isotope dictionary in mass fractions.

        The dictionary keys are isotope symbols, e.g., "H-1". The entries for the
        isotope dictionary are a list containing the following entries (in order):

        - Relative abundance
        - Solar abundance (mass fractions)

        :return: Isotope dictionary
        :rtype: dict
        """
        return self._iso_dict_mf

    @property
    def norm_isos(self) -> dict:
        """Get / Set user defined normalization isotopes.

        .. note:: If you set the `norm_isos` multiple times, it will not be overwritten.
            Keys will rather be added to the dictionary. To reset it, please use the
            function `ini.reset_norm_isos()`.

        :setter: A dictionary with your normalization isotope per element.

        :return: The dictionary with user defined normalization isotopes.

        Example:
            >>> from iniabu import ini
            >>> ini.norm_isos
            {}
            >>> ini.norm_isos = {"Ba": "Ba-136"}
            >>> ini.norm_isos
            {'Ba': 'Ba-136'}
            >>> ini.norm_isos = {"Si": "Si-29"}
            >>> ini.norm_isos
            {'Ba': 'Ba-136', 'Si': 'Si-29'}
            >>> ini.reset_norm_isos()
            >>> ini.norm_isos
            {}
        """
        return self._norm_isos

    @norm_isos.setter
    def norm_isos(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError(
                "The normalization isotopes must be given as a dictionary. "
                "The key should be the element name, the value the "
                "normalization isotope."
            )

        for key in value.keys():
            val = value[key]
            if not isinstance(val, str):
                raise TypeError(
                    f"The value {val} for key {key} must be a string, but it is not. "
                    f"Please make sure you only select one normalization isotope per "
                    f"element."
                )
            nkey = utilities.item_formatter(key)
            nval = utilities.item_formatter(val)
            self._norm_isos[nkey] = nval

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

        Example:
            >>> from iniabu import ini  # loads with default linear units
            >>> ini.unit = "num_log"  # set logarithmic abundance unit
            >>> ini.unit
            'num_log'
            >>> ini.ele["H"].abu_solar
            12.0

            >>> ini.unit = "num_lin"  # set back to default
            >>> ini.unit
            'num_lin'
        """
        return self._unit

    @unit.setter
    def unit(self, s):
        if s == "num_lin" or s == "num_log" or s == "mass_fraction":
            self._unit = s
        else:
            raise ValueError(f"Your selected unit {s} is not a valid unit.")

    # METHODS #

    def ele_bracket(self, nominator, denominator, value, mass_fraction=None):
        """Calculate the bracket ratio for a given element ratio and a value.

        The bracket notation is the usual astronomy / logarithmic ratio, defined as:

        result = log10(measured value) - log10(solar ratio)

        Nominator and denominator have the same restrictions as for the
        ``ele_ratio`` method.
        If one element ratio is defined but multiple values, the isotope ratio for
        all values is calculated and returned as a numpy array. If more than one element
        ratio is defined, the same number of values must be supplied as there are
        element ratios defined.

        :param nominator: Element(s) in nominator.
        :type nominator: str,list
        :param denominator: Element(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate bracket notation value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
        :type mass_fraction: bool

        :return: Bracket notation expression of given values with respect to the solar
            system abundances.
        :rtype: float,ndarray

        :raises ValueError: Number of element ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.ele_bracket("Ne", "Si", 33)
            1.0008802726402624
        """
        solar_ratios = return_as_ndarray(
            self.ele_ratio(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape and solar_ratios.shape != ():
            raise ValueError(
                "Length of requested element ratios does not match length of "
                "provided values."
            )

        return np.log10(value) - np.log10(solar_ratios)

    def iso_bracket(self, nominator, denominator, value, mass_fraction=None):
        """Calculate the bracket ratio for a given isotope ratio and a value.

        The bracket notation is the usual astronomy / logarithmic ratio, defined as:

        result = log10(measured value) - log10(solar ratio)

        Nominator and denominator have the same restrictions as for the
        ``ele_ratio`` method.
        If one isotope ratio is defined but multiple values, the isotope ratio for
        all values is calculated and returned as a numpy array. If more than one isotope
        ratio is defined, the same number of values must be supplied as there are
        isotope ratios defined.

        :param nominator: Isotope(s) in nominator.
        :type nominator: str,list
        :param denominator: Isotope(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate bracket notation value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
        :type mass_fraction: bool

        :return: Bracket notation expression of given values with respect to the solar
            system abundances.
        :rtype: float,ndarray

        :raises ValueError: Number of element ratios and number of values supplied are
            mismatched.

        Example:
            >>> from iniabu import ini
            >>> ini.iso_bracket("Ne-21", "Ne-20", 2.397)
            3.0002854858741057
        """
        solar_ratios = return_as_ndarray(
            self.iso_ratio(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape and solar_ratios.shape != ():
            raise ValueError(
                "Length of requested isotope ratios does not match length of "
                "provided values."
            )

        return np.log10(value) - np.log10(solar_ratios)

    def ele_delta(
        self, nominator, denominator, value, mass_fraction=None, delta_factor=1000.0
    ):
        """Calculate the delta-value for a given element ratio and a value.

        The delta-value is defined as:

        result = (measured value / solar ratio - 1)

        By default, the delta-value is multiplied by 1000, thus, expressing it in
        permil. Other factors can be chosen.

        Nominator and denominator have the same restrictions as for the
        ``ele_ratio`` method.
        If one element ratio is defined but multiple values, the isotope ratio for
        all values is calculated and returned as a numpy array. If more than one element
        ratio is defined, the same number of values must be supplied as there are
        element ratios defined.

        :param nominator: Element(s) in nominator.
        :type nominator: str,list
        :param denominator: Element(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate delta-value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
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
            >>> ini.ele_delta("Ne", "Si", 3.4)
            32.39347210030586
        """
        solar_ratios = return_as_ndarray(
            self.ele_ratio(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape and solar_ratios.shape != ():
            raise ValueError(
                "Length of requested element ratios does not match length of "
                "provided values."
            )

        return (value / solar_ratios - 1) * delta_factor

    def iso_delta(
        self, nominator, denominator, value, mass_fraction=None, delta_factor=1000.0
    ):
        """Calculate the delta-value for a given isotope ratio and a value.

        The delta-value is defined as:

        result = (measured value / solar ratio - 1)

        By default, the delta-value is multiplied by 1000, thus, expressing it in
        permil. Other factors can be chosen.

        Nominator and denominator have the same restrictions as for the
        ``ele_ratio`` method.
        If one isotope ratio is defined but multiple values, the isotope ratio for
        all values is calculated and returned as a numpy array. If more than one isotope
        ratio is defined, the same number of values must be supplied as there are
        isotope ratios defined.

        :param nominator: Isotope(s) in nominator.
        :type nominator: str,list
        :param denominator: Isotope(s) in denominator.
        :type denominator: str,list
        :param value: Value(s) to calculate delta-value with respect to.
        :type value: float,ndarray
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
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
            >>> ini.iso_delta("Ne-22", "Ne-20", 0.07, delta_factor=10000)
            -479.9999999999993

            >>> # For more than 1 ratio
            >>> nominator_isos = ["Ne-21", "Ne-22"]
            >>> values = [0.01, 0.07]  # values to compare with
            >>> ini.iso_delta(nominator_isos, "Ne-20", values, delta_factor=10000)
            array([31746.24829468,  -480.        ])
        """
        solar_ratios = return_as_ndarray(
            self.iso_ratio(nominator, denominator, mass_fraction=mass_fraction)
        )
        value = return_as_ndarray(value)

        if solar_ratios.shape != value.shape and solar_ratios.shape != ():
            raise ValueError(
                "Length of requested isotope ratios does not match length of "
                "provided values."
            )

        return (value / solar_ratios - 1) * delta_factor

    def iso_int_norm(
        self,
        nominator,
        norm_isos,
        sample_values,
        sample_norm_values,
        delta_factor=10000,
        law="exp",
    ):
        """Calculate internally normalized value for isotope data with respect to solar.

        The internally normalized value requires two normalizing isotopes. This
        normalization ratios the value to one normalization isotope and uses the
        second one to correct for mass-dependent fractionation. Details can be found
        in the background section of the documentation.

        Note: A `mass_fraction` toggle, as for other routines, is useless here. Internal
        normalization, by definition, removes any fractionation effects due to mass.

        An elemental routine analogous to this one does not make sense since elemental
        ratios do usually show other effects than mass dependent ones.

        :param nominator: Name of the nominator isotope(s) to be used. Multiple can be
            selected at once by giving them as a list.
        :type nominator: str or tuple/list(str)
        :param norm_isos: The names of the normalizing isotopes. First is the major
            normalizing isotope, i.e., the one that the sample value is ratioed to.
            The second one is the isotope that is used for correcting mass fractionation
            effects.
        :type norm_isos: tuple/list(str, str)
        :param sample_values: The sample's value(s) for the nominator isotope.
            Shape must match the `nominator` name and values must be in the same order.
        :type sample_values: float, ndarray/tuple/list(floats)
        :param sample_norm_values: The sample's values for the normalization isotopes.
            Same order as the normalization isotope names.
        :type sample_norm_values: tuple/list/ndarray(float, float)
        :param delta_factor: What factor should the normalization be multiplied?
            Defaults to 10000 (for internally normalized epsilon values).
        :type delta_factor: float
        :param law: Normalization law to use: Either "exp" for exponential low or "lin"
            for linear law. Defaults to "exp"
        :type law: str

        :return: Internally normalized delta-values multiplied with given factor.
            Returns as many values as given in nominator / sample_values.
        :rtype: float, ndarray(float)

        :raises ValueError: Input values are mismatched, selected law is not valid.

        Example:
            >>> from iniabu import ini
            >>> # define input values
            >>> norm_isos = ("Ni-58", "Ni-60") # normalizing isotopes
            >>> sample_vals = (1., 0.4, 0.15, 0.5, 0.3)  # measured isotope abundances
            >>> sample_norm_vals = (sample_vals[0], sample_vals[1])  # Ni-58, Ni-60
            >>> # get the internally normalized values for all nickel isotopes
            >>> ini.iso_int_norm("Ni", norm_isos, sample_vals, sample_norm_vals)
            array([     0.        ,      0.        ,  75068.93030287,  77568.12815864,
                   189333.87185102])
        """
        # values to numpy arrays
        sample_values = np.array(sample_values)
        sample_norm_values = np.array(sample_norm_values)

        # get masses and isotope ratios for normalization isotopes
        mass_maj_norm, mass_min_norm = self.iso[norm_isos].mass
        iso_ratio_solar_norm = self.iso_ratio(norm_isos[1], norm_isos[0])

        # measured value isotope ratio
        iso_ratio_smpl_norm = sample_norm_values[1] / sample_norm_values[0]

        # get masses and ratios for nominator isotope
        mass_nominator = self.iso[nominator].mass
        iso_ratio_solar = self.iso_ratio(nominator, norm_isos[0])

        # check for input value shape mismatch
        if mass_nominator.shape != sample_values.shape and mass_nominator.shape != ():
            raise ValueError(
                "Length of requested isotope ratios does not match length of "
                "provided values."
            )

        if law == "exp":
            # calculate exponent for exponential law
            beta = np.log10(iso_ratio_smpl_norm / iso_ratio_solar_norm) / np.log10(
                mass_min_norm / mass_maj_norm
            )
            # calculate normalized ratio for sample (star ratio)
            smp_ratio = (
                sample_values
                / sample_norm_values[0]
                / (mass_nominator / mass_maj_norm) ** beta
            )
            # capital delta value
            capd_value = (smp_ratio / iso_ratio_solar - 1) * delta_factor
        elif law == "lin":
            # get the respective (lower-case) delta values
            delta_norm = self.iso_delta(
                norm_isos[1],
                norm_isos[0],
                sample_norm_values[1] / sample_norm_values[0],
                delta_factor=delta_factor,
            )
            delta_samp = self.iso_delta(
                nominator,
                norm_isos[0],
                sample_values / sample_norm_values[0],
                delta_factor=delta_factor,
            )
            # calculate mass difference ratio
            corr_factor = (mass_maj_norm - mass_nominator) / (
                mass_maj_norm - mass_min_norm
            )
            # calculate capital delta value
            capd_value = delta_samp - corr_factor * delta_norm

            capd_value = np.array(capd_value)

            # make sure the value makes sense - the rest is up to the user
            # this is kind of ugly but does the trick for now...
            if capd_value.shape == ():
                if capd_value < -delta_factor:
                    capd_value = -delta_factor
            else:
                for it, val in enumerate(capd_value):
                    if val < -delta_factor:
                        capd_value[it] = -delta_factor
        else:
            raise ValueError(
                f"The selected law {law} is invalid. Please select either 'exp' for "
                f"an exponential law or 'lin' for a linear law."
            )

        return capd_value

    def ele_ratio(self, nominator, denominator, mass_fraction=None):
        """Get the ratios of given elements.

        Nominator and denominator can be element names or lists of element names (if
        more than one ratio should be calculated). If the denominator is a list, its
        length must be identical to the list in the nominator.

        :param nominator: Element or list of elements in nominator of ratio.
        :type nominator: str,list
        :param denominator: Element or list of elements in denominator of ratio.
        :type denominator: str,list
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
        :type mass_fraction: bool

        :return: The element ratio or a numpy array of the requested ratios.
        :rtype: float,ndarray

        :raises ValueError: Denominator is a list with more than one entry and does not
            have the same length as the nominator.

        Example:
            >>> from iniabu import ini
            >>> # Calculate H/He ratio
            >>> ini.ele_ratio("H", "He")
            10.314692775474606

            >>> # Calculate same ratio as mass fraction
            >>> ini.ele_ratio("H", "He", mass_fraction=True)
            2.597460199709773

            >>> # Calculate ratios with multiple elements
            >>> ini.ele_ratio(["H", "He", "Al"], ["Si"])
            array([2.59082755e+04, 2.51178354e+03, 8.46253876e-02])

            >>> # Multiple ratios at the same time
            >>> ini.ele_ratio(["H", "He"], ["He", "H"])
            array([10.31469278,  0.09694908])

            >>> # The result when the solar abundance of an element is not avaialble
            >>> ini.database = "nist"
            >>> ini.ele_ratio("H", "He")
            nan

            >>> ini.database = "lodders09"  # set back to default and check again
            >>> ini.ele_ratio("H", "He")
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

        # get the values back, use linear units if required:
        with linear_units(self, mass_fraction=mass_fraction) as ini_tmp:
            nominator_value = ini_tmp.ele[nominator].abu_solar
            denominator_value = ini_tmp.ele[denominator].abu_solar

        ratio = nominator_value / denominator_value

        # correct if mass_fraction is true and not in mass_fraction notation already
        if mass_fraction and self.unit != "mass_fraction":
            # get masses
            nominator_masses = [data.elements_mass[ele] for ele in nominator]
            denominator_masses = [data.elements_mass[ele] for ele in denominator]
            # correct ratio
            corr_factor = utilities.return_list_simplifier(
                np.array(denominator_masses) / np.array(nominator_masses)
            )
            ratio /= corr_factor

        return ratio

    def iso_ratio(self, nominator, denominator, mass_fraction=None):
        """Get the ratios of given isotopes.

        Grabs the isotope ratios for nominator / denominator.
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
        :param mass_fraction: Are the given values in mass fractions? Defaults to None,
            which makes it dependent on the units that are currently loaded. The loaded
            setting can be overwritten by setting `mass_fraction=True` or
            `mass_fraction=False`.
        :type mass_fraction: bool

        :return: The isotope ratio or a numpy array of the requested ratios.
        :rtype: float,ndarray

        :raises ValueError: Denominator is a list with more than one entry and does not
            have the same length as the nominator.

        Example:
            >>> from iniabu import ini
            >>> # calculate Ne-21 / Ne-20 isotope ratio
            >>> ini.iso_ratio("Ne-21", "Ne-20")
            0.002395424836601307

            >>> # calculate isotope ratios for all Ne isotopes versus Ne-20
            >>> ini.iso_ratio("Ne", "Ne-20")
            array([1.        , 0.00239542, 0.07352941])

            >>> # Isotope ratios for Ne-21 and Ne-22 versus most abundant Ne isotope
            >>> ini.iso_ratio(["Ne-21", "Ne-22"], "Ne")
            array([0.00239542, 0.07352941])

            >>> # repeat this calculation assuming mass fractions
            >>> ini.iso_ratio(["Ne-21", "Ne-22"], "Ne", mass_fraction=True)
            array([0.00251541, 0.08088125])

            >>> from iniabu import inimf
            >>> # calculate Ne-21 / Ne-20 isotope ratio using mass fractions
            >>> inimf.iso_ratio("Ne-21", "Ne-20")
            0.002515409891030499

            >>> # calculate the same ratio in number fractions
            >>> inimf.iso_ratio("Ne-21", "Ne-20", mass_fraction=False)
            0.002395424836601307
        """
        # check for equal length if nominator and denominator are lists
        if not isinstance(nominator, str) and not isinstance(denominator, str):
            if len(nominator) != len(denominator) and len(denominator) != 1:
                raise ValueError(
                    "The denominator contains more than one entry but "
                    "has a different length from the nominator. This "
                    "is not allowed."
                )

        if isinstance(denominator, str) and denominator in self._ele_dict.keys():
            denominator = self._get_norm_iso(denominator)

        # get the values back:
        with linear_units(self, mass_fraction=mass_fraction) as ini_tmp:
            if self._database == "nist":
                nominator_value = ini_tmp.iso[nominator].abu_rel
                denominator_value = ini_tmp.iso[denominator].abu_rel
            else:
                nominator_value = ini_tmp.iso[nominator].abu_solar
                denominator_value = ini_tmp.iso[denominator].abu_solar

        ratio = nominator_value / denominator_value

        # correct if mass_fraction is true and not in mass_fraction notation already
        if mass_fraction and self.unit != "mass_fraction":
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
            ratio /= corr_factor

        # if nist database, we need to check for the same elements, otherwise nan
        if self._database == "nist":
            z_ratio = self.iso[nominator].z / self.iso[denominator].z  # ratio of Z
            ratio = np.where(np.array(z_ratio) == 1, np.array(ratio), np.nan)
            # ratio = utilities.return_list_simplifier(ratio)

        return ratio

    def reset_norm_isos(self):
        """Reset the user defined normalization isotopes.

        This will result in the normalization isotopes to be simple a empty dictionary
        again.

        Example:
            >>> from iniabu import ini
            >>> ini.norm_isos = {"Ba": "Ba-136"}
            >>> ini.norm_isos
            {'Ba': 'Ba-136'}
            >>> ini.reset_norm_isos()
            >>> ini.norm_isos
            {}
        """
        self._norm_isos = {}

    # PRIVATE METHODS #

    def _get_norm_iso(self, element):
        """Get the most abundant isotope for a given element.

        :param element: Element.
        :type element: str

        :return: Isotope.
        :rtype: str
        """
        if element in self._norm_isos.keys():
            return self._norm_isos[element]
        else:
            isotopes = self.ele[element].iso_a
            abus = self.ele[element].iso_abu_rel
            return f"{element}-{isotopes[abus.argmax()]}"
