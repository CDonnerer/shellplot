"""API for pandas plotting backend
"""

import pandas as pd

import shellplot.plots as plt


def plot(data, kind, **kwargs):
    # TODO: check kind

    if isinstance(data, pd.Series):
        return _plot_series(data, kind)
    else:
        return _plot_frame(data, **kwargs)


def _plot_series(data, kind, **kwargs):

    series_func = {"barh": _series_barh, "line": _series_line, "scatter": _series_line}

    plot_func = series_func.get(kind)
    if plot_func is None:
        raise NotImplementedError

    return plot_func(data, **kwargs)


def _series_barh(data, **kwargs):
    return plt.barh(
        x=data.values, labels=data.index, x_title=data.name, y_title=data.index.name
    )


def _series_line(data, **kwargs):
    return plt.plot(
        x=data.index.values,
        y=data.values,
        x_title=data.index.name,
        y_title=data.name,
    )


def _plot_frame(data, **kwargs):
    x_col = kwargs.get("x")
    y_col = kwargs.get("y")
    color = kwargs.get("color", None)

    if x_col is None and y_col is None:
        raise ValueError("Please provide both x, y column names")

    if color in data.columns:
        color = data[color]

    s_x = data[x_col]
    s_y = data[y_col]

    return plt.plot(
        x=s_x.values,
        y=s_y.values,
        x_title=s_x.name,
        y_title=s_y.name,
        color=color,
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
