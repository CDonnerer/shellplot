"""Shellplot plots
"""
import numpy as np

from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.utils import get_index, get_label, numpy_1d, numpy_2d, remove_any_nan

__all__ = ["plot", "hist", "barh", "boxplot"]


# -----------------------------------------------------------------------------
# Exposed functions that directly print the plot
# -----------------------------------------------------------------------------


def plot(*args, **kwargs):
    """Plot x versus y as scatter.

    Parameters
    ----------
    x : array-like
        The horizontal coordinates of the data points.
        Should be 1d np.ndarray or pandas series
    y : array-like
        The vertical coordinates of the data points.
        Should be 1d np.ndarray or pandas series
    color : array, optional
        Color of scatter. Needs to be of same dimension as x, y
        Should be 1-d np.ndarray or pandas series
    figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.

    Returns
    -------
    result
        See Notes.

    """
    plt_str = _plot(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


def hist(*args, **kwargs):
    """Plot a histogram of x

    Parameters
    ----------
    x : array-like
        The array of points to plot a histogram of. Should be 1d np.ndarray or
        pandas series.
    bins : int, optional
        Number of bins in histogram. Default is 10 bins.
    figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.

    Returns
    -------
    result
        See Notes.

    """
    plt_str = _hist(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


def barh(*args, **kwargs):
    """Plot horizontal bars

    Parameters
    ----------
    x : array-like
        The width of the horizontal bars. Should be 1d np.ndarray or pandas
        series.
    labels : array-like
        Array that is used to label the bars. Needs to have the same dim as x.
    figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.

    Returns
    -------
    result
        See Notes.

    """
    plt_str = _barh(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


def boxplot(*args, **kwargs):
    """Plot a boxplot of x

    Note that currently this makes a boxplot using the quantiles:
    [0, 0.25, 0.5, 0.75, 1.0] - i.e. it the whiskers will not exclude outliers

    Parameters
    ----------
    x : array-like
        The horizontal coordinates of the data points.
        Can be 1d or 2d np.ndarray/ pandas series/ dataframe. If 2d, each 1d
        slice will be plotted as a separate boxplot.
    figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.

    Returns
    -------
    result
        See Notes.

    """
    plt_str = _boxplot(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


def return_plt(plt_str, **kwargs):
    if kwargs.get("return_type") == "str":
        return plt_str
    else:
        print(plt_str)


# -----------------------------------------------------------------------------
# Private functions for generating plot strings
# -----------------------------------------------------------------------------


def _init_figure(
    figsize=None, xlim=None, ylim=None, xlabel=None, ylabel=None, **kwargs
):
    """Initialise a new figure.

    TODO:
        - This could be a class to hold a figure state?
        - add ticks
        - add tick labels
    """
    if figsize is None:
        figsize = (70, 25)  # this should go somewhere else

    x_axis = Axis(figsize[0], label=xlabel, limits=xlim)
    y_axis = Axis(figsize[1], label=ylabel, limits=ylim)
    canvas = np.zeros(shape=(figsize[0], figsize[1]), dtype=int)

    return x_axis, y_axis, canvas


def _plot(x, y, color=None, **kwargs):
    """Scatterplot"""

    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": get_label(y)})

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x, y = remove_any_nan(numpy_1d(x), numpy_1d(y))
    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    within_display = np.logical_and(x_scaled.mask == 0, y_scaled.mask == 0)
    x_scaled, y_scaled = x_scaled[within_display], y_scaled[within_display]

    if color is not None:
        color_scaled = numpy_1d(color)[within_display]
        values = np.unique(color_scaled)

        for ii, val in enumerate(values):
            mask = val == color_scaled
            canvas[x_scaled[mask], y_scaled[mask]] = ii + 1

        legend = {ii + 1: val for ii, val in enumerate(values)}
    else:
        canvas[x_scaled, y_scaled] = 1
        legend = None

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


def _hist(x, bins=10, **kwargs):
    """Histogram"""

    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": "counts"})

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x = numpy_1d(x)
    x = x[~np.isnan(x)]
    counts, bin_edges = np.histogram(x, bins)

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

    kwargs.update({"xlabel": get_label(x)})
    if labels is None:
        labels = get_index(x)

    x_axis, y_axis, canvas = _init_figure(**kwargs)

    x_axis.limits = (0, max(x))
    x_scaled = x_axis.fit_transform(x)

    y_axis = y_axis.fit(np.arange(0, len(x) + 1, 1))
    y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is not None:
        y_axis.labels = labels

    bin = 0
    bin_width = y_axis.display_max // len(x) - 1

    for val in x_scaled:
        canvas = _add_hbar(canvas, bin, bin_width, val)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    y_axis.scale = (display_max) / (y_axis.limits[1] - y_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)


def _boxplot(x, labels=None, **kwargs):
    """Box plot"""

    if labels is None:
        labels = get_label(x)
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
        y_axis.labels = numpy_1d(labels)

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
    for jj in range(5):
        canvas[quantiles[jj], limits[0] + 1 : limits[2]] = 20

    canvas[quantiles[0] + 1 : quantiles[1], limits[1]] = 22
    canvas[quantiles[3] + 1 : quantiles[4], limits[1]] = 22

    canvas[quantiles[1] + 1 : quantiles[3], limits[2]] = 22
    canvas[quantiles[1] + 1 : quantiles[3], limits[0]] = 22
    return canvas
