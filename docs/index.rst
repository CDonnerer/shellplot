=========
shellplot
=========

Shellplot produces beautiful ascii plots, thus enabling a rapid data-science
workflow contained in your command line.

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




Contents
========

.. toctree::
   :maxdepth: 2

   Installation <installation>
   Examples <examples/index>
   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _matplotlib: https://matplotlib.org/contents.html#
