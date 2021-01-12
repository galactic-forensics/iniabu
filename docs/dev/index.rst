.. _dev:

Developer Reference
===================

First off,
please make sure you have read and understood
our code of conduct.
We expect everybody to adhere to it.
You can find this project's
code of condact
`here <https://github.com/galactic-forensics/iniabu/blob/main/CODE_OF_CONDUCT.md>`_.

To get started with developing,
fork the github repository and
clone it into a local directory.
If this is your first time
contributing to an open-source project,
have a look at
`these general guidelines <https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution>`_.

This project uses fairly tight restrictions
in terms of testing and linting.
Don't be discouraged if you run into issues.
Always feel free to ask questions by
`raising an issue <https://github.com/galactic-forensics/iniabu/issues>`_.
Many style guides and ideas here are taken from the
`Hypermodern Python <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>`_
blog created by Claudio Jolowicz.
These blog post,
while intense,
are an excellent read and are highly recommended.


Dependencies
------------

For full testing of the project,
you should have the supported python versions installed.
Furthermore, you need to install ``nox``,
which can be done from the console by typing:

.. code-block:: console

    $ pip install nox

If you completely test your setup with ``nox``,
dependency installation is not required.
If you like to test directly with ``pytest``,
write your own temporary routines,
create examples, etc.,
you can install the dependencies
from your console by typing:

.. code-block:: console

    $ pip install -r requirements.txt
    $ pip install -r dev-requirements.txt


Contribution requirements
-------------------------

All code submissions should be tested.
The CI requires that all unit tests
and lint tests complete successfully
before merging into the main branch is allowed.


**Coverage:**

All code should be tested.
Code testing coverage of 100% is required
to ensure future integrity.


**Docstrings:**

The documentation automatically generates
the API reference from the supplied docstrings.
Please use
`Sphinx style <https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html>`_
docstrings to document your routines.


**Linting:**

All code must adhere to ``flake8`` specifications,
see also :ref:`section_linting`.
This allows for better readability.
Even though you won't remember all linting rules,
you should go back and fix linting issues after testing.
The tests will give you feedback on what to do.



Test driven development
-----------------------

Testing of the ``iniabu`` package is done using ``pytest``
and automated using ``nox``.
To run a full test using ``nox``,
Python 3.6, 3.7, 3.8, and 3.9,
must be available in the environment.
A full nox test, which includes
linting, safety, and tests
can be run from the terminal by typing:

.. code-block:: console

    $ nox

To check wha sessions are implemented,
run the following code from your terminal:

.. code-block:: console

    $ nox -l

This will also display information
for all sessions implemented in ``nox``.
You can also check out the ``noxfile.py`` directly.

Please also check the
`nox documentation <https://nox.thea.codes/en/stable/index.html>`_
for further options, etc.

The test suite lives in the ``tests`` folder.
This folder mirrors the package structure.
In addition,
a file named ``conftest.py``
is used to set fixtures for pytest.
This allows for proper initialization
of the package with every test.

The iniabu project requires that the whole code base
is covered with tests, i.e.,
that a code coverage of 100% is maintained.
Of course, the tests should also be meaningful!
This code coverage ensures that future developments
do not break other functionalities.
More about this can be found in
:ref:`section_testing`.

**Example: Bugfix**

If a bug is found in the code and reported,
a bug fix should be implemented in the following way:

#. Write a test with the wanted outcome
   and make sure the test suite fails
   due to the reported bug.
#. Fix the bug in the source code.
#. The bug is fixed once tew new test
   passes successfully
   and no other tests were broken.


Formatting with ``black``
~~~~~~~~~~~~~~~~~~~~~~~~~

The iniabu project adopts the default style
that is provided by the
`black python formatter <https://github.com/psf/black>`_.
Their GitHub site describes in detail
how to use the formatter.
There is really not much to configure.

