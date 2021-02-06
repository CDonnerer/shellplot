"""Object-oriented API for shellplot

Can be used like:

fig = plt.figure()
fig.plot(x, y)
fig.show()

"""
from itertools import cycle

import numpy as np

from shellplot._config import _global_config as config
from shellplot._plotting import _plot
from shellplot.axis import Axis
from shellplot.drawing import draw


def figure(figsize=None, **kwargs):
    figsize = figsize or config["figsize"]
    fig = Figure(figsize)

    fig_kwargs = {k: v for k, v in kwargs.items() if k in fig.setters}

    for key, value in fig_kwargs.items():
        getattr(fig, f"set_{key}")(value)

    return fig


# @dataclass
# class FuncCall:
#     """Class for keeping track of function calls."""
#
#     func: callable
#     args: List
#     kwargs: Dict
#
#     def __call__(self, fig):
#         self.func(fig, *self.args, **self.kwargs)


class PlotCall:
    def __init__(self):
        self.l_x = list()
        self.l_y = list()
        self.l_kwargs = list()

    def add(self, x, y, kwargs):
        self.l_x.append(x)
        self.l_y.append(y)
        self.l_kwargs.append(kwargs)

    def __call__(self, fig):
        _plot(fig, self.l_x, self.l_y, self.l_kwargs)


class Figure:
    """Encapsulates a shellplot figure"""

    def __init__(self, figsize):
        self.figsize = figsize
        self.x_axis = Axis(self.figsize[0])
        self.y_axis = Axis(self.figsize[1])
        self.plot_call = PlotCall()
        self._init_figure_elements()

    def _init_figure_elements(self):
        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)
        self.legend = dict()
        self.markers = cycle([1, 2, 3, 4, 5, 6])
        self.lines = cycle([10, 11])

    def plot(self, x, y, **kwargs):
        self.plot_call.add(x=x, y=y, kwargs=kwargs)

    # def hist(self, x, bins, **kwargs):
    # TODO: How?
    #     self.x.append(x)

    def show(self):
        self._init_figure_elements()
        self.plot_call(self)
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
        self.plot_call = PlotCall()

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
        self.y_axis.ticklabels = value

    def set_ylabel(self, value):
        self.y_axis.label = value
