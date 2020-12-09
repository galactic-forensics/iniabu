The Iniabu Project
==================

.. image:: https://readthedocs.org/projects/iniabu/badge/?version=latest
    :target: https://iniabu.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/iniabu?color=informational
    :target: https://pypi.org/project/iniabu/
    :alt: PyPi
.. image:: https://github.com/galactic-forensics/iniabu/workflows/tests/badge.svg?branch=master
    :target: https://github.com/galactic-forensics/iniabu
    :alt: tests
.. image:: https://github.com/galactic-forensics/iniabu/workflows/doctests/badge.svg?branch=master
    :target: https://github.com/galactic-forensics/iniabu
    :alt: doctests
.. image:: https://coveralls.io/repos/github/galactic-forensics/iniabu/badge.svg?branch=master
    :target: https://coveralls.io/github/galactic-forensics/iniabu?branch=master
    :alt: coverage
.. image:: https://img.shields.io/badge/License-GPL%20v2-blue.svg
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
    :alt: License: GPL v2
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black
.. image:: https://github.com/galactic-forensics/iniabu/workflows/CodeQL/badge.svg
    :target: https://github.com/galactic-forensics/iniabu
    :alt: CodeQL

Introduction
------------

The goal of this project is to give you access
to various published solar abundance tables of elements as isotopes
from a Python terminal.
As one might guess,
``iniabu`` stands for initial abundances.
Functions that are useful for everyday's life as an
astrophysicist, cosmo-, or geochemist,
are here made available in an easy to use interface.
You can find more information on the scientific background
:doc:`here <background>`.
Aside from querying the databases,
the ``iniabu`` tool allows you directly
to calculate isotope ratios,
δ-values,
or ratios in bracket notation
for fast comparison with your observations or measurements.
These calculations can also be performed "numpy-style",
i.e., element-wise on whole arrays.

The iniabu project is a young undertaking
of the newly established
`Galactic Forensics Laboratory <https://galactic-forensics.space>`_.
We strive to support the open source culture
and would be happy to hear how you use this tool,
but also to see what you would like to have improved.

To get you started,
check out the :doc:`Installation and Usage <intro>` page.
If you would like to contribute,
which we for sure welcome,
please have a look at our,
hopefully detailed,
:doc:`Developers Guide </dev/index>`.
We welcome all contributions,
from simple typo fixes in the documentation,
to feature contributions!

.. note:: Currently the package is still in testing
  and has not been released on PyPi as v1.0.0.
  You can always check the badge above to see
  which version is currently available on PyPi.
  Please follow the instructions on the
  :doc:`Installation and Usage <intro>`
  page to see how to install the package from GitHub.


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
This package is in its idea based on a
software package that was was written at
Lawrence Livermore National Laboratory,
and replaces that specific package,
which can in it's archived form be found
`here <https://github.com/LLNL/iniabu>`_.
That package's latest release was v0.3.1
and it was released under GPLv2.
Note that the codebase for this version was
rewritten from ground-up.

This new and improved version
is available on PyPi
and replaces the previous version there.
The new package is not backwards compatible
and is initially released as v1.0.0.


Contents
--------

.. toctree::
   :maxdepth: 2

   intro
   background
   license
   api/index
   dev/index
