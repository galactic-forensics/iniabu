"""Utility functions."""

from contextlib import contextmanager
import copy

import numpy as np

from . import data

# CLASSES #


class ProxyList:
    """Proxy for accessing elements and isotopes as lists.

    This class is inspired by a class with the same name from the project
    ``InstrumentKit`` by Galvant Industries. It is used to generate lists of objects.
    The valid keys are defined by the `valid_set` initialization parameter. This allows
    generating a single property for elements and isotopes to access them.

    `InstrumentKit <https://github.com/Galvant/InstrumentKit>`_
    """

    def __init__(self, parent, proxy_cls, valid_set, *args, **kwargs):
        """Initialize a ProxyList object.

        :param parent: The "parent" of the of the proxy classes. In python, this is
            usually `self`
        :type parent: class
        :param proxy_cls: The child class that will be returned when the returned
            object is iterated through.
        :type proxy_cls: class
        :param valid_set: The set of valid keys by which the proxy class objects
            are accessed.
        :type valid_set: list
        :param *args: Variable length argument list.
        :param **kwargs: Arbitrary keyword arguments.
        """
        self._parent = parent
        self._proxy_cls = proxy_cls
        self._valid_set = valid_set

        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        """Yield iterator of the proxy list."""
        for idx in self._valid_set:
            yield self._proxy_cls(self._parent, idx, *self.args, **self.kwargs)

    def __getitem__(self, idx):
        """Get an item from the proxy list."""
        if hasattr(idx, "copy"):
            idx = idx.copy()  # do not modify user input
        # turn idx into a list
        if isinstance(idx, tuple):
            idx = list(idx)
        # turn into list if required
        idx = return_string_as_list(idx)

        for it, entry in enumerate(idx):
            entry = item_formatter(entry)
            idx[it] = entry
            if entry not in self._valid_set:
                raise IndexError(
                    "Item {} out of range. Must be "
                    "in {}.".format(entry, self._valid_set)
                )
        return self._proxy_cls(self._parent, idx, *self.args, **self.kwargs)

    def __len__(self):
        """Get length of the valid set."""
        return len(self._valid_set)


# FUNCTIONS #


def get_all_available_isos(ele):
    """Get all available isotopes of a given element, stable and unstable.

    This is particularly interesting if we want to know the mass of unstable isotopes.

    :param ele: Element name
    :type ele: str

    :return: All isotopes of the element as a list.
    :rtype: list(str)
    """
    all_iso_list = list(data.isotopes_mass_all.keys())
    ret_val = [
        entry for entry in all_iso_list if entry.split("-")[0].lower() == ele.lower()
    ]
    return ret_val


def get_all_stable_isos(ini, ele):
    """Get all isotopes of a given element.

    :param ini: Initialized iniabu instance
    :type ini: IniAbu
    :param ele: Element name
    :type ele: str

    :return: All isotopes of the element as a list.
    :rtype: list(str)
    """
    isotopes = ini.ele[ele].iso_a
    ret_val = [f"{ele}-{isotope}" for isotope in isotopes]
    return ret_val


def item_formatter(iso: str) -> str:
    """Transform `iso` into correct format, e.g,. from `46Ti` to `Ti-46`.

    Also appropriately capitalizes isotopes and elements.

    Supported formats:
    - `46Ti`
    - `Ti46`
    - `Ti-46`

    :param iso: Isotope as string or element name.

    :return: iso, but in transformed notation and capitalized
    """
    if "-" in iso:
        iso_split = iso.split("-")
        return f"{iso_split[0].capitalize()}-{iso_split[1]}"
    elif iso[0].isnumeric():  # mass number comes first
        index_to = None
        for it, char in enumerate(iso):
            if not char.isnumeric():
                index_to = it
                break
        return f"{iso[index_to:].capitalize()}-{iso[:index_to]}"
    elif iso[-1].isnumeric():  # mass number comes last
        index_to = None
        for it, char in enumerate(iso):
            if char.isnumeric():
                index_to = it
                break
        return f"{iso[:index_to].capitalize()}-{iso[index_to:]}"
    else:
        return iso.capitalize()  # no rule applied, return input (e.g., elements)


@contextmanager
def linear_units(ini, mass_fraction):
    """Context manager to turn current instants units linear if logarithmic.

    This is used mainly for ratio calculation, since logarithmic cannot be ratioed
    to each other.

    :param ini: Initialized iniabu instance
    :type ini: `IniAbu`
    :param mass_fraction: Mass fraction variable passed on from last routine
    :type mass_fraction: bool or None

    :yield: `ini` as with adjusted units (if necessary)
    :ytype: `IniAbu` instance
    """
    current_units = ini.unit

    try:  # change units if necessary
        if current_units == "num_log":
            ini.unit = "num_lin"
        # to avoid rounding err
        elif current_units == "mass_fraction" and mass_fraction is False:
            ini.unit = "num_lin"
        yield ini
    finally:  # reset units
        ini.unit = current_units


