"""Initializes all the data."""

from .asplund09 import asplund09_elements, asplund09_isotopes
from .lodders09 import lodders09_elements, lodders09_isotopes
from .nist15 import (
    elements_mass,
    elements_z,
    isotopes_mass,
    nist15_elements,
    nist15_isotopes,
)
from .nist15_isomasses_all import isotopes_mass as isotopes_mass_all

__all__ = [
    "asplund09_elements",
    "asplund09_isotopes",
    "lodders09_elements",
    "lodders09_isotopes",
    "elements_mass",
    "elements_z",
    "isotopes_mass",
    "nist15_elements",
    "nist15_isotopes",
    "isotopes_mass_all",
]


def database_selector(db):
    """Select the database to be used.

    Selects the correct database and returns the element and isotope dictionary.

    :param db: Database to be read in
    :type db: str

    :return: elements_dictionary, isotopes_dictionary
    :rtype: tuple<dict, dict>

    :raises ValueError: An invalid database was selected.
    """
    if db == "nist":
        return nist15_elements, nist15_isotopes
    elif db == "lodders09":
        return lodders09_elements, lodders09_isotopes
    elif db == "asplund09":
        return asplund09_elements, asplund09_isotopes
    else:
        raise ValueError(
            "The database {} could not be found. Make sure it is a valid option or "
            "choose one of the available ones.".format(db)
        )
