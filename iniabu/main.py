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

    :param <str> database: Name of the database to read in. Must be defined in
        reading class. Defaults to lodders09

    Current possibilities for databases that are included are:

    - lodders09

    """

    def __init__(self, database="lodders09"):
        """
        Initializes iniabu
        """
        # save database
        self._database = database

        # initialize dictionaries
        self._ele_dict, self._iso_dict = data.database_selector(database)
