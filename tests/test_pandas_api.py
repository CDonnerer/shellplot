"""Testing the pandas backend of shellplot
"""
import pytest

import numpy as np
import pandas as pd
import pytest


def set_shellplot_plotting_backend():
    pd.set_option("plotting.backend", "shellplot")


def test_set_shellplot_backend():
    set_shellplot_plotting_backend()


# Test series backend


@pytest.fixture
def random_series():
    x = np.arange(0, 100, 1)
    return pd.Series(index=x, data=np.random.randn(100), name="my_series")


def test_plot_series(random_series):
    set_shellplot_plotting_backend()
    random_series.plot()


def test_hist_series(random_series):
    set_shellplot_plotting_backend()
    random_series.hist()


def test_barh_series():
    set_shellplot_plotting_backend()
    my_series = pd.Series(index=["bar_1", "bar_1", "bar_3"], data=[1, 10, 23])
    my_series.plot.barh()


@pytest.mark.skip
def test_boxplot_series(random_series):
    with pytest.raises(NotImplementedError):
        random_series.boxplot()


# Test frame backend


@pytest.fixture
def random_frame():
    x = np.arange(0, 100, 1)
    y = np.random.randn(100)
    return pd.DataFrame({"x": x, "y": y})


def test_plot_frame(random_frame):
    set_shellplot_plotting_backend()
    random_frame.plot(x="x", y="y")


def test_boxplot_frame(random_frame):
    with pytest.raises(NotImplementedError):
        random_frame.boxplot()


def test_hist_frame(random_frame):
    with pytest.raises(NotImplementedError):
        random_frame.hist()
