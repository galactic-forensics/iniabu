Installation and Usage
======================


Dependencies
------------

This package is tested
with python versions 3.6 - 3.9.
It might work on older python version as well,
however,
compatibility is not guaranteed.

The only dependency at the moment
for running the ``iniabu`` package
is ``numpy``.
There is currently no pinned ``numpy`` version
and the latest one should be working great.


Installation
------------

.. warning:: Currently,
    this package can only be installed from its GitHub repository.
    Installation directly from PyPi
    will result in the old version (v0.3.1) being installed.

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
The default database is called "lodders09"
and is based on
`Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_.
Further databases,
listed by the string used to call them,
are as following:

- "asplund09": `Asplund et al. (2009) <https://doi.org/10.1146/annurev.astro.46.060407.145222>`_
- "lodders09" (default): `Lodders et al. (2009) <https://doi.org/10.1007/978-3-540-88055-4_34>`_
- "nist": `NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_

The solar abundances of all databases
were converted to number abundances
and are relative to Si = 10\ :sup:`6`.
Conversion to other units,
as described below,
is possible.

*Note*: Not all databases mentioned here
contain the solar abundances for every isotope.
If an operation you are trying to perform
encounters a solar abundance value that is not availagle
in the currently loaded database,
the result will be returned as an ``np.nan``,
i.e., as not a number.


Usage
-----

Here we give a short overview of the ``iniabu`` module.
Please also have a look at the
:doc:`API Reference <api/index>`.
There,
each module is described in detail,
often with examples on how to use the specific function.


Importing the module
~~~~~~~~~~~~~~~~~~~~

Once installed,
you can simply import the package
from your python session as:

.. code-block:: python

    >>> from iniabu import ini

This is the recommended import
and will be used throughout
the rest of this documentation,
unless otherwise noted.
Here, the :code:`ini` instance will be loaded
with the default database
(currently Lodders et al., 2009)
and using linear,
number abundances.
Alternatively you can directly import
the database using number, logarithmic abundances
or mass fractions.
The respective imports for these are:

.. code-block:: python

  >>> from iniabu import inilog  # number logarithmic abundances
  >>> from iniabu import inimf  # mass fraction


In case multiple databases
are required at the same time,
e.g., :code:`db1` using Lodders et al. (2009)
and :code:`db2` using Asplund et al. (2009) values and number logarithmic units,
the following import could be used:

.. code-block:: python

    >>> import iniabu
    >>> db1 = iniabu.IniAbu(database="lodders09")
    >>> db2 = iniabu.IniAbu(database="asplund09", unit="num_log")


Loading a database
~~~~~~~~~~~~~~~~~~

Switching the data base from a given instance :code:`ini`
can be easily accomplished.
For example, the "asplund09" database
can easily be loaded into a given instance
by calling:

.. code-block:: python

    >>> ini.database = "asplund09"

.. note:: Switching a database does not reset the units.
  For example: If "lodders09" is loaded
  using mass fractions and you load
  "asplund09" as the new database,
  the units will stay the same that are used by default.
  A message will be printed to reflect this.

  .. code-block:: python

    >>> ini.database = 'asplund09'
    iniabu loaded database: 'asplund09', current units: 'mass_fraction'



Available abundance units
~~~~~~~~~~~~~~~~~~~~~~~~~

Abundance units can easily be switched between
linear number abundances,
logarithmic number abundances,
and mass fraction units.

In the linear number abundances case
all abundances are linear with respect to each other
and are normalized
such that the abundance of silicon
is equal to 10\ :sup:`6` by number.


The logarithmic number abundances
are generally used in astronomy.
For an element X,
the logarithmic abundance is defined
with respect to the abundance of hydrogen as:

.. math::

  \log_{10}(\epsilon_X) = \log_{10} \left(\frac{\mathrm{N}_\mathrm{X}}{\mathrm{N}_\mathrm{H}}\right) + 12

Mass fraction values
are common in nucleosynthesis calculations.
To return mass fraction values
the database can be switched to `mass_fraction`.
The abundances are then defined as following:

.. math::

  X_{i} = \frac{N_{i} m_{i}}{\rho N_{A}} \\

Here :math:`X_{i}` is the mass fraction
of element :math:`i`,
:math:`N_{i}` its number abundance,
:math:`m_{i}` its molecular mass,
and :math:`N_{N}` Avogadro's constant.
The density :math:`\rho`
is defined as:

.. math::

  \rho = \frac{1}{N_{A}} \sum_i N_{i} m_{i}

To switch a given database between
linear number abundance ("num_lin"),
logarithmic number abundance ("num_log") mode,
and mass fraction mode ("mass_fraction")
the following property can be set:

.. code-block:: python

    >>> ini.unit == "num_log"

In this case,
we would switch to logarithmic number abundance mode.
To check what abundance unit is currently set,
the following command can be used:

.. code-block:: python

    >>> ini.unit
    "num_log"

By default,
linear number abundance values are used.

.. note:: To use "num_log" or
  "mass_fraction" mode by default
  you can import the module in the following ways:

  .. code-block:: python

    from iniabu import inilog  # "num_log" units
    from iniabu import inimf  # "mass_fraction" units

.. note:: If you use "mass_fraction" units,
  the relative abundances of the isotopes
  are also given in mass fractions!

Element and isotope properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Properties of an element are independent from the loaded database
and are taken from the
`NIST database <https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses>`_.
To query the loaded database for relative or solar abundances,
see the next two sections.

Querying an element:
~~~~~~~~~~~~~~~~~~~~

To query an element's properties
with respect to the solar abundance,
it can be loaded into a temporary variable.
For example:
To query silicon the element and its properties
can be loaded into a variable as following:

.. code-block:: python

    >>> ele = ini.element["Si"]

The following properties can now be queried
from the element:

- The mass of the element,
  calculated using the isotope masses
  and the currently loaded abundances,
  using ``mass``.
- The solar abundance of the element itself using ``solar_abundance``,
  normed as discussed above
- The mass number of its (stable) isotopes using ``isotopes_a``
- The relative abundances of its (stable) isotopes using
  ``isotopes_relative_abundance``.
  If you are using "mass_fractions" as units,
  the relative abundances will also be given
  as mass fractions!
- The solar abundances of its (stable) isotopes using ``isotopes_solar_abundance``

For example,
to query the solar abundance of iron
one could run the following statement:

.. code-block:: python

   >>> ele = ini.element["Fe"]
   >>> ele.solar_abundance
   847990.0



Querying an isotope
~~~~~~~~~~~~~~~~~~~

To query an isotope's properties
with respect to teh solar abundance,
it can be loaded into a temporary variable,
similar to when loading an element.
For example:
To query :sup:`54`\Fe,
the isotope can be loaded as a variable
as following:

.. code-block:: python

    >>> iso = ini.isotope["Fe-54"]

The following properties can then
be queried from this isotope:

- The mass of a specific isotope using ``mass``.
- The solar abundance of the isotope itself using ``solar_abundance``,
  normed as discussed above
- The relative abundance of the specific isotope
  with respect to the element using ``relative_abundance``.
  *Note*: All isotopes of an element
  would sum up to a relative abundance of 1.
  If you are using "mass_fractions" as units,
  the relative abundances will also be given
  as mass fractions!

For example:
To query the solar and the relative abundances
of :sup:`54`\Fe
one could run the following two commands in python:

.. code-block:: python

  >>> iso = ini.isotope["Fe-54"]
  >>> iso.solar_abundance
  49600.0
  >>> iso.relative_abundance
  0.058449999999999995


Element and isotope ratios
~~~~~~~~~~~~~~~~~~~~~~~~~~

This function is used to calculate element and isotope ratios.
Sure, the same can be accomplished by simply
dividing the abundances of two isotopes.
However, this function
has some added benefits:

- Select if ratio is number fraction (default) or mass fraction
- Return multiple elements or isotopes at once

Some additional benefits when calculating isotope ratios:

- Choosing an element as the nominator
  selects all isotopes of the given element
  for the nominator
- Choosing an element as the denominator
  calculates the ratio for every isotope in the nominator
  with respect to the most abundant isotope
  of the element given as the denominator.
  This might sound complicated,
  but can be very useful since isotope ratios
  are often given with the most abundant isotope
  in the denominator

.. note:: If multiple isotope ratios are returned
  the function automatically returns them
  as a numpy array.
  This facilitates subsequent mathematical operations
  using these ratios.

The functions to calculate these ratios are called
``ratio_element`` and ``ratio_isotope``.
Below are some examples
that describe some standard usage of these routines:

.. caution:: In these examples we assume
  that the database is loaded with "num_lin" units.
  If you are using "mass_fraction" units,
  you will get "mass_fraction" units back,
  even if you do not set :code:`mass_fraction=True`.
  However,
  you could overwrite this behavior
  (the same way you can return `mass_fractions`
  even if you are in "num_lin" mode)
  by setting :code:`mass_fraction=False`.

Some examples for elemental ratios:

- Calculate He to Pb ratio
  using number fraction and mass fraction:
  Here we assume that number, linear units are loaded:

  .. code-block:: python

    >>> ini.ratio_element("He", "Pb")  # number fraction
    759537205.0816697
    >>> ini.ratio_element("He", "Pb", mass_fraction=True)
    39321659726.58637

- Calculate multiple element ratios
  with the same denominator.
  The specific example here ratios Fe and Ni to Si:

  .. code-block:: python

    >>> ini.ratio_element(["Fe", "Ni"], "Si")
    array([0.84824447, 0.04910773])

- Calculate multiple element ratios
  that have individual nominators and denominators.
  Here Si to Fe and Ni to Zr is calculated:

  .. code-block:: python

    >>> ini.ratio_element(["Si", "Ni"], ["Fe", "Zr"])
    array([1.17890541e+00, 4.55450413e+03])


Some examples for isotope ratios:

- Calculate the isotope ratios
  of :sup:`6`\Li to :sup:`7`\Li
  as number fractions
  and as mass fractions.
  Here we assume that number, linear units are loaded:

  .. code-block:: python

    >>> ini.ratio_isotope("Li-6", "Li-7")  # number fractions by default
    0.08212225817272835
    >>> ini.ratio_isotope("Li-6", "Li-7", mass_fraction=True)
    0.09578691181324486

- Calculate isotope fractions of :sup:`3`\He to :sup:`4`\He
  and :sup:`21`\Ne to :sup:`20`\Ne:

  .. code-block:: python

    >>> ini.ratio_isotope(["He-3", "Ne-21"], ["He-4", "Ne-20"])
    array([0.00016603, 0.00239717])

- Calculate the isotope ratios of all Si isotopes
  with respect to :sup:`28`\Si.
  Three methods, all identical, are specified as following:

  - Method 1: The manual way specifying each isotope individually
  - Method 2: Select element in nominator chooses all isotopes of specified element
  - Method 3: The fastest way for this specific case is to choose `'Si'` as the element
    in the nominator and to choose `'Si'` in the denominator.
    The latter will pick the most abundant isotope of silicon,
    which is :sup:`28`\Si.


  .. code-block:: python

    >>> ini.ratio_isotope(["Si-28", "Si-29", "Si-30"], "Si-28")  # Method 1
    array([1.        , 0.05077524, 0.03347067])
    >>> ini.ratio_isotope("Si", "Si-28")  # Method 2
    array([1.        , 0.05077524, 0.03347067])
    >>> ini.ratio_isotope("Si", "Si")  # Method 3
    array([1.        , 0.05077524, 0.03347067])



δ-values
~~~~~~~~

.. note:: A detailed discussion
  of δ-values can be found in the
  :doc:`Background Information <background>`

The δ-value of a given isotope ratio,
generally used in cosmo- and geochemistry,
is defined as:

.. math::

  \delta \left( \frac{^{i}X}{^{j}X} \right) =
  \left(\frac{\left(\frac{^{i}X}{^{j}X}\right)_{\mathrm{measured}}}
  {\left(\frac{^{i}X}{^{j}X}\right)_{\mathrm{solar}}} -
  1\right) \times f

Here the isotopes chosen for the ratio are :math:`^{i}X` and :math:`^{j}X`.
The measured isotope ratio,
which is in the nominator,
is a value that must be provided to the function.
The solar isotope ratio (denominator)
will be taken from the solar abundance table
using the isotope ratios provided to the routine.
The factor :math:`f` is by default set to 1000.
This means that δ-values are by default
returned as parts-per-thousand (‰).
Choosing a different factor can be done
by setting the keyword argument ``delta_factor`` accordingly.

Furthermore, the keyword argument ``mass_fraction``
can also be used as for ratios.
Setting this keyword to ``True``
or ``False`` allows the user
to overwrite the behavior of the loaded units.

While δ-values are commonly calculated for isotopes of one individual element,
the routine allows to calculate δ-values between isotopes of different elements.
To calculate a δ-values of two elements,
the ``delta_element`` function should be used.
The equation given above represents a specific,
but most commonly used case.

Finally: The ``delta_isotope``
and ``delta_element`` functions
have the same features
for specifying the nominator and denominator
as the ``ratio_isotope``
and ``ratio_element`` functions mentioned above.

.. caution:: The values must be given in the same shape
  as the number of ratios provided.
  Otherwise the routine will return a ``ValueError``
  specifying that there was a length mismatch.

Some examples for calculating δ-values for isotopes:

- Calculate one δ-value with a given measurement value.
  Here for :sup:`29`\Si/:sup:`28`\Si.
  First calculated in parts per thousand (default),
  then as percent.

  .. code-block:: python

    >>> ini.delta_isotope("Si-30", "Si-28", 0.04)  # parts per thousand (default)
    195.0761256883704
    >>> ini.delta_isotope("Si-30", "Si-28", 0.04, delta_factor=100)  # percent
    19.50761256883704

- Calculate multiple δ-values as mass fractions.
  Here we calculate all Si isotopes with respect to :sup:`28`\Si.
  Measurements are defined first.
  Three versions are provided that yield the same result.
  See description on calculating isotope ratios above
  for more detail.

  .. code-block:: python

    >>> msr = [1., 0.01, 0.04]  # measurement
    >>> ini.delta_isotope(["Si-28", "Si-29", "Si-30"], "Si-28", msr)
    array([   0.        , -803.05359812,  195.07612569])
    >>> ini.delta_isotope("Si", "Si-28", msr)
    array([   0.        , -803.05359812,  195.07612569])
    >>> ini.delta_isotope("Si", "Si", msr)
    array([   0.        , -803.05359812,  195.07612569])

- Calculate the δ-value for :sup:`84`\Sr
  with respect to the major Sr isotope (:sup:`86`\Sr).
  The measurement value is provided as a mass fraction
  (assumption),
  but the database is loaded using number, linear units:

  .. code-block:: python

    >>> ini.delta_isotope("Sr-84", "Sr", 0.01, mass_fraction=True)
    414.3962670607242


Some examples for calculating δ-values for elements:

- Calculate a δ-value for multiple elements,
  here Si and Ne with respect to Fe:

  .. code-block:: python

    >>>  ini.delta_element(["Si", "Ne"], "Fe", [2, 4])
    array([696.48894668,  30.26124356])


Bracket-notation
~~~~~~~~~~~~~~~~

The bracket notation,
generally used in astronomy,
for a given elemental ratio
is defined as:

.. math::

  [\mathrm{X}/\mathrm{Y}] =
  \log_{10} \left( \frac{N_\mathrm{X}}{N_\mathrm{Y}} \right)_\mathrm{star} -
  \log_{10} \left( \frac{N_\mathrm{X}}{N_\mathrm{Y}} \right)_\mathrm{solar}

Here,
star stands for an arbitrary measurement,
e.g.,
of a given star.
X and Y are the elements of interest in this case,
:math:`N_\mathrm{X}` and :math:`N_\mathrm{Y}`
represent the respective number abundances of elements X and Y.
Calculations with mass fractions
are also allowed by the routine.

While bracket notation is commonly used with elements,
there is no mathematical reason to prohibit using it for isotopes.
Therefore,
two routines are provided,
namely ``bracket_element`` and ``bracket_isotope``.

Finally: The ``bracket_element``
and ``bracket_isotope`` functions
have the same features
for specifying the nominator and denominator
as the ``ratio_isotope``
and ``ratio_element`` functions mentioned above.


Some examples for calculating bracket notation values for elements:

- Calculate bracket notation value
  for Fe / H for a given measurement.
  First we calculate it as a number fraction (default setting)
  then as a mass fraction while having the database loaded
  in number linear mode.

  .. code-block:: python

    >>> ini.bracket_element("Fe", "H", 0.005)  # number fraction
    2.183887471873783
    >>> ini.bracket_element("Fe", "H", 0.005, mass_fraction=True)  # mass fraction
    3.9274378849968263

- Calculate bracket notation value
  for multiple measurements.
  Here, for O and Fe with respect to Fe.

  .. code-block:: python

    >>> ini.bracket_element(["O", "Fe"], "H", [0.02, 0.005])
    array([1.51740521, 2.18388747])



Some examples for calculating bracket notation values for isotopes:

- Calculate a bracket notation values for multiple isotopes.
  Here for all Si isotopes with respect to :sup:`28`\Si.
  *Note*: See ``ratio_isotopes`` for a detailed description
  of the possibilities.

  .. code-block:: python

    >>> msr = [1., 0.01, 0.04]
    >>>  ini.bracket_isotope(["Si-28", "Si-29", "Si-30"], "Si-28", msr)
    array([ 0.        , -0.70565195,  0.07739557])
    >>> ini.bracket_isotope("Si", "Si-28", msr)
    array([ 0.        , -0.70565195,  0.07739557])
    >>> ini.bracket_isotope("Si", "Si", msr)
    array([ 0.        , -0.70565195,  0.07739557])
