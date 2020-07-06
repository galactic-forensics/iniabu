Installation and Usage
======================


Installation
------------

To install the iniabu project,
run this command in your terminal:

.. code-block:: console

   $ pip install iniabu

Alternatively you can install the inabu project directly from GitHub.
To do so, type in your terminal:

.. code-block:: console

    $ pip install git+https://github.com/galactic-forensics/iniabu.git


Available databases
-------------------
Several databases are available to work with.
The default database is called ``lodders09``
and is based on
`Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_.
Further databases,
listed by the string used to call them,
are as following:

- ``asplund09``: `Asplund et al. (2009) <https://doi.org/10.1146/annurev.astro.46.060407.145222>`_
- ``lodders09`` (default): `Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_
- ``nist``: `NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_

The solar abundances of all databases
were converted to number abundances
and are relative to `Si = 1e6`.
Conversion to dex, as described below, is possible.

*Note*: Not all databases mentioned here
contain the solar abundances.
If an operation that you are trying to perform
requires the solar abundance to be available,
the result will be return as an ``np.nan``,
i.e., as not a number.


Usage
-----

Importing the module:
~~~~~~~~~~~~~~~~~~~~~

Loading a database:
~~~~~~~~~~~~~~~~~~~

Putting the solar abundances into logarithmic mode:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Querying element and isotope properties:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Properties of an element are independent from the loaded database
and are taken from the
`NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_.
To query the loaded database for relative or solar abundances,
see the next two sections.

Querying an element:
~~~~~~~~~~~~~~~~~~~~

Querying an isotope:
~~~~~~~~~~~~~~~~~~~~

Isotope ratios:
~~~~~~~~~~~~~~~

δ-values:
~~~~~~~~~

Bracket-notation:
~~~~~~~~~~~~~~~~~



