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

        import shellplot as plt

        plt.plot(x=x, y=y)


Shellplot replicates the matplotlib API, except where it doesn't.

Via pandas. For your pleasure, you can use shellplot via pandas::

        import pandas as pd
        pd.set_option('plotting.backend', 'shellplot')

        df["my_feature"].hist(bins=10)




Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
