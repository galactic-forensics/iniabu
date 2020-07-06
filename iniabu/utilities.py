"""Utility functions."""

import numpy as np

# CLASSES #


class ProxyList(object):
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
        # turn idx into a list
        if isinstance(idx, tuple):
            idx = list(idx)
        if not isinstance(idx, list):
            idx = [idx]

        for it in idx:
            if it not in self._valid_set:
                raise IndexError(
                    "Item {} out of range. Must be "
                    "in {}.".format(it, self._valid_set)
                )
        return self._proxy_cls(self._parent, idx, *self.args, **self.kwargs)

    def __len__(self):
        """Get length of the valid set."""
        return len(self._valid_set)


# FUNCTIONS #


def make_log_abundance_dictionaries(element_dict):
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
    iso_keys = []
    iso_entries = []
    for key in element_dict_log.keys():
        for it, iso in enumerate(element_dict_log[key][1]):
            iso_keys.append("{}-{}".format(key, iso))
            rel_abu = element_dict_log[key][2][it]
            ss_abu = element_dict_log[key][3][it]
            iso_entries.append([rel_abu, ss_abu])
    isotope_dict_log = dict(zip(iso_keys, iso_entries))

    return element_dict_log, isotope_dict_log


def return_value_simplifier(return_list):
    """Simplifies standard return values.

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
