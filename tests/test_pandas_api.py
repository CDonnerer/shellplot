"""Testing the pandas backend of shellplot
"""
import numpy as np
import pandas as pd


def test_set_shellplot_backend():
    pd.set_option("plotting.backend", "shellplot")


def test_plot():
    pd.set_option("plotting.backend", "shellplot")
    x = np.arange(-3, 3, 0.1)
    df = pd.DataFrame({"x": x, "y": np.cos(x) ** 2 + x / 5})
    df.plot(x="x", y="y")