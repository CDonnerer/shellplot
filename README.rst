
.. image:: https://travis-ci.com/CDonnerer/shellplot.svg?branch=master
  :alt: Built Status
  :target: https://travis-ci.com/github/CDonnerer/shellplot?branch=master

.. image:: https://readthedocs.org/projects/shellplot/badge/?version=latest
  :target: https://shellplot.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/CDonnerer/shellplot/badge.svg?branch=master
  :alt: Coveralls
  :target: https://coveralls.io/github/CDonnerer/shellplot?branch=master

.. image:: https://img.shields.io/pypi/v/shellplot.svg
  :alt: PyPI-Server
  :target: https://pypi.org/project/shellplot/

=========
shellplot
=========

    "We should have never left the command line."


Shellplot is the plotting package that you didn't know you needed. Plotting,
straight outta the command line.

Please take a look at the `documentation`_, which contains many `examples`_.


Installation
============

.. code-block:: console

        $ pip install shellplot


Quickstart
===========

Shellplot loosely replicates the `matplotlib`_ API, offering both a figure and
functional `api`_. It currently supports scatter, line, histogram, bar and
boxplots, with many options to customize the figure. It's as easy as:


.. code-block:: python

      >>> import shellplot as plt
      >>> df = plt.load_dataset("penguins")
      >>> plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

.. code-block::

      flipper_length_mm
       232┤                                    o oo  oo    o o        o
          |                                     oo o  o       o
          |                                      oooo
          |                            o oooo ooo oo   o
          |                        oo oooo oo o o o o    o
       217┤                       o o oo ooooo ooo o
          |                   o   o o ooooo o o*oo
          |                     o oo + oooo oooo   *  *
          |                   +   oooo o       o      *       *
          |                   ++              o *  **   **
       202┤        +           +    *             ** **    *
          |      +    ++++   +  +      *    **   ****
          |        ++    +++ +++ +++ +  ** **   ***** **
          |     +++  ++++   ++ ++  +    *+**     * ***
          |   +  + ++++++++++ ++++     *+***  *   *
       187┤+    + + ++ +++++++*+ * *    **           *
          |    ++  ++++++ + +++            *
          |          + ++ +  + + *                                 *
          |  +        ++   +             *                              + Adelie
          |            +     +                                          * Chinstrap
       172┤             +                                               o Gentoo
          └┬----------┬---------┬----------┬----------┬----------┬------
           32         37        42         47         52         57
                                  bill_length_mm


Shellplot also provides a convenient integration with `pandas`_. Simply set the
pandas plotting backend to shellplot:


.. code-block:: python

        >>> import pandas as pd
        >>> pd.set_option("plotting.backend", "shellplot")


Please refer to `pandas visualisation`_ page for further details.

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. _documentation: https://shellplot.readthedocs.io/en/stable/
.. _examples: https://shellplot.readthedocs.io/en/stable/examples/index.html
.. _api: https://shellplot.readthedocs.io/en/stable/api.html
.. _pandas visualisation: https://shellplot.readthedocs.io/en/latest/examples/pandas.html
.. _matplotlib: https://matplotlib.org/contents.html#
.. _pandas: https://pandas.pydata.org/
