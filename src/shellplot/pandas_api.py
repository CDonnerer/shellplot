"""API for pandas plotting backend
"""
import numpy as np
import pandas as pd

import shellplot.plots as plt

__all__ = [
    "plot",
    "hist_series",
    "boxplot_frame",
    "boxplot_frame_groupby",
    "hist_frame",
]

# -----------------------------------------------------------------------------
# Functions exposed to pandas
# -----------------------------------------------------------------------------


def plot(data, kind, **kwargs):
    # TODO: check kind

    if isinstance(data, pd.Series):
        return _plot_series(data, kind)
    else:
        return _plot_frame(data, **kwargs)


def hist_series(data, **kwargs):
    return plt.hist(x=data.values, x_title=data.name, **kwargs)


def boxplot_frame(data, *args, **kwargs):
    column = kwargs.get("column", data.columns)
    by = kwargs.get("by")

    if by is not None:
        df = data.pivot(columns=by, values=column)

        x_title = df.columns.get_level_values(0)[0]
        y_title = by
        labels = df.columns.get_level_values(1)
        kwargs.update({"x_title": x_title, "y_title": y_title, "labels": labels})
    else:
        df = data[column]
        kwargs.update({"labels": df.columns})

    return plt.boxplot(df, **kwargs)


def boxplot_frame_groupby(grouped, **kwargs):
    raise NotImplementedError


def hist_frame(*args, **kwargs):
    raise NotImplementedError


# -----------------------------------------------------------------------------
# Private functions that dispatch to relevant shellplot plots
# -----------------------------------------------------------------------------


def _plot_series(data, kind, *args, **kwargs):

    series_func = {
        "barh": _series_barh,
        "line": _series_line,
        "scatter": _series_line,
        "box": _series_boxplot,
    }

    plot_func = series_func.get(kind)
    if plot_func is None:
        raise NotImplementedError

    return plot_func(data, *args, **kwargs)


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


def _series_boxplot(data, *args, **kwargs):
    return plt.boxplot(data, labels=np.array([data.name]))


def _plot_frame(data, **kwargs):
    x_col = kwargs.get("x")
    y_col = kwargs.get("y")
    color = kwargs.get("color", None)

    if x_col is None or y_col is None:
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
