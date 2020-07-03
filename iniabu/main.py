"""
Todo License text and copyright
"""

import os
from . import data
from .elements import Elements
from .isotopes import Isotopes
from .utilities import ProxyList


class IniAbu(object):

    """
    Initialize the IniAbu class. By default, lodders09 is read in. A valid data
    reader must exist for the chose
    datafile. This goes even more over the line now.

    Current possibilities for databases that are included are:

    - ``nist``: Current (as of 2020) NIST isotopic abundances.
    - ``lodders09``: Lodders et al. (2009), doi: 10.1007/978-3-540-88055-4_34

    :param str database: Name of the database to read in. Must be defined in reading
        class. Defaults to lodders09.
    """

    def __init__(self, database="lodders09"):
        """Initialize IniAbu."""
        # init parameters
        self._database = None

        # set database
        self.database = database

    # PROXY LISTS #

    @property
    def element(self):
        """
        Gets a specific element and the associated information. This represents a
        convenient way to dig through elemental information. More information and a
        full list of properties can be found in the :doc:`Elements </api/elements>`
        class.

        Example::

         from iniabu import ini
         # get the solar abundance of silicon, store to var1
         var1 = ini.element["Si"].solar_abundance

         # get a numpy array of the solar abundance of two elements, store to var2
         var2 = ini.element[["Fe", "Ni"]].solar_abundance

         # get a list of all atomic numbers for isotopes of helium, store to var3
         var3 = ini.element["He"].isotopes_a

         # similarly, query isotopes relative abundances, and solar abundances
         var4 = ini.element["He"].isotopes_relative_abundance
         var5 = ini.element["He"].isotopes_solar_abundance
        """
        return ProxyList(self, Elements, self._ele_dict.keys())

    @property
    def isotope(self):
        """
        Gets a specific isotope and the associated information. This represents a
        convenient way to dig through isotope information. More information and a
        full list of properties can be found in the :doc:`Isotopes </api/isotopes>`
        class.

        Example::

         from iniabu import ini
         # get the solar abundance of Si-28, store to var1
         var1 = ini.isotope["Si-28"].solar_abundance

         # get a numpy array of the solar abundance of two isotopes, store to var2
         var2 = ini.isotope[["Fe-56", "Ni-60"]].solar_abundance

         # similarly, query relative abundance(s) of isotope(s)
         var4 = ini.isotope["He-4"].relative_abundance
         var5 = ini.isotope[["H-2", "He-3"]].relative_abundance
        """
        return ProxyList(self, Isotopes, self._iso_dict.keys())

    # PROPERTIES #

    @property
    def database(self):
        """
        Gets / Sets the current database. A string is expected with the database
        name, as if the class was freshly initialized.

        Example::

         from iniabu import ini  # loads `lodders09` by default
         ini.database = "nist"  # change database to `nist`
         print(ini.database)  # print out which database is loaded

        """
        return self._database

    @database.setter
    def database(self, db):
        self._ele_dict, self._iso_dict = data.database_selector(db)
        self._database = db

    @property
    def ele_dict(self):
        """
        Gets the element dictionary and returns it. There is no setter for this, the
        element dictionary needs to be set by choosing a database.
        """
        return self._ele_dict

    @property
    def iso_dict(self):
        """
        Gets the isotope dictionary and returns it. There is no setter for this, the
        isotope dictionary needs to be set by choosing a database.
        """
        return self._iso_dict

    # METHODS #
