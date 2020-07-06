"""IniAbu class - the heart of the package.

This file contains the main `IniAbu` class.
"""

from . import data
from . import utilities
from .elements import Elements
from .isotopes import Isotopes
from .utilities import ProxyList


class IniAbu(object):
    """Initialize the IniAbu class.

    By default, the ``lodders09`` database is read in. Available databases are:

    - ``asplund09``: Asplund et al. (2009), doi: 10.1146/annurev.astro.46.060407.145222
    - ``lodders09``: Lodders et al. (2009), doi: 10.1007/978-3-540-88055-4_34
    - ``nist``: Current (as of 2020) NIST isotopic abundances.

    Todo Example
    """

    def __init__(self, database="lodders09"):
        """Initialize IniAbu.

        Load and set the default database.

        :param database: Database to initialize the class with, defaults to
            ``lodders09``.
        :type database: str
        """
        # init parameters
        self._database = None
        self._log_abu = False

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
        return ProxyList(self, Elements, self._ele_dict.keys(), log_abu=self._log_abu)

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
        return ProxyList(self, Isotopes, self._iso_dict.keys(), log_abu=self._log_abu)

    # PROPERTIES #

    @property
    def abundance_unit(self):
        """Get / Set the unit for the solar abundances.

        Routine to easily switch the database between the **default** linear number
        abundances, normed to Si with an abundance of 1e6 (``lin``, typically used
        in cosmo- and geochemistry studies) or the logarithmic (``log``, typically used
        in astronomy) abundance units, normed to H as 12.

        :setter: Unit to set, either "lin" (default) or "log".
        :type: str

        :return: Currently set unit.
        :rtype: str

        Example:
            >>> from iniabu import ini  # loads with default linear units
            >>> ini.abundance_unit
            'lin'

            >>> ini.abundance_unit = "log"  # set logarithmic abundance unit
            >>> ini.element["H"].solar_abundance
            12.0
        """
        return "log" if self._log_abu else "lin"

    @abundance_unit.setter
    def abundance_unit(self, s):
        self._log_abu = True if s == "log" else False

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
        """
        return self._database

    @database.setter
    def database(self, db):
        self._ele_dict, self._iso_dict = data.database_selector(db)
        (
            self._ele_dict_log,
            self._iso_dict_log,
        ) = utilities.make_log_abundance_dictionaries(self._ele_dict)
        self.abundance_unit = "lin"
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

    # METHODS #
