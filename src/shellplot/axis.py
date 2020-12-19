"""Module that contains Axis class (usable for both x and y axis)

The main function of an axis is to transform from the data-coordinates to the
coordinates of the plot, hence we loosely follow an sklearn transfomer api.

It can be used like so:

x_axis = Axis(display)
x_axis = x_axis.fit(x)
x_plot = x_axis.transform(x)
"""
import operator

import numpy as np

from shellplot.utils import tolerance_round


class Axis:
    def __init__(self, display_length, title=None, limits=None):
        self.display_length = display_length - 1
        self._title = title
        self._limits = limits

    # -------------------------------------------------------------------------
    # Public properties that can be set by the user
    # -------------------------------------------------------------------------

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits):
        self._limits = limits
        self.fit()  # setting axis limits automatically fits the axis

    @property
    def ticks(self):
        if not hasattr(self, "_ticks"):
            self.ticks = self._get_ticks()
        return self._ticks

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = ticks

    @property
    def labels(self):
        if not hasattr(self, "_labels"):
            self.labels = self.ticks
        return self._labels

    @labels.setter
    def labels(self, labels):
        if len(labels) != len(self.ticks):
            raise ValueError("Len of tick labels must equal len of ticks!")
        self._labels = labels

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def fit(self, x=None):
        """Fit axis to get conversion from data to plot scale"""
        if self.limits is None:
            self.limits = self._auto_limits(x)

        self.scale = float(self.display_length) / (self.limits[1] - self.limits[0])
        return self

    def transform(self, x):
        return np.around(self.scale * (x - self.limits[0])).astype(int)

    def fit_transform(self, x):
        self = self.fit(x)
        return self.transform(x)

    def tick_labels(self):
        """Generate display tick location and labels"""
        within_display = np.logical_and(
            self.ticks >= self.limits[0], self.ticks <= self.limits[1]
        )
        display_labels = self.labels[within_display]
        display_ticks = self.transform(self.ticks[within_display])

        return list(zip(display_ticks, display_labels))  # generator?

    def _get_ticks(self, n=5):
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / n, tol=1e-1
        )
        return np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )

    def _auto_limits(self, x):
        """Automatically find `good` axis limits

        This works by using tolerance_round, which round to the closest
        decimals within a 10 % threshold. If this rounding does not ends up
        higher (lower) than the min of the data, we keep adding small factors
        and try the rounding again until we reach a suitable, round value.
        """

        ax_min = self._rattle_min(min(x))
        ax_max = self._rattle_max(max(x))
        return ax_min, ax_max

    def _rattle_min(self, start_val):
        return self._rattle_val(start_val, op=operator.sub, cond=operator.le)

    def _rattle_max(self, start_val):
        return self._rattle_val(start_val, op=operator.add, cond=operator.ge)

    def _rattle_val(self, start_val, op, cond, rattle_factor=0.025, nround=50):
        for i in range(nround):
            rattle_val, _ = tolerance_round(
                op(start_val, abs(rattle_factor * start_val)), tol=1e-1
            )

            if cond(rattle_val, start_val):
                return rattle_val
            rattle_factor += rattle_factor
        return start_val
