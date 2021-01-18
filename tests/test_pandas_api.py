"""Testing the pandas backend of shellplot
"""
import pytest

import numpy as np
import pandas as pd


def set_shellplot_plotting_backend():
    pd.set_option("plotting.backend", "shellplot")


@pytest.fixture(autouse=True)
def test_with_shellplot_backend():
    """All tests in this module will use the shellplot backend"""
    set_shellplot_plotting_backend()
    yield


def test_set_shellplot_backend():
    assert pd.get_option("plotting.backend") == "shellplot"


# -----------------------------------------------------------------------------
# Test pandas series plotting
# -----------------------------------------------------------------------------


@pytest.fixture
def random_series():
    x = np.arange(0, 100, 1)
    return pd.Series(index=x, data=np.random.randn(100), name="my_series")


def test_plot_series(random_series):
    random_series.plot()


def test_hist_series(random_series):
    random_series.hist()


def test_barh_series():
    my_series = pd.Series(index=["bar_1", "bar_1", "bar_3"], data=[1, 10, 23])
    my_series.plot.barh()


@pytest.mark.skip
def test_boxplot_series(random_series):
    with pytest.raises(NotImplementedError):
        random_series.boxplot()


# -----------------------------------------------------------------------------
# Test pandas frame plotting
# -----------------------------------------------------------------------------


@pytest.fixture
def random_frame():
    df = pd.DataFrame(np.random.randn(1000, 3), columns=["A", "B", "C"]).cumsum()
    df.index = pd.Series(list(range(len(df))))
    return df


def test_plot_frame_xy(random_frame):
    random_frame.plot(x="A", y="B")


def test_plot_frame_index_cols(random_frame):
    random_frame.plot()


def test_plot_frame(df_penguins):
    df_penguins.dropna().plot("bill_length_mm", "flipper_length_mm")


def test_plot_frame_color(df_penguins):
    df_penguins.dropna().plot("bill_length_mm", "flipper_length_mm", color="species")


def test_plot_frame_missing_arg(df_penguins):
    with pytest.raises(ValueError):
        df_penguins.plot(x="flipper_length_mm")


def test_boxplot_frame(df_penguins):
    df_penguins.boxplot(column=["bill_length_mm", "bill_depth_mm"])


def test_boxplot_frame_by(df_penguins):
    df_penguins.boxplot(column=["bill_length_mm"], by="species")


def test_hist_frame(random_frame):
    with pytest.raises(NotImplementedError):
        random_frame.hist()
