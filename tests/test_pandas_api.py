"""Testing the pandas backend of shellplot
"""
import numpy as np
import pandas as pd


def test_set_shellplot_backed():
    pd.set_option('plotting.backend', 'shellplot')


def test_plot():

    import pdb; pdb.set_trace()

    x = np.arange(-3, 3, 0.1)
    df = pd.DataFrame({"x": x, "y": np.cos(x) ** 2 + x/5 })
    df.plot(x="x", y="y")
