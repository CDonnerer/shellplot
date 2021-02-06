"""OO API for shellplot
"""
import numpy as np

from shellplot._config import _global_config as config
from shellplot._plotting import _plot
from shellplot.axis import Axis
from shellplot.drawing import draw


def figure(figsize, **kwargs):
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
        self._init_figure_elements()

    def _init_figure_elements(self):
        self.x = list()
        self.y = list()
        self.plt_kwargs = list()
        self.legend = dict()
        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)

    def plot(self, x, y, **kwargs):
        self.x.append(x)
        self.y.append(y)
        self.plt_kwargs.append(kwargs)

    # def hist(self, x, bins, **kwargs):
    # TODO: How?
    #     self.x.append(x)

    def show(self):
        _plot(self, self.x, self.y, self.plt_kwargs)
        print(self.draw())

    def draw(self):
        return draw(
            canvas=self.canvas,
            y_axis=self.y_axis,
            x_axis=self.x_axis,
            legend=self.legend,
        )

    def clear(self):
        self._init_figure_elements()

    # -------------------------------------------------------------------------
    # Axis setters
    # TODO: this could  be done with getatrr, setattr?
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
        self.y_axis.yticklabels = value

    def set_ylabel(self, value):
        self.y_axis.label = value
