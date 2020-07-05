"""Utility functions."""

# CLASSES #


class ProxyList(object):
    """Proxy for accessing elements and isotopes as lists.

    This class is inspired by a class with the same name from the project
    ``InstrumentKit`` by Galvant Industries. It is used to generate lists of objects.
    The valid keys are defined by the `valid_set` initialization parameter. This allows
    generating a single property for elements and isotopes to access them.

    `InstrumentKit <https://github.com/Galvant/InstrumentKit>`_
    """

    def __init__(self, parent, proxy_cls, valid_set):
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
        """
        self._parent = parent
        self._proxy_cls = proxy_cls
        self._valid_set = valid_set

    def __iter__(self):
        """Yield iterator of the proxy list."""
        for idx in self._valid_set:
            yield self._proxy_cls(self._parent, idx)

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
        return self._proxy_cls(self._parent, idx)

    def __len__(self):
        """Get length of the valid set."""
        return len(self._valid_set)


# FUNCTIONS #


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
