import numpy as np

from shellplot.utils import tolerance_round


class Axis:
    def __init__(self, display_length, title=None, limits=None):
        self.display_length = display_length - 1
        self._title = title
        self._limits = limits

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
        self._labels = labels

    def fit(self, x):
        """Fit axis to get conversion from data to plot scale"""
        if self.limits is None:
            self.limits = self._determine_limits(x)

        self.scale = float(self.display_length) / (self.limits[1] - self.limits[0])
        return self

    def transform(self, x):
        return (self.scale * (x - self.limits[0])).astype(int)

    def fit_transform(self, x):
        self = self.fit(x)
        return self.transform(x)

    def tick_labels(self):
        display_labels = self.labels
        display_ticks = self.transform(self.ticks)

        if display_ticks[-1] > self.display_length:
            display_ticks = display_ticks[:-1]
            display_labels = display_labels[:-1]

        return list(zip(display_ticks, display_labels))

    def _get_ticks(self, n=5):
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / n, tol=1e-1
        )
        return np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )

    def _determine_limits(self, x):
        plot_min = min(x)
        plot_max = max(x)
        rattle_factor = 0.03

        ax_min, _ = tolerance_round(
            plot_min - rattle_factor * np.sign(plot_min) * plot_min, tol=1e-1
        )
        ax_max, _ = tolerance_round(
            plot_max + rattle_factor * np.sign(plot_max) * plot_max, tol=1e-1
        )
        return ax_min, ax_max