def make_iso_dict(element_dict):
    """Make an isotope dictionary from an element dictionary.

    :param element_dict: Element dictionary.
    :type element_dict: dict

    :return: Isotope dictionaries with same abundances as element dictionary.
    :rtype: dict
    """
    iso_keys = []
    iso_entries = []
    for key in element_dict.keys():
        for it, iso in enumerate(element_dict[key][1]):
            iso_keys.append(f"{key}-{iso}")
            rel_abu = element_dict[key][2][it]
            ss_abu = element_dict[key][3][it]
            iso_entries.append([rel_abu, ss_abu])
    return dict(zip(iso_keys, iso_entries))


def make_log_abu_dict(element_dict):
    """Make element and isotope dictionaries for logarithmic abundances.

    This routine takes an element dictionary with linear abundances, normed to Si
    equals 1e6, and returns new dictionaries with logarithmic abundances, normed to
    log10(Nx/NH) + 12, where Nx is the number abundance of the element in question and
    NH is the number abundance of hydrogen.

    :param element_dict: Element dictionary.
    :type element_dict: dict

    :return: Element and isotope dictionaries with logarithmic solar abundances.
    :rtype: dict,dict
    """
    # get hydrogen abundance
    abu_h = element_dict["H"][0]

    # create a renormalized element dictionary
    ele_keys = element_dict.keys()
    ele_entries = []

    # fill keys, entries for dictionary formation
    for key in ele_keys:
        # original values
        ss_abu_lin = element_dict[key][0]
        isos = element_dict[key][1]
        rel_abu = element_dict[key][2]
        # calculate new
        ss_abu_log = np.log10(ss_abu_lin / abu_h) + 12.0
        # create temporary list to later append to, then append to entries
        tmp_entry = [ss_abu_log, isos, rel_abu]
        # isotope abundances
        iso_ss_abu_log = [
            np.log10(rel_a * ss_abu_lin / abu_h) + 12.0 for rel_a in rel_abu
        ]
        tmp_entry.append(iso_ss_abu_log)
        # append to full list
        ele_entries.append(tmp_entry)

    # form new dictionary
    element_dict_log = dict(zip(ele_keys, ele_entries))

    # isotope dictionary
    isotope_dict_log = make_iso_dict(element_dict_log)

    return element_dict_log, isotope_dict_log


def make_mf_dict(element_dict):
    """Make element and isotope dictionaries for mass fractions.

    This routine takes an element dictionary with linear abundances, normed to Si
    equals 1e6, and returns new dictionaries with mass fractions. The mass fraction
    Xi of an isotope i is defined as Xi = Ni mi / sum(Ni mi). Here, Ni is the number
    abundance of a element / isotope i and mi is its mass.

    :param element_dict: Element dictionary.
    :type element_dict: dict

    :return: Element and isotope dictionaries with mass fractions.
    :rtype: dict,dict
    """
    ele_keys = element_dict.keys()

    # create the sum of all using isotopes and isotope masses
    abu_sum = 0.0
    for key in ele_keys:
        for it, iso in enumerate(element_dict[key][1]):
            iso_abu = element_dict[key][3][it]
            iso_mass = data.isotopes_mass[f"{key}-{iso}"]
            abu_sum += iso_abu * iso_mass

    # make element mass fraction dictionary make abundance
    element_dict_mf = copy.deepcopy(element_dict)
    for key in ele_keys:
        ele_abu_mf = 0.0
        for it, iso in enumerate(element_dict_mf[key][1]):
            iso_abu = element_dict_mf[key][3][it]
            iso_mass = data.isotopes_mass[f"{key}-{iso}"]
            iso_abu_mf = iso_abu * iso_mass / abu_sum
            ele_abu_mf += iso_abu_mf
            element_dict_mf[key][3][it] = iso_abu_mf
        element_dict_mf[key][0] = ele_abu_mf

    # # correct relative isotope abundances to be relative by weight!
    for key in ele_keys:
        abu_sum = sum(element_dict_mf[key][3])
        for it, sol_abu_val in enumerate(element_dict_mf[key][3]):
            element_dict_mf[key][2][it] = sol_abu_val / abu_sum

    # make isotope mass fraction dictionary
    isotope_dict_mf = make_iso_dict(element_dict_mf)

    return element_dict_mf, isotope_dict_mf


def return_as_ndarray(val):
    """Return the input as a ndarray.

    :param val: Input value.
    :type val: int,float,list,tuple,ndarray

    :return: Array of input value if not an array, otherwise return itself.
    :rtype: ndarray
    """
    if isinstance(val, np.ndarray):
        return val
    if isinstance(val, list) or isinstance(val, tuple):
        return np.array(return_list_simplifier(val))
    else:
        return np.array(val)


def return_string_as_list(s):
    """Return the input as a list.

    :param s: Input value.
    :type s: str,list

    :return: List of input value if not a list, otherwise return itself.
    :rtype: list
    """
    if isinstance(s, list):
        return s
    else:
        return [s]


def return_list_simplifier(return_list):
    """Simplify standard return values.

    Specifically written for classes with multiple return types, such as
    :class:`iniabu.elements.Elements` and :class:`iniabu.isotopes.Isotopes`. If only
    one entry is in the list, it should not be returned as a list but as a value.
    Otherwise, return the list.

    :param return_list: List or numpy array with the value to be returned.
    :type return_list: list,ndarray

    :return: If only one entry in list, return that entry. Otherwise return list.
    """
    length = len(return_list)
    if length == 0:
        return None
    elif len(return_list) == 1:
        return return_list[0]
    else:
        return return_list
