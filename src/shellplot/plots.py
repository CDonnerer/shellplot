"""Shellplot plots
"""
import numpy as np
import pandas as pd

from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.utils import numpy_2d, remove_any_nan

__all__ = ["plot", "hist", "barh", "boxplot"]

DISPLAY_X = 70
DISPLAY_Y = 25


# -----------------------------------------------------------------------------
# Exposed functions that directly print the plot
# -----------------------------------------------------------------------------


def plot(*args, **kwargs):
    plt_str = _plot(*args, **kwargs)
    print(plt_str)


def hist(*args, **kwargs):
    plt_str = _hist(*args, **kwargs)
    print(plt_str)


def barh(*args, **kwargs):
    plt_str = _barh(*args, **kwargs)
    print(plt_str)


def boxplot(*args, **kwargs):
    plt_str = _boxplot(*args, **kwargs)
    print(plt_str)


# -----------------------------------------------------------------------------
# Private functions for generating plot strings
# -----------------------------------------------------------------------------


def _plot(x, y, color=None, x_title=None, y_title=None):
    """Scatterplot"""
    x, y = remove_any_nan(x, y)

    def get_name(x):
        if isinstance(x, pd.Series):
            return x.name
        else:
            return None

    if x_title is None:
        x_title = get_name(x)
    if y_title is None:
        y_title = get_name(y)

    x_axis = Axis(DISPLAY_X, title=x_title)
    y_axis = Axis(DISPLAY_Y, title=y_title)

    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y), dtype=int)

    if color is not None:
        values = np.unique(color)

        for ii, val in enumerate(values):
            mask = val == color
            canvas[x_scaled[mask], y_scaled[mask]] = ii + 1

        legend = {ii + 1: val for ii, val in enumerate(values)}
    else:
        canvas[x_scaled, y_scaled] = 1
        legend = None

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


def _hist(x, bins=10, x_title=None, **kwargs):
    """Histogram"""
    x = x[~np.isnan(x)]

    counts, bin_edges = np.histogram(x, bins)

    y_axis = Axis(DISPLAY_Y, title="counts")
    x_axis = Axis(DISPLAY_X, title=x_title)

    y_axis.limits = (0, max(counts))
    counts_scaled = y_axis.transform(counts)
    x_axis = x_axis.fit(bin_edges)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y), dtype=int)

    bin = 0
    bin_width = int((DISPLAY_X - 1) / len(counts)) - 1

    for count in counts_scaled:
        canvas = _add_vbar(canvas, bin, bin_width, count)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(counts)
    x_axis.scale = display_max / (x_axis.limits[1] - x_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


def _barh(x, labels=None, x_title=None, y_title=None):
    """Horizontal bar plot"""
    y_axis = Axis(DISPLAY_Y, title=y_title)
    x_axis = Axis(DISPLAY_X, title=x_title)

    x_axis.limits = (0, max(x))
    x_scaled = x_axis.fit_transform(x)

    y_axis = y_axis.fit(np.arange(0, len(x) + 1, 1))
    y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is not None:
        y_axis.labels = labels

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y), dtype=int)

    bin = 0
    bin_width = int((DISPLAY_Y - 1) / len(x)) - 1

    for val in x_scaled:
        canvas = _add_hbar(canvas, bin, bin_width, val)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    y_axis.scale = (display_max) / (y_axis.limits[1] - y_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


def _boxplot(x, labels=None, x_title=None, y_title=None, **kwargs):
    """Box plot"""
    x = numpy_2d(x)
    x = np.ma.masked_where(np.isnan(x), x)

    quantiles = np.array(
        [np.quantile(dist[dist.mask == 0], q=[0, 0.25, 0.5, 0.75, 1.0]) for dist in x]
    )

    x_axis = Axis(DISPLAY_X, x_title)
    y_axis = Axis(DISPLAY_Y, y_title)

    quantiles_scaled = x_axis.fit_transform(quantiles)

    y_axis = y_axis.fit(np.array([0, len(x)]))
    y_lims = y_axis.transform(
        np.array([0.2, 0.50, 0.8]) + np.arange(0, len(x), 1)[np.newaxis].T
    )
    y_axis.ticks = np.arange(0.5, len(x), 1)
    if labels is not None:
        y_axis.labels = labels

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y), dtype=int)

    for ii in range(len(x)):
        quants = quantiles_scaled[ii, :]
        lims = y_lims[ii, :]
        canvas = _add_box_and_whiskers(canvas, quants, lims)

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


# -----------------------------------------------------------------------------
# Canvas elements
# -----------------------------------------------------------------------------


def _add_vbar(canvas, start, width, height):
    """Add a vertical bar to the canvas"""
    canvas[start, :height] = 20
    canvas[start + 1 : start + 1 + width, height] = 22
    canvas[start + 1 + width, :height] = 20
    return canvas


def _add_hbar(canvas, start, width, height):
    """Add a horizontal bar to the canvas"""
    canvas[:height, start] = 22
    canvas[height, start + 1 : start + 1 + width] = 20
    canvas[:height, start + 1 + width] = 22
    return canvas


def _add_box_and_whiskers(canvas, quantiles, limits):
    """Add a box and whiskers to the canvas"""
    for jj in [0, 1, 2, 3, 4]:
        canvas[quantiles[jj], limits[0] + 1 : limits[2]] = 20

    canvas[quantiles[0] + 1 : quantiles[1], limits[1]] = 22
    canvas[quantiles[3] + 1 : quantiles[4], limits[1]] = 22

    canvas[quantiles[1] + 1 : quantiles[3], limits[2]] = 22
    canvas[quantiles[1] + 1 : quantiles[3], limits[0]] = 22
    return canvas
