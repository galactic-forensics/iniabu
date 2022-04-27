Configurations
==============


Normalization isotope
---------------------

Throughout this package,
you are able to set isotope ratios
by selecting an element for the denominator.
In these cases,
``iniabu`` will by default select the most abundant isotope
of this element as the normalizing one.
However,
you can configure ``iniabu`` to overwrite this behavior.
This especially handy if you want to normalize ratios
by default to another isotope.
For example,
barium is often normalized to :sup:`136`\Ba
instead of the most abundant :sup:`138`\Ba.
In order to set this isotope as the main one,
you can run the following:

.. code-block:: python

    >>> from iniabu import ini
    >>> ini.norm_isos = {"Ba": "Ba-136"}

The ``ini.norm_isos`` property
holds a dictionary with user defined normalization / main isotopes.
You can add more isotopes after the fact:

.. code-block:: python

    >>> ini.norm_isos = {"Si": "Si-29"}
    >>> ini.norm_isos
    {'Ba': 'Ba-136', 'Si': 'Si-29'}

This would now hold both normalization isotopes
that were defined.
To reset the dictionary,
run:

.. code-block:: python

    >>> ini.reset_norm_isos()
