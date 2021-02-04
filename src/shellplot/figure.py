"""OO API for shellplot

fig = plt.figure(figsize=(80, 40))

fig.plot(x, y, marker=True, line=False)

figure holds x, y, kwargs

fig.plot(x, x**2, line=True, marker=False)

fig.set_xlim((0, 10))

fig.show()

"""
import numpy as np

from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.plots import _new_plot


def figure(figsize=(60, 25)):
    return Figure(figsize)


class Figure:
    """Encapsulates a shellplot figure"""

    def __init__(self, figsize):
        self.figsize = figsize
        self.x_axis = Axis(self.figsize[0])
        self.y_axis = Axis(self.figsize[1])
        self.x = list()
        self.y = list()
        self.plt_kwargs = list()
        self.legend = dict()

    def plot(self, x, y, **kwargs):
        self.x.append(x)
        self.y.append(y)
        self.plt_kwargs.append(kwargs)

    def show(self):

        self.canvas = np.zeros(shape=(self.figsize[0], self.figsize[1]), dtype=int)

        _new_plot(self.x, self.y, self.plt_kwargs, fig=self)
        print(self.draw())

    def draw(self):
        return draw(
            canvas=self.canvas,
            y_axis=self.y_axis,
            x_axis=self.x_axis,
            legend=self.legend,
        )

    # -------------------------------------------------------------------------
    # Axis setters
    # -------------------------------------------------------------------------

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
