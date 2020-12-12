"""API for pandas plotting backend
"""

import pandas as pd

import shellplot.plots as plt


def plot(data, kind, **kwargs):
    # TODO: check kind

    if isinstance(data, pd.Series):
        return _plot_series(data)
    else:
        return _plot_frame(data, **kwargs)


def _plot_series(data):
    return plt.plot(
        x=data.index.values,
        y=data.values,
        x_title=data.index.name,
        y_title=data.name,
    )


def _plot_frame(data, **kwargs):
    x_col = kwargs.get("x")
    y_col = kwargs.get("y")

    if x_col is None and y_col is None:
        raise ValueError("Please provide both x, y column names")

    s_x = data[x_col]
    s_y = data[y_col]

    return plt.plot(
        x=s_x.values,
        y=s_y.values,
        x_title=s_x.name,
        y_title=s_y.name,
        color=kwargs.get("color", None),
    )


def hist_series(data, **kwargs):
    return plt.hist(x=data.values, x_title=data.name, **kwargs)


def boxplot_series(*args, **kwargs):
    raise NotImplementedError


def boxplot_frame(*args, **kwargs):
    raise NotImplementedError


def boxplot_frame_groupby(grouped, **kwargs):
    raise NotImplementedError


def hist_frame(*args, **kwargs):
    raise NotImplementedError
