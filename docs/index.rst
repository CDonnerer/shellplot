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
         232┤                                         o  o   o o    o o          o
            |                                          ooo o   o        o
            |                                           o ooo
            |                                 o         oooo
            |                            o   oo o oo ooo oooo   o
            |                            o  o  o o o  o  oo  o    o
         217┤                             o     oo  o  oo  o
            |                      o   ooo  oooooooooo   o
            |                                oo o  o   o
            |                      + ooooooo ooooo o oo*   *  *
            |                                o                *         *
            |                      +                 o  *  **   * *
         202┤         +             +    *                ** **     *
            |      +      ++++   ++  ++       *    * *  **** *
            |                  +++    ++++ +  *+         ** *****
            |        +++++ ++ +++++++ + +      * * *   *** * **
            |       + +   +  ++ +  ++++  +    *+***   *
            |+   + ++ ++++ +++++++++          ****        *
         187┤      + + + +  + +++ +*   * *      *            *
            |     ++  + +++++ + +  +              *
            |           +  ++ +   ++   *                                     *
            |              +  +   +   +
            |   +         +    + +              *                                  + Adelie
            |              +                                                       * Chinstrap
         172┤               +                                                      o Gentoo
            └┬--------------┬--------------┬-------------┬--------------┬----------
             32             38             44            50             56
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
