The Iniabu Project
==================

.. image:: https://readthedocs.org/projects/iniabu/badge/?version=latest
    :target: https://iniabu.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/iniabu?color=informational
    :target: https://pypi.org/project/iniabu/
    :alt: PyPi
.. image:: https://github.com/galactic-forensics/iniabu/actions/workflows/package_testing.yml/badge.svg
    :target: https://github.com/galactic-forensics/iniabu
    :alt: tests
.. image:: https://codecov.io/gh/galactic-forensics/iniabu/branch/main/graph/badge.svg?token=P2SJEANE6S
    :target: https://codecov.io/gh/galactic-forensics/iniabu
    :alt: Code coverage
.. image:: https://img.shields.io/badge/License-GPL%20v2-blue.svg
    :target: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html
    :alt: License: GPL v2

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
More information can also be found in the
:doc:`scientific background section <background>`.
Aside from querying the databases,
the ``iniabu`` tool allows you directly
to calculate isotope ratios,
δ-values,
or ratios in bracket notation
(the usual astronomy / logarithmic ratio notation)
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
   config
   background
   license
   api/index
   dev/index
