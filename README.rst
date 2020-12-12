
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

As shellplot replicates the `matplotlib`_ API, it's as easy as::


        >>> import shellplot as plt
        >>> df = plt.load_dataset("penguins")
        >>> plt.plot(df["bill_length_mm"], df["flipper_length_mm"], color=df["species"])

          flipper_length_mm
              |
           237┤
              |
              |                                        o  o   oo    o o         o
              |                                         ooo o  o        o
              |                                          ooooo
           223┤                                o oooo ooo  oo   o
              |                            o o ooo oo  oo oo o    o
              |                           oo  oo ooooo  oo o
              |                      o   o o  ooooo o  oo o
           209┤                        oo oo + oooo o oo*   *  *
              |                      +   o oo  o       o       *        *
              |                       +                o *  **   **
              |          +          + +++  *             * *** *    *
              |        +     ++++    + +++++   * +  * *   ** * **
           195┤          +++  + +++ +++++++  +  ** * *  * * * *
              |       + ++  +++ +++++++++  +   ** **   * *  **
              |  +  +  ++++++ ++++++ ++ +       ****      *
              |      + ++++++ ++ ++ +*   * *     * *          *
              |       +    + ++    + ++
           181┤            + +++++  +   +*                                   *
              |    +         +    + +            *
              |               +                                                      + Adelie
              |               +                                                      * Chinstrap
           167┤                                                                      o Gentoo
              ├------------┬-------------┬-------------┬-------------┬-------------┬
              31           37            43            49            55            61
                                          bill_length_mm



Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.


.. _documentation: https://shellplot.readthedocs.io/en/latest/
.. _examples:  https://shellplot.readthedocs.io/en/latest/examples.html
.. _matplotlib: https://matplotlib.org/contents.html#
