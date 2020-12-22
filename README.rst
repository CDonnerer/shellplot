
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

Run::

        pip install shellplot


Quickstart
===========

Shellplot loosely replicates the `matplotlib`_ API, it's as easy as::

        >>> import shellplot as plt
        >>> df = plt.load_dataset("penguins")
        >>> plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

        flipper_length_mm
         232┤                                         o  o   o o    o o          o
            |                                          ooo o   o        o
            |                                           o ooo
            |                                 o         oooo
            |                            o   oo o oo ooo oooo   o
            |                            o  o  o o o  o  oo  o    o
         217┤                             o o   oo oo  oo  o
            |                      o   ooo  oooooooooo   o
            |                                oo o  o   o
            |                      + ooooooo ooooo o oo*   *  *
            |                                o                *         *
            |                      +                 o  *  **   * *
         202┤         +             +    *                ** **     *
            |      +      ++++   ++  ++       *    * *  **** *
            |                  +++    ++++ +  *+         ** *****
            |     +  +++++ ++ +++++++ + +      * * *   *** * **
            |       + +   +  ++ +  ++++  +    *+***   *
            |+   + ++ ++++ +++++++++  +       ****        *
         187┤      + + + + ++ +++ +*   * *      *            *
            |     ++  + +++++ + +  +              *
            |           +  ++ +   ++   *                                     *
            |              +  +   +   +
            |   +         +    + +              *                                  + Adelie
            |              +                                                       * Chinstrap
         172┤               +                                                      o Gentoo
            └┬--------------┬--------------┬-------------┬--------------┬----------
             32             38             44            50             56
                                        bill_length_mm


Shellplot also provides a convenient integration with `pandas`_. Simply set the
pandas plotting backend to shellplot::


        >>> import pandas as pd
        >>> pd.set_option("plotting.backend", "shellplot")


Please refer to the `documentation`_ for further details.

Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. _documentation: https://shellplot.readthedocs.io/en/latest/
.. _examples: https://shellplot.readthedocs.io/en/latest/examples/index.html
.. _matplotlib: https://matplotlib.org/contents.html#
.. _pandas: https://pandas.pydata.org/
