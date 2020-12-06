
.. image:: https://api.cirrus-ci.com/github/CDonnerer/shellplot.svg?branch=initial-concept
  :alt: Built Status
  :target: https://cirrus-ci.com/github/CDonnerer/shellplot?branch=initial-concept
.. image:: https://coveralls.io/repos/github/CDonnerer/shellplot/badge.svg?branch=master
  :alt: Coveralls
  :target: https://coveralls.io/github/CDonnerer/shellplot?branch=master


=========
shellplot
=========

    "We should have never left the command line." - Unknown, 2020


Shellplot is the plotting package that you didn't know you needed. Plotting,
straight outta the command line.


Installation
============

Run::

        pip install shellplot


Usage
======

Simply pretend you're using matplotlib's pyplot::

        import numpy as np
        import shellplot as plt

        x = np.arange(-3, 3, 0.05)
        y = np.cos(x) ** 2

        plt.plot(x, y)

        1.0┤                             +
           |+                          +++++                          +
           | +                        +     +                        +
           |  +                      +       +                      +
       0.75┤   +                    +         +                    +
           |    +                  ++         ++                  +
           |    +                  +           +                  +
           |     +                +             +                +
        0.5┤      +              +               +              +
           |      +              +               +              +
           |       +            +                 +            +
           |        +          +                   +          +
       0.25┤        ++        ++                   ++        ++
           |         ++       +                     +       ++
           |          ++    ++                       ++    ++
        0.0┤           ++++++                         ++++++
           ├------------------┬-------------------┬-------------------┬
           -3                 -1                  1                   3



Shellplot replicates the matplotlib API, except where it doesn't.


Pandas backend
--------------

For your pleasure, you can use shellplot via pandas::

        import pandas as pd
        pd.set_option("plotting.backend", "shellplot")

        x = np.random.randn(1000)
        pd.Series(data=x, name="my_fun_distribution").hist(bins=10)

        counts
         286┤
            |                          ____
            |                     ____|    |
            |                    |    |    |
         215┤                    |    |    |____
            |                    |    |    |    |
            |                    |    |    |    |
            |                    |    |    |    |
         144┤                ____|    |    |    |
            |               |    |    |    |    |____
            |               |    |    |    |    |    |
            |               |    |    |    |    |    |
          73┤               |    |    |    |    |    |
            |           ____|    |    |    |    |    |____
            | ____ ____|    |    |    |    |    |    |    |____
            ├-------------┬-------------┬--------------┬-------------┬--
            -4.0          -2.0          0.0            2.0           4.0
                                my_fun_distribution



Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
