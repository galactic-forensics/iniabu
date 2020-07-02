"""
Todo License text and copyright
"""

import os
from . import data


class IniAbu:

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
        # save database
        self._database = database

        # initialize dictionaries
        self._ele_dict, self._iso_dict = data.database_selector(database)
