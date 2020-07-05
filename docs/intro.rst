Introduction
------------

What it does


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


Issues and feature requests
---------------------------

If you find a bug or have other problems or questions
with this project, have a look at the
`GitHub issue page <https://github.com/galactic-forensics/iniabu/issues>`_.
Your issue might already have been discussed.
Otherwise feel free to open a new issue.
Please be as detailed as possible.

If you would like a new feature,
please feel free to file a feature request.
If you are interested in contributing
this feature yourself, say so and we can
help to get you started.


Contributing
------------

Contributions to this project are welcome.
Please see the
`Developers Guide <dev>`_
for detailed instructions on how to contribute.


Relationship to previous package
--------------------------------
This package is loosely based on a
software package that was I wrote at
Lawrence Livermore National Laboratory,
and replaces that specific package,
which can in it's archived form be found
`here <https://github.com/LLNL/iniabu>`_.
That package's latest release was v0.3.1
and it was released under GPLv2.
Note that only the basic idea behind
the two packages are identical.
The codebase for this version was
rewritten from ground-up.

This is a new and improved version
that is also available as a PyPi package
and replaces that older version.
The new package is not backwards compatible
and is initially released as v1.0.0.
