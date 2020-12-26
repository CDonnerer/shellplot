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
    if isinstance(data, pd.Series):
        return _plot_series(data, kind, **kwargs)
    elif isinstance(data, pd.DataFrame):
        return _plot_frame(data, kind, **kwargs)
    else:
        # we should never get here
        raise ValueError


def hist_series(data, **kwargs):
    return plt.hist(x=data, **kwargs)


def boxplot_frame(data, *args, **kwargs):
    """TODO
    - can this logic go into `plt.boxplot`?
    """
    column = kwargs.pop("column", data.columns)
    by = kwargs.pop("by")

    if by is not None:
        df = data.pivot(columns=by, values=column)

        xlabel = df.columns.get_level_values(0)[0]
        labels = df.columns.get_level_values(1)
        kwargs.update({"xlabel": xlabel, "ylabel": by, "labels": labels})
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
    """Dispatch on kind to the relevant series plot function"""
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


def _plot_frame(data, kind, *args, **kwargs):
    """Dispatch on kind to the relevant frame plot function"""
    frame_func = {
        "line": _frame_line,
        "scatter": _frame_line,
    }

    plot_func = frame_func.get(kind)
    if plot_func is None:
        raise NotImplementedError

    return plot_func(data, *args, **kwargs)


def _series_barh(data, **kwargs):
    x_col = kwargs.pop("x")

    if x_col is not None:
        data = data[x_col]

    return plt.barh(x=data, **kwargs)


def _series_line(data, **kwargs):
    x_col = kwargs.pop("x")
    y_col = kwargs.pop("y")

    # why do we get both x and y here?
    if x_col is not None:
        data = data[x_col]
    if y_col is not None:
        data = data[y_col]

    return plt.plot(x=data.index, y=data, **kwargs)


def _series_boxplot(data, *args, **kwargs):
    return plt.boxplot(data, labels=np.array([data.name]), **kwargs)


def _frame_line(data, **kwargs):
    x_col = kwargs.pop("x")
    y_col = kwargs.pop("y")
    color = kwargs.pop("color", None)

    if x_col is None or y_col is None:
        raise ValueError("Please provide both x, y column names")

    if color in data.columns:
        color = data[color]

    s_x = data[x_col]
    s_y = data[y_col]

    return plt.plot(x=s_x, y=s_y, color=color, **kwargs)