If you are using
`PyCharm <https://www.jetbrains.com/pycharm/>`_
as you editor,
have a look at the
`BlackConnect <https://plugins.jetbrains.com/plugin/14321-blackconnect>`_
plugin.
Make sure that no options are checked
in the section ``Formatting options``.

Alternatively, a ``nox`` session is implemented
to automatically format code with ``black``.
To do so,
run the following command from your terminal:

.. code-block:: console

    $ nox -rs black

As an alternative,
the pre-commit hook can also be used
to format your code using black.
Check out section
:ref:`section_hooks`
for more information.

.. caution:: Make sure that you use
  the correct version of black,
  especially when formatting
  differently from using ``nox``
  or the pre-commit hook.
  You can find the currently used version
  in the `noxfile.py`.


.. _section_linting:


Linting
~~~~~~~

Linting heavily improves code readability.
Please follow all linting guidelines.
We use ``flake8``.
Furthermore, the following additional plugins are used:

* ``flake8-bandit`` to identify security issues.
* ``flake8-black`` to check that the codebase is formatted using black.
* ``flake8-bugbear`` to find additional bugs and design problems.
* ``flake8-docstrings`` to ensure docsting completeness and consistency.
* ``flake8-import-order`` to ensure consistent package importing.

Exact linting options are configured in the
``.flake8`` file.
This file also contains comments
to better understand the options.

Invoking only linting with nox can be done
from the terminal by typing:

.. code-block:: console

    $ nox -rs lint

To fix linting issues,
read the output of the linter carefully.
If absolutely required,
use the ``# noqa: err`` comment
after the line in question
to exclude specific linting errors.
Replace the ``err`` part with the error number
that was returned by the linter.
This should only be used where it makes sense.



.. _section_testing:

Testing
~~~~~~~

Project testing is done with ``pytest``.
The following ``pytest`` plugins
are defined in the ``dev-requirements.txt`` file:

* ``pytest-cov`` to test code coverage.
* ``pytest-mock`` to mock out certain parts of the code base.
* ``pytest-sugar`` to display nicely formatted output.

The ``pytest.ini`` file configures
the testing environment properly.
To run tests from the terminal,
assuming that all dependencies are installed,
type:

.. code-block:: console

    $ pytest

To test the test suite only with ``nox``,
you can type the following into the terminal:

.. code-block:: console

    $ nox -rs tests

Again, adding the option ``-p 3.9``
would limit the test to
Python 3.9 only.

**Hypothesis**

Where adequate,
make use of the
`hypothesis <https://hypothesis.readthedocs.io/en/latest/>`_
package for writing your tests.
Have a look at the existing tests
for input on what to test for.
Hypothesis allows for simple edge case testing
and often catches errors
that might otherwise go through.


Docstring example testing
~~~~~~~~~~~~~~~~~~~~~~~~~

As discussed before,
docstrings should be used
to document every new routine.
The docstrings should also contain examples.
Check out the source code for examples
on how to write them.

Examples should of course represent
the behavior of the code.
It thus must be written in Python prompt form.
For example, look at the following example:

.. code-block:: python

    >>> from iniabu import ini  # loads with default ("lodders09")
    >>> ini.database = "nist"  # change database to "nist"
    >>> ini.database
    'nist'

To ensure that all examples are correct,
they can be tested using
`xdoctest <https://github.com/Erotemic/xdoctest>`_.
This is implemented as a ``nox`` session
and can be called
by typing the following into your terminal:

.. code-block:: console

    $ nox -rs xdoctest

*Note*: This is not part of the unit tests
and must be called separately.
A GitHub action is implemented
to specifically run ``doctests``.



Safety
~~~~~~

`Safety <https://github.com/pyupio/safety>`_
is used to check all required dependencies
for known security vulnerabilities.
To run only ``safety`` form ``nox``,
type the following into your terminal:

.. code-block:: console

    $ nox -rs safety


Documentation
~~~~~~~~~~~~~

The documentation uses ``sphinx``.
It is automatically built and hosted by
`readthedocs.io <https://readthedocs.org/>`_.
To locally build the documentation,
run the following from your terminal:

