from .nist15 import (
    elements_mass,
    elements_z,
    isotopes_mass,
    nist15_elements,
    nist15_isotopes,
)

from .lodders09 import lodders09_elements, lodders09_isotopes


def database_selector(db):
    """
    Selects the correct database and returns the element and isotope dictionary.

    :param <str> db: Database to be read in

    :return: elements_dictionary, isotopes_dictionary
    :rtype: <dict>, <dict>
    """
    if db == "nist":
        return nist15_elements, nist15_isotopes
    elif db == "lodders09":
        return lodders09_elements, lodders09_isotopes
    else:
        raise ValueError(
            "The database {} could not be found. Make sure it is a valid option or "
            "choose one of the available ones.".format(db)
        )
