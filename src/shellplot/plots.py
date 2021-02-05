"""Shellplot plots
"""
from functools import wraps

import numpy as np

from shellplot._config import _global_config as config
from shellplot.axis import Axis
from shellplot.drawing import LINES, MARKERS, draw
from shellplot.utils import get_index, get_label, numpy_1d, numpy_2d

__all__ = ["plot", "hist", "barh", "boxplot"]


# -----------------------------------------------------------------------------
# Exposed functions that directly print the plot
# -----------------------------------------------------------------------------

__figure_doc = """figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    label : str/ list of str, optional
        Labels that make the figure legend
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.


    Returns
    -------
    result
        See Notes.
"""


def add_fig_doc(func):
    """Add figure params to docstring of func"""

    @wraps(func)
    def func_fig_doc(*args, **kwargs):
        return func(*args, **kwargs)

    func_fig_doc.__doc__ = func.__doc__ + __figure_doc
    return func_fig_doc


@add_fig_doc
def plot(*args, **kwargs):
    """Plot x versus y as scatter.

    Parameters
    ----------
    x : array-like
        The horizontal coordinates of the data points.
        Should be 1d or 2d np.ndarray or pandas series
    y : array-like
        The vertical coordinates of the data points.
        Should be 1d or 2d np.ndarray or pandas series
    color : array, optional
        Color of scatter. Needs to be of same dimension as x, y
        Should be 1-d np.ndarray or pandas series
    line : bool, optional, default False
        Whether a line should be plotted using the x, y points. This will use a
        linear interpolation of the points.
    """
    plt_str = _plot(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


@add_fig_doc
def hist(*args, **kwargs):
    """Plot a histogram of x

    Parameters
    ----------
    x : array-like
        The array of points to plot a histogram of. Should be 1d np.ndarray or
        pandas series.
    bins : int, optional
        Number of bins in histogram. Default is 10 bins.
    """
    plt_str = _hist(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


@add_fig_doc
def barh(*args, **kwargs):
    """Plot horizontal bars

    Parameters
    ----------
    x : array-like
        The width of the horizontal bars. Should be 1d np.ndarray or pandas
        series.
    labels : array-like
        Array that is used to label the bars. Needs to have the same dim as x.
    """
    plt_str = _barh(*args, **kwargs)
    return return_plt(plt_str, **kwargs)


@add_fig_doc
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
    figsize=None, xlim=None, ylim=None, xlabel=None, ylabel=None, label=None, **kwargs
):
    """Initialise a new figure.

    TODO:
        - This could be a class to hold a figure state?
        - add ticks
        - add tick labels
    """
    if figsize is None:
        figsize = config["figsize"]

    x_axis = Axis(figsize[0])
    x_axis.label = xlabel
    x_axis.limits = xlim
    y_axis = Axis(figsize[1])
    y_axis.label = ylabel
    y_axis.limits = ylim
    canvas = np.zeros(shape=(figsize[0], figsize[1]), dtype=int)

    if label is not None:
        legend = {ii + 1: val for ii, val in enumerate(label)}
    else:
        legend = None

    return x_axis, y_axis, canvas, legend


def _plot(x, y, color=None, line=False, **kwargs):
    """Scatterplot"""

    x_label, y_label = get_label(x), get_label(y)

    if isinstance(y_label, list):  # multi label goes into legend
        if kwargs.get("label") is None:
            kwargs.update({"label": y_label})
    elif isinstance(y_label, str):  # single label goes into axis labels
        if kwargs.get("ylabel") is None:
            kwargs.update({"ylabel": y_label})
        if kwargs.get("xlabel") is None:
            kwargs.update({"xlabel": x_label})

    x_axis, y_axis, canvas, legend = _init_figure(**kwargs)

    x = numpy_2d(x)
    y = numpy_2d(y)

    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    outside_display = np.logical_or(x_scaled.mask, y_scaled.mask)
    x_scaled.mask = outside_display
    y_scaled.mask = outside_display

    if color is not None:
        color_scaled = numpy_1d(color)[~outside_display].squeeze()
        values = np.unique(color_scaled)

        for ii, val in enumerate(values):
            mask = val == color_scaled
            idx = x_scaled[:, mask].compressed()
            idy = y_scaled[:, mask].compressed()
            canvas = _add_xy(canvas=canvas, idx=idx, idy=idy, marker=ii + 1, line=line)

        legend = {ii + 1: val for ii, val in enumerate(values)}
    else:
        for ii in range(y_scaled.shape[0]):
            idx = x_scaled[ii, :].compressed()
            idy = y_scaled[ii, :].compressed()
            canvas = _add_xy(canvas=canvas, idx=idx, idy=idy, marker=ii + 1, line=line)

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


def _new_plot(x, y, l_kwargs, fig=None):
    """Scatterplot"""

    fig.x_axis.fit(np.concatenate([x for x in x]))
    fig.y_axis.fit(np.concatenate([y for y in y]))

    for x, y, plt_kwargs in zip(x, y, l_kwargs):
        _single_plot(
            fig=fig,
            x=x,
            y=y,
            marker=plt_kwargs.get("marker", next(MARKERS)),
            line=plt_kwargs.get("line", next(LINES)),
            label=plt_kwargs.get("label"),
        )


def _single_plot(fig, x, y, marker=None, line=None, label=None):
    x_scaled = fig.x_axis.transform(numpy_1d(x))
    y_scaled = fig.y_axis.transform(numpy_1d(y))

    idx, idy = within_display(x_scaled, y_scaled)

    _add_xy(
        canvas=fig.canvas,
        idx=idx,
        idy=idy,
        marker=marker,
        line=line,
    )

    if label is not None:
        key = marker or line
        fig.legend.update({key: label})


def within_display(x, y):
    outside_display = np.logical_or(x.mask, y.mask)
    x.mask = outside_display
    y.mask = outside_display

    idx = x.compressed()
    idy = y.compressed()
    return idx, idy


def _hist(x, bins=10, **kwargs):
    """Histogram"""

    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": "counts"})

    x_axis, y_axis, canvas, legend = _init_figure(**kwargs)
    _check_bins(bins, x_axis)

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

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


def _check_bins(bins, x_axis):
    if isinstance(bins, int):
        bin_len = bins
    elif isinstance(bins, np.ndarray) or isinstance(bins, list):
        bin_len = len(bins)
    else:
        raise ValueError("Please provider either integer or array of bins!")
    if bin_len > x_axis.display_max:
        raise ValueError("Number of bins needs to be less than figsize along x!")


def _barh(x, labels=None, **kwargs):
    """Horizontal bar plot"""

    kwargs.update({"xlabel": get_label(x)})
    if labels is None:
        labels = get_index(x)

    x_axis, y_axis, canvas, legend = _init_figure(**kwargs)

    x_axis.limits = (0, x.max())
    x_scaled = x_axis.fit_transform(x)

    y_axis = y_axis.fit(np.arange(0, len(x) + 1, 1))
    y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is not None:
        y_axis.labels = labels

    bin = 0
    bin_width = y_axis.display_max // len(x) - 1

    for val in x_scaled.data:
        canvas = _add_hbar(canvas, bin, bin_width, val)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    y_axis.scale = (display_max) / (y_axis.limits[1] - y_axis.limits[0])

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


def _boxplot(x, labels=None, **kwargs):
    """Box plot"""

    if labels is None:
        labels = get_label(x)
    x_axis, y_axis, canvas, legend = _init_figure(**kwargs)

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

    return draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)


# -----------------------------------------------------------------------------
# Function to add canvas elements
# -----------------------------------------------------------------------------


def _add_xy(canvas, idx, idy, marker=None, line=None):
    """Add x, y series to canvas, as marker and/ or line"""
    if line is not None:
        x_line, y_line = _line_interp(idx, idy)
        canvas[x_line, y_line] = line
    if marker is not None:
        canvas[idx, idy] = marker
    return canvas


def _line_interp(x, y, round_tol=0.4):
    """Interpolate for line plotting"""
    x_interp = np.arange(x.min(), x.max(), 1)
    y_interp = np.interp(x_interp, x, y)

    # Point selection is turned off for now
    # is_discrete = np.isclose(
    #     y_interp,
    #     np.around(y_interp).astype(int),
    #     atol=round_tol,
    # )
    is_discrete = True

    x_line = x_interp[is_discrete].astype(int)
    y_line = np.around(y_interp[is_discrete]).astype(int)

    return x_line, y_line


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
