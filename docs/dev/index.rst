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

We are trying to make it as easy as possible
to contribute to this project.
The project itself is set up using
`rye <https://rye.astral.sh>`_.
This makes everything very smooth.

Development workflow
--------------------

Fork the repository and clone it to your computer.
If you have rye installed, simply run:

.. code-block:: console

  rye sync

and all dependencies will be installed and you are ready to go.
We use rye to manage format and lint.
To format and lint, run:

.. code-block:: console

  rye fmt
  rye lint

We also strive for 100% test coverage.
So if you fix a bug, please write a test first that fails,
then fix the bug,
then make sure all tests still pass, including the new one.
To run the tests, use:

.. code-block:: console

  rye test

If you add a new feature,
please also add a test for it.
In addition,
please add a docstring to the new feature that includes an example.
This will automatically be included in the documentation.
To test all the docstrings,
run:

.. code-block:: console

  rye run test_doc


Pre-commit hooks
~~~~~~~~~~~~~~~~

Personally, I like the
`pre-commit framework <https://pre-commit.com>`_
a lot as it helps me commit clean code upon every commit.

If you want to set up pre-commit hooks,
go to the folder and run the following command
(after installing pre-commit using pip or pipx):

.. code-block:: console

  $ pre-commit install

This will install the hooks
that are defined in `.pre-commit-config.yaml`
into your git repository.


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
