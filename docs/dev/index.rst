.. _dev:

Developer Reference
===================

Contents:

.. toctree::
    :maxdepth: 2

Dependencies:
-------------

Structure of the data tables:
-----------------------------
All data lives in the ``data`` subfolder underneath the main package. Aside from the
``nist.py`` file, all databases contain 2 dictionaries, one for elements and one for
isotopes.

Missing values must be denotes as ``np.nan``.

``ele_dict`` Element dictionary:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The element dictionary ``ele_dict`` is shaped in the following structure::

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

Here, ``Symb`` is the element symbol, e.g., ``H`` for hydrogen. This is the dictionary
key. The entry is followed by a list. The entry ``sol_abu_ele`` is the solar abundance
of the element in number fractions normalized such that the solar abundance of Si is
1e6. ``a1`` to ``an`` are the atomic mass numbers of the isotopes of this element.
``rel_abu1`` to ``rel_abun`` and ``sol_abu1`` to ``sol_abun`` are these isotopes
relative abundances and solar abundance, respectively. Note that the relative abundances
must be normed such that their sum is unity.

``iso_dict`` Isotope dictionary:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The isotope dictionary ``iso_dict`` is shaped in teh following structure::

 iso_dict = {
                'Symb-A':
                    [
                        rel_abu,
                        sol_abu
                    ],
                ...
            }

Here, `Symb-A` is the key of the dictionary and is composed of the element symbol
``Symb`` and the isotope's atomic number ``A``. A dash separates the two entries. The
dictionary entries are ``rel_abu`` and ``sol_abu``, which are the isotopes relative and
solar abundance, respectively. The same normalization rules apply as discussed above.

Adding a database:
------------------
Parser files for individual databases that have already been added were put into the
``dev`` folder in the repository. Every database added has their datafile in some
format and a parser living there. The parser creates automatically the python file.
Have a look at some of these parsers, especially the write method. Here, the headers,
imports, etc. are written. Then the dictionaries are dumped out using ``json.dump()``.
While this results in a really ugly format for the python file, running ``black``
over the generated file will properly format everything.

This python file must then be moved to the ``iniabu/data`` folder. Adjust the
``iniabu/data/__init__.py`` file to contain imports for the two new dictionaries.
Extend the ``database_selector()`` function with an additional ``elif`` statement
to contain the new database.

Finally, new tests for this database must be added. All tests live in the ``test``
folder, which has the same structure as the ``iniabu`` folder that contains the
package source code. One good way to write a test is to use an existing test and
simply adjust all asserts. At least make sure that:

- Some data integrety is tested for
- A test exists to check that the solar abundance of Si is 1e6
- A test exists that makes sure that the relative abundances of all isotopes sum to unity.

Finally, extend extend the ``test_init_database()`` function in ``test_main.py``.
You should add a consistency check for the new database. This ensures that code
coverage stays at 100%.