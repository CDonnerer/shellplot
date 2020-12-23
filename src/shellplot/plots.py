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


def _init_figure(
    figsize=(70, 25),
    xlim=None,
    ylim=None,
    xticks=None,
    yticks=None,
    xlabel=None,
    ylabel=None,
):
    """Initialise a new figure.

    TODO:
        - This could be a class to hold a figure state?
    """

    x_axis = Axis(figsize[0], label=xlabel, limits=xlim)
    y_axis = Axis(figsize[1], label=ylabel, limits=ylim)
    canvas = np.zeros(shape=(figsize[0], figsize[1]), dtype=int)

    return x_axis, y_axis, canvas


def _plot(x, y, color=None, **kwargs):
    """Scatterplot"""

    def get_name(x):
        if isinstance(x, pd.Series):
            return x.name
        else:
            return None

    if kwargs.get("xlabel") is None:
        xlabel = get_name(x)
        kwargs.update({"xlabel": xlabel})
    if kwargs.get("ylabel") is None:
        ylabel = get_name(y)
        kwargs.update({"ylabel": ylabel})

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x, y = remove_any_nan(x, y)
    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    within_display = np.logical_and(x_scaled.mask == 0, y_scaled.mask == 0)
    x_scaled, y_scaled = x_scaled[within_display], y_scaled[within_display]

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


def _hist(x, bins=10, **kwargs):
    """Histogram"""
    x = x[~np.isnan(x)]

    counts, bin_edges = np.histogram(x, bins)

    kwargs.update({"ylabel": "counts"})

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    y_axis.limits = (0, max(counts))
    counts_scaled = y_axis.transform(counts)
    x_axis = x_axis.fit(bin_edges)

    bin = 0
    bin_width = x_axis.display_max // len(counts) - 1

    for count in counts_scaled:
        canvas = _add_vbar(canvas, bin, bin_width, count)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(counts)
    x_axis.scale = display_max / (x_axis.limits[1] - x_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


def _barh(x, labels=None, **kwargs):
    """Horizontal bar plot"""

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x_axis.limits = (0, max(x))
    x_scaled = x_axis.fit_transform(x)

    y_axis = y_axis.fit(np.arange(0, len(x) + 1, 1))
    y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is not None:
        y_axis.labels = labels

    bin = 0
    bin_width = int((DISPLAY_Y - 1) / len(x)) - 1

    for val in x_scaled:
        canvas = _add_hbar(canvas, bin, bin_width, val)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    y_axis.scale = (display_max) / (y_axis.limits[1] - y_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


def _boxplot(x, labels=None, **kwargs):
    """Box plot"""

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x = numpy_2d(x)
    x = np.ma.masked_where(np.isnan(x), x)

    quantiles = np.array(
        [np.quantile(dist[dist.mask == 0], q=[0, 0.25, 0.5, 0.75, 1.0]) for dist in x]
    )

    quantiles_scaled = x_axis.fit_transform(quantiles)

    y_axis = y_axis.fit(np.array([0, len(x)]))
    y_lims = y_axis.transform(
        np.array([0.2, 0.50, 0.8]) + np.arange(0, len(x), 1)[np.newaxis].T
    )
    y_axis.ticks = np.arange(0.5, len(x), 1)
    if labels is not None:
        y_axis.labels = labels

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
