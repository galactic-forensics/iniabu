"""
Todo License text and copyright
"""

from . import read_data


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
        if database not in read_data.reader_dict.keys():
            raise FileNotFoundError(
                "The database {} could not be found. Make sure it exists and that the "
                "appropriate reader methods are implemented as well."
            )

    def temp(self, x):
        """
        This is the doc string for the temp function. Adds one to whatever goes in.

        :param <float> x: Whatever comes in

        :return: Returns whatever comes in + 1
        :rtype: <float>
        """
        return x + 1
