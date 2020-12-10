"""Testing the pandas backend of shellplot
"""
import numpy as np
import pandas as pd


def set_shellplot_plotting_backend():
    pd.set_option("plotting.backend", "shellplot")


def test_set_shellplot_backend():
    set_shellplot_plotting_backend()


def test_plot_series():
    set_shellplot_plotting_backend()
    x = np.arange(0, 100, 1)
    s = pd.Series(index=x, data=np.random.randn(100), name="my_series")

    s.plot()
