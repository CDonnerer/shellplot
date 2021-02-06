"""Functional API for shellplot

Can be used like so:

plt.plot(x, y)

"""
import copy
from functools import wraps

from shellplot._plotting import _barh, _boxplot, _hist, _plot
from shellplot.figure import figure
from shellplot.utils import get_index, get_label, numpy_2d

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
        See notes, dependent on `return_type`
"""


def add_fig_doc(func):
    """Add figure params to docstring of func"""

    @wraps(func)
    def func_fig_doc(*args, **kwargs):
        return func(*args, **kwargs)

    func_fig_doc.__doc__ = func.__doc__ + __figure_doc
    return func_fig_doc


@add_fig_doc
def plot(x, y, color=None, **kwargs):
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

    x_label, y_label = get_label(x), get_label(y)

    if isinstance(y_label, list):  # multi label goes into legend
        if kwargs.get("label") is None:
            kwargs.update({"label": y_label})
    elif isinstance(y_label, str):  # single label goes into axis labels
        if kwargs.get("ylabel") is None:
            kwargs.update({"ylabel": y_label})
        if kwargs.get("xlabel") is None:
            kwargs.update({"xlabel": x_label})

    fig = figure(**kwargs)
    x = numpy_2d(x)
    y = numpy_2d(y)
    l_kwargs = [copy.deepcopy(kwargs) for i in range(x.shape[0])]

    label = kwargs.get("label")
    if isinstance(label, list):
        # TODO: this can't be quite right. There should be a clean sepration
        # between constant (fig) params and the ones for a given plot
        for plt_kwargs, plt_label in zip(l_kwargs, label):
            plt_kwargs.update({"label": plt_label})

    _plot(fig, x, y, l_kwargs, color=color)
    return return_plt(fig.draw(), **kwargs)


@add_fig_doc
def hist(x, bins=10, **kwargs):
    """Plot a histogram of x

    Parameters
    ----------
    x : array-like
        The array of points to plot a histogram of. Should be 1d np.ndarray or
        pandas series.
    bins : int, optional
        Number of bins in histogram. Default is 10 bins.
    """
    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": "counts"})

    fig = figure(**kwargs)
    _hist(fig, x, bins, **kwargs)
    return return_plt(fig.draw(), **kwargs)


@add_fig_doc
def barh(x, labels=None, **kwargs):
    """Plot horizontal bars

    Parameters
    ----------
    x : array-like
        The width of the horizontal bars. Should be 1d np.ndarray or pandas
        series.
    labels : array-like
        Array that is used to label the bars. Needs to have the same dim as x.
    """
    kwargs.update({"xlabel": get_label(x)})
    if labels is None:
        labels = get_index(x)

    fig = figure(**kwargs)
    _barh(fig, x, labels=labels)
    return return_plt(fig.draw(), **kwargs)


@add_fig_doc
def boxplot(x, labels=None, **kwargs):
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
    if labels is None:
        labels = get_label(x)

    fig = figure(**kwargs)
    _boxplot(fig, x, labels=labels, **kwargs)
    return return_plt(fig.draw(), **kwargs)


def return_plt(plt_str, **kwargs):
    if kwargs.get("return_type") == "str":
        return plt_str
    else:
        print(plt_str)
