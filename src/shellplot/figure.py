"""Object-oriented API for shellplot

Can be used like:

fig = plt.figure()
fig.plot(x, y)
fig.show()

"""
import copy
from itertools import cycle

import numpy as np

from shellplot._config import _global_config as config
from shellplot._plotting import PlotCall, Plotter, _barh, _boxplot, _hist, _plot
from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.utils import get_index, numpy_1d, numpy_2d


def figure(figsize=None, **kwargs):
    figsize = figsize or config["figsize"]
    fig = Figure(figsize)

    fig_kwargs = {k: v for k, v in kwargs.items() if k in fig.setters}

    for key, value in fig_kwargs.items():
        getattr(fig, f"set_{key}")(value)
    return fig


class Figure:
    """Encapsulates a shellplot figure"""

    def __init__(self, figsize):
        self.figsize = figsize
        self.x_axis = Axis(self.figsize[0])
        self.y_axis = Axis(self.figsize[1])
        self.clear()

    def clear(self):
        self.plotter = Plotter()
        self._init_figure_elements()

    def _init_figure_elements(self):
        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)
        self.legend = dict()
        self.markers = cycle([1, 2, 3, 4, 5, 6])
        self.lines = cycle([10, 11])

    def plot(self, x, y, color=None, **kwargs):
        x = numpy_2d(x)
        y = numpy_2d(y)

        for x, y, kwargs in array_split(x, y, kwargs):
            for x, y, kwargs in color_split(x, y, color, kwargs):
                call = PlotCall(func=_plot, args=[x, y], kwargs=kwargs)
                self.plotter.add(call)

    def hist(self, x, **kwargs):
        call = PlotCall(func=_hist, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def barh(self, x, **kwargs):
        if kwargs.get("labels") is None:
            kwargs["labels"] = get_index(x)
        call = PlotCall(func=_barh, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def boxplot(self, x, **kwargs):
        call = PlotCall(func=_boxplot, args=[x], kwargs=kwargs)
        self.plotter.add(call)

    def show(self):
        plt_str = self.draw()
        print(plt_str)

    def draw(self):
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

    setters = {
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
        self.x_axis.limits = value

    def set_xticks(self, value):
        self.x_axis.ticks = value

    def set_xticklabels(self, value):
        self.x_axis.ticklabels = value

    def set_xlabel(self, value):
        self.x_axis.label = value

    def set_ylim(self, value):
        self.y_axis.limits = value

    def set_yticks(self, value):
        self.y_axis.ticks = value

    def set_yticklabels(self, value):
        self.y_axis.ticklabels = value

    def set_ylabel(self, value):
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
