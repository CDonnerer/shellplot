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
        y = np.cos(x)**2

        plt.plot(x, y)

        1.0┤                                  +
           |+                               ++ ++                               +
           | +                             +     +                             +
           |  +                           ++     ++                           +
           |  +                          +         +                          +
        0.8┤   +                         +         +                         +
           |    +                       +           +                       +
           |    +                       +           +                       +
           |     +                     +             +                     +
           |     +                     +             +                     +
        0.6┤      +                   +               +                   +
           |      +                                                       +
           |                         +                 +
           |       +                 +                 +                 +
           |        +               +                   +               +
        0.4┤        +               +                   +               +
           |         +             +                     +             +
           |         +                                                 +
           |          +           +                      +            +
           |          +           +                       +           +
        0.2┤           +         +                         +         +
           |            +       ++                         ++       +
           |            +       +                           +       +
           |             +    ++                             ++    +
        0.0┤              +++++                               +++++
           ├------------┬-------------┬-------------┬-------------┬-------------┬
           -3.0         -1.8          -0.6          0.6           1.8           3.0


Shellplot replicates the matplotlib API, except where it doesn't.


Pandas backend
--------------

For your pleasure, you can use shellplot via pandas::

        import pandas as pd
        pd.set_option('plotting.backend', 'shellplot')

        df["my_feature"].hist(bins=10)




Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
