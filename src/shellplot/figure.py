"""Object-oriented API for shellplot
"""
import copy
from itertools import cycle
from typing import Optional, Tuple

import numpy as np

from shellplot._config import _global_config as config
from shellplot._plotting import PlotBuilder, PlotCall, _barh, _boxplot, _hist, _plot
from shellplot.axis import Axis
from shellplot.drawing import LINE_STYLES, MARKER_STYLES, draw
from shellplot.utils import array_like, get_index, numpy_1d, numpy_2d, remove_any_nan


class Figure:
    """Encapsulates a shellplot figure."""

    def __init__(
        self,
        figsize: Optional[Tuple[int]] = None,
        xlim: Optional[array_like] = None,
        xticks: Optional[array_like] = None,
        xticklabels: Optional[array_like] = None,
        xlabel: Optional[str] = None,
        ylim: Optional[array_like] = None,
        yticks: Optional[array_like] = None,
        yticklabels: Optional[array_like] = None,
        ylabel: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> None:
        """Instantiate a new figure

        Parameters
        ----------
        figsize : a tuple (width, height) in ascii characters, optional
            Size of the figure.
        xlim : 2-tuple/list, optional
            Set the x limits.
        xticks : Optional[array_like], optional
            [description], by default None
        xticklabels : Optional[array_like], optional
            [description], by default None
        xlabel : Optional[str], optional
            Name to use for the xlabel on x-axis.
        ylim : 2-tuple/list, optional
            Set the y limits.
        yticks : Optional[array_like], optional
            [description], by default None
        yticklabels : Optional[array_like], optional
            [description], by default None
        ylabel : Optional[str], optional
            Name to use for the ylabel on y-axis.
        title : Optional[str], optional
            The title of the figure.
        """
        self.figsize = figsize or config["figsize"]
        self.x_axis = Axis(
            display_length=self.figsize[0],
            limits=xlim,
            ticks=xticks,
            ticklabels=xticklabels,
            label=xlabel,
        )
        self.y_axis = Axis(
            display_length=self.figsize[1],
            limits=ylim,
            ticks=yticks,
            ticklabels=yticklabels,
            label=ylabel,
        )
        self.title = title
        self.clear()

    def clear(self) -> None:
        """Clear the figure, by removing all attached plots."""
        self._plot_builder = PlotBuilder()
        self.__init_figure_elements()

    def __init_figure_elements(self) -> None:
        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)
        self.legend = list()
        self.markers = cycle(MARKER_STYLES.keys())
        self.lines = cycle(LINE_STYLES.keys())

    def plot(self, x: array_like, y: array_like, color=None, **kwargs) -> None:
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
                self._plot_builder.add(call)

    def hist(self, x: array_like, **kwargs) -> None:
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
        self._plot_builder.add(call)

    def barh(self, x: array_like, **kwargs) -> None:
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
        self._plot_builder.add(call)

    def boxplot(self, x: array_like, **kwargs) -> None:
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
        self._plot_builder.add(call)

    def show(self) -> None:
        """Show the figure by printing to stdout.

        Returns
        -------
        None

        """
        plt_str = self.draw()
        print(plt_str)

    def draw(self) -> str:
        """Draw the figure as a string

        Returns
        -------
        str
            Ascii string of figure

        """
        self.__init_figure_elements()
        self._plot_builder.create(self)

        return draw(
            canvas=self.canvas,
            y_axis=self.y_axis,
            x_axis=self.x_axis,
            legend=self.legend,
            title=self.title,
        )

    # -------------------------------------------------------------------------
    # Axis setters
    # TODO: quite boilerplatey. could  this be done with getatrr, setattr?
    # -------------------------------------------------------------------------

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

    def set_title(self, value):
        self.title = value


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


figure = Figure  # alias for convenience
