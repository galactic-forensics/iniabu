The iniabu project
!!!!!!!!!!!!!!!!!!

.. image:: https://readthedocs.org/projects/iniabu/badge/?version=latest
    :target: https://iniabu.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/iniabu
    :target: https://pypi.org/project/iniabu/
    :alt: PyPi
.. image:: https://github.com/galactic-forensics/iniabu/workflows/tests/badge.svg?branch=master
    :target: https://github.com/galactic-forensics/iniabu
    :alt: tests
.. image:: https://github.com/galactic-forensics/iniabu/workflows/xdoctest/badge.svg?branch=master
    :target: https://github.com/Erotemic/xdoctest
    :alt: xdoctest
.. image:: https://coveralls.io/repos/github/galactic-forensics/iniabu/badge.svg?branch=master
    :target: https://coveralls.io/github/galactic-forensics/iniabu?branch=master
    :alt: coverage
.. image:: https://img.shields.io/badge/License-GPL%20v2-blue.svg
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
    :alt: License: GPL v2
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black


============
Introduction
============

- What problem does this project solve

Available databases
-------------------
Currently, several databases are available to work with. The default database is
called ``lodders09`` and is based on
`Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_. Further
databases, listed by the string used to call them, are as following:

- ``asplund09``: `Asplund et al. (2009) <https://doi.org/10.1146/annurev.astro.46.060407.145222>`_
- ``lodders09`` (default): `Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_
- ``nist``: `NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_

The solar abundances of all databases were converted to number abundances and
are relative to `Si = 1e6`. Conversion to dex, as described below, is possible.

*Note*: Not all databases mentioned here contain the solar abundances. If an
operation that you are trying to perform requires the solar abundance to be
available, the result will be return as an ``np.nan``, i.e., as not a number.


Basic usage
-----------

Importing the module:
~~~~~~~~~~~~~~~~~~~~~

Loading a database:
~~~~~~~~~~~~~~~~~~~

Putting the solar abundances into logarithmic mode:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Querying element and isotope properties:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Properties of an element are independent from the loaded database and are taken from
the `NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_.
To query the loaded database for relative or solar abundances, see the next two sections.

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


Issue tracking and feature requests
-----------------------------------

.. FAQ

Developer instructions
----------------------

Relationship to previous package
--------------------------------
This package is loosely based on a software package that was I wrote at
Lawrence Livermore National Laboratory and replaces that specific
package, which can in it's archived form be found
https://github.com/LLNL/iniabu. That package's latest release was v0.3.1
and it was released under GPLv2. Note that only the basic idea behind
the two packages are identical. The codebase for this version was
rewritten from ground-up.

This is a new and improved version that is also available as a PyPi
package and replaces that older version. The new package is not
backwards compatible and is initially released as v1.0.0.

License
-------



=========================
Installation Instructions
=========================

The ``iniabu`` package can be installed via pip. You can install the latest release via::

 pip install iniabu

Alternatively, you can install the latest development version from github via::

 pip install git+https://github.com/galactic-forensics/iniabu.git

Dependencies
------------

Most of the required and optional dependencies can be obtained using  ``pip``.

Required Dependencies
~~~~~~~~~~~~~~~~~~~~~

Using ``pip``, these requirements can be obtained automatically by using the
provided ``requirements.txt``::

 pip install -r requirements.txt

- NumPy

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~
For development purposes, additional requirements can be installed with::

 pip install -r dev-requirements

Please also see the developers guide (Todo link). The following packages, which can
be installed with ``pip`` as well, are furthermore recommended:

- ``black``: Automatic code formatting to adhere to the formatting guidelines of the project.
- ``coverage``: To display graphical coverage in a browser.
- ``nox``: Testing in various environments
- ``sphinx``: Documentation generation