.. code-block:: console

    $ nox -rs docs

This will dump the ``html`` files
for the documentation into the
``docs/_build`` folder.
You can now locally browse them.


.. _section_hooks:

Pre-commit hooks
~~~~~~~~~~~~~~~~

Using pre-commit hooks
your project can be tested
for simple formatting mishaps.
These will also be automatically corrected.
Here,
we use the
`pre-commit framework <https://pre-commit.com>`_.
If you want to set up pre-commit hooks,
go to the folder and run the following command
(after installing pre-commit using pip or pipx):

.. code-block:: console

  $ pre-commit install

This will install the hooks
that are defined in `.pre-commit-config.yaml`
into your git repository.
Note that a fairly standard pre-commit configuration is used.
Black is pinned to a specific version,
i.e., the same version as in the nox file itself.




Structure of the data tables
----------------------------
All data lives in the ``data`` subfolder
underneath the main package.
Aside from the ``nist.py`` file,
all databases contain 2 dictionaries,
one for elements and one for isotopes.

Missing values must be denotes as ``np.nan``.

``ele_dict`` Element dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The element dictionary ``ele_dict``
is shaped in the following structure:

.. code-block:: python

    ele_dict = {
                'Symb':
                    [
                        sol_abu_ele,
                        [a1, ..., an],
                        [rel_abu1, ..., rel_abun],
                        [sol_abu1, ..., sol_abun]
                    ],
                ...
                }

Here, ``Symb`` is the element symbol,
e.g., ``H`` for hydrogen.
This is the dictionary key.
The entry is followed by a list.
The entry ``sol_abu_ele`` is the
solar abundance of the element in number fractions
normalized such that the solar abundance of Si is 1e6.
``a1`` to ``an`` are the atomic mass numbers
of the isotopes of this element.
``rel_abu1`` to ``rel_abun`` and ``sol_abu1`` to ``sol_abun``
are these isotopes relative abundances and solar abundance,
respectively.
Note that the relative abundances
must be normed such that their sum is unity.


``iso_dict`` Isotope dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The isotope dictionary ``iso_dict``
is shaped in the following structure:

.. code-block:: python

    iso_dict = {
                'Symb-A':
                    [
                        rel_abu,
                        sol_abu
                    ],
                ...
               }

Here, `Symb-A` is the key of the dictionary
and is composed of the element symbol ``Symb``
and the isotope's atomic number ``A``.
A dash separates the two entries.
The dictionary entries are ``rel_abu`` and ``sol_abu``,
which are the isotopes relative and
solar abundance, respectively.
The same normalization rules apply as discussed above.

Adding a database
-----------------
Parser files for individual databases
that have already been added
were put into the ``dev`` folder in the repository.
Every database added has their datafile in some format
and a parser living there.
The parser creates automatically the python file.
Have a look at some of these parsers,
especially the write method.
Here, the headers,
imports, etc. are written.
Then the dictionaries are dumped out using ``json.dump()``.
While this results in a really ugly format for the python file,
running ``black`` over the generated file
will properly format everything.

This python file must then be moved to the ``iniabu/data`` folder.
Adjust the ``iniabu/data/__init__.py`` file
to contain imports for the two new dictionaries.
Extend the ``database_selector()`` function
with an additional ``elif`` statement
to contain the new database.

Finally, new tests for this database must be added.
All tests live in the ``test`` folder,
which has the same structure as the ``iniabu`` folder
that contains the package source code.
One good way to write a test is to use an existing test
file for a dataset.
Then adjust the subroutines and associated asserts.
At least make sure that tests exist for:

- Data integrity
- Solar abundance of Si is 10\ :sup:`6`
- Relative abundances of all isotopes sum to unity

Finally, add a new test in ``test_main.py``
to ensure that the database loads correctly.
You should add a consistency check for the new database.
This ensures that code
coverage stays at 100%.
