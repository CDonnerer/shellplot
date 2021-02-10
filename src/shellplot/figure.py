"""Object-oriented API for shellplot
"""
import copy
from itertools import cycle

import numpy as np

from shellplot._config import _global_config as config
from shellplot._plotting import PlotCall, Plotter, _barh, _boxplot, _hist, _plot
from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.utils import get_index, numpy_1d, numpy_2d, remove_any_nan


def figure(figsize=None, **kwargs):
    """Create a new shellplot figure

    Parameters
    ----------
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

    Returns
    -------
    `shellplot.figure.Figure`
        Instantiated shellplot figure

    """
    figsize = figsize or config["figsize"]
    fig = Figure(figsize)

    fig_kwargs = {k: v for k, v in kwargs.items() if k in fig._setters}

    for key, value in fig_kwargs.items():
        getattr(fig, f"set_{key}")(value)
    return fig


class Figure:
    """Encapsulates a shellplot figure. Should be instantiated via `shellplot.figure`"""

    def __init__(self, figsize):
        """Instantiate a new figure

        Parameters
        ----------
        figsize : a tuple (width, height) in ascii characters, optional
            Size of the figure.
        """
        self.figsize = figsize
        self.x_axis = Axis(self.figsize[0])
        self.y_axis = Axis(self.figsize[1])
        self.clear()

    def clear(self):
        """Clear the figure, by removing all attached plots."""
        self.plotter = Plotter()
        self._init_figure_elements()

    def _init_figure_elements(self):
        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)
        self.legend = dict()
        self.markers = cycle([1, 2, 3, 4, 5, 6])
        self.lines = cycle([10, 11])

    def plot(self, x, y, color=None, **kwargs):
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
        label : str
            The label of the plot for display in the legend
        """
        x = numpy_2d(x)
        y = numpy_2d(y)

        for x, y, kwargs in array_split(x, y, kwargs):
            for x, y, kwargs in color_split(x, y, color, kwargs):
                x, y = remove_any_nan(x, y)
                call = PlotCall(func=_plot, args=[x, y], kwargs=kwargs)
                self.plotter.add(call)

    def hist(self, x, **kwargs):
        """Plot a histogram of x

        Parameters
        ----------
        x : array-like
            The array of points to plot a histogram of. Should be 1d np.ndarray or
            pandas series.
        bins : int, optional
            Number of bins in histogram. Default is 10 bins.
        label : str
            The label of the plot for display in the legend
        """
        call = PlotCall(func=_hist, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def barh(self, x, **kwargs):
        """Plot horizontal bars

        Parameters
        ----------
        x : array-like
            The width of the horizontal bars. Should be 1d np.ndarray or pandas
            series.
        labels : array-like
            Array that is used to label the bars. Needs to have the same dim as x.
        """
        if kwargs.get("labels") is None:
            kwargs["labels"] = get_index(x)
        call = PlotCall(func=_barh, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def boxplot(self, x, **kwargs):
        """Plot a boxplot of x

        Note that currently this makes a boxplot using the quantiles:
        [0, 0.25, 0.5, 0.75, 1.0] - i.e. it the whiskers will not exclude outliers

        Parameters
        ----------
        x : array-like
            The horizontal coordinates of the data points.
            Can be 1d or 2d np.ndarray/ pandas series/ dataframe. If 2d, each 1d
            slice will be plotted as a separate boxplot.
        labels : array-like
            Array that is used to label the boxplots.
        """

        call = PlotCall(func=_boxplot, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def show(self):
        """Show the figure by printing to stdout.

        Returns
        -------
        None

        """
        plt_str = self.draw()
        print(plt_str)

    def draw(self):
        """Draw the figure as a string

        Returns
        -------
        str
            Ascii string of figure

        """
        self._init_figure_elements()
        self.plotter.fill_figure(self)
        return draw(
            canvas=self.canvas,
            y_axis=self.y_axis,
            x_axis=self.x_axis,
            legend=self.legend,
        )

    # -------------------------------------------------------------------------
    # Axis setters
    # TODO: quite boilerplatey. could  this be done with getatrr, setattr?
    # -------------------------------------------------------------------------

    _setters = {
        "xlim",
        "xticks",
        "xticklabels",
        "xlabel",
        "ylim",
        "yticks",
        "yticklabels",
        "ylabel",
    }

    def set_xlim(self, value):
        """Set limits of x-axis"""
        self.x_axis.limits = value

    def set_xticks(self, value):
        """Set x-axis ticks"""
        self.x_axis.ticks = value

    def set_xticklabels(self, value):
        """Set x-axis tick labels."""
        self.x_axis.ticklabels = value

    def set_xlabel(self, value):
        """Set the label of the x-axis"""
        self.x_axis.label = value

    def set_ylim(self, value):
        """Set limits of y-axis"""
        self.y_axis.limits = value

    def set_yticks(self, value):
        """Set y-axis ticks"""
        self.y_axis.ticks = value

    def set_yticklabels(self, value):
        """Set y-axis tick labels."""
        self.y_axis.ticklabels = value

    def set_ylabel(self, value):
        """Set y-axis tick labels."""
        self.y_axis.label = value


def color_split(x, y, color, kwargs):
    """If a color array is provided, we split on it"""
    if color is None:
        yield x, y, kwargs
    else:
        color = numpy_1d(color).squeeze()
        values = np.unique(color)

        for value in values:
            mask = value == color
            val_kwargs = copy.deepcopy(kwargs)
            val_kwargs.update({"label": value})
            yield x[mask], y[mask], val_kwargs


def array_split(x, y, kwargs):
    """If x, y contain multiple lines, we split"""
    if x.shape[0] == 1:
        yield x.squeeze(), y.squeeze(), kwargs
    else:
        label = kwargs.get("label", [])
        if kwargs.get("label") is not None:
            kwargs.pop("label")

        for x, y in zip(x, y):
            val_kwargs = copy.deepcopy(kwargs)
            if len(label) != 0:
                val_kwargs.update({"label": label.pop(0)})
            yield x, y, val_kwargs
