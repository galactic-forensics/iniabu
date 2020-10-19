Background information
======================

This section serves
to further explain details of the databases and notations
in a scientific concept.
Here,
background information is given
that can help the user to better understand
the various elements of the package
and the logic behind it.
Usage of the module is not discussed here.

Databases
---------


Notations
---------

δ-values:
~~~~~~~~~

The δ-value of a given isotope ratio,
generally used in cosmo- and geochemistry,
is defined as:

.. math::

  \delta \left( \frac{^{i}X}{^{j}X} \right) =
  \left(\frac{\left(\frac{^{i}X}{^{j}X}\right)_{\mathrm{measured}}}
  {\left(\frac{^{i}X}{^{j}X}\right)_{\mathrm{solar}}} -
  1\right) \times f

Here,
the measured isotope ratio
of element X and isotopes :math:`i` and :math:`j`
represents the ratio as measured in a stardust grain
or as modeled in a stellar model.
The solar isotope ratio for the same isotope ratio
is the one chosen from the database.

Subtracting unity form the ratio of ratios
determines the deviation of the measurement
from the solar abundance.

.. note:: The part of the equation in parenthesis should
  correctly be referred to as the δ-value,
  i.e.,
  the δ-value is defined when setting :math:`f=1`.

This is important to remember.
However,
many measurements,
especially of stardust,
are expressed in parts per thousand or per mil.
This means that the δ-value must be multiplied
by a factor :math:`f=1000`.

On the other hand,
bulk measurements of meteorites generally detect
smaller deviations from solar.
Thus,
such measurements are often expressed
in so-called ε- or µ-values.
These generally only differ from the δ-value
by using a different factor :math:`f`.
The table below gives an overview
of different notations
and the respective :math:`f`-values:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Notation
     - :math:`f`-value
   * - absolute deviation
     - 1
   * - %, percent
     - 100
   * - ‰, per mil
     - 1,000
   * - ε, parts per ten thousand
     - 10,000
   * - µ, parts per one-hundred thousand
     - 100,000
   * - ppm, parts per million
     - 1,000,000
   * - ppb, parts per trillion
     - 1, 000,000,000
   * - ppt, parts per trillion
     - 1,000,000,000,000
