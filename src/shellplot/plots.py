"""Shellplot plots
"""
import numpy as np

from shellplot.utils import remove_any_nan, tolerance_round

DISPLAY_X = 70
DISPLAY_Y = 25


def plot(x, y, **kwargs):
    plt_str = _plot(x=x, y=y, **kwargs)
    print(plt_str)


def _plot(x, y, x_title=None, y_title=None, color=None):
    x, y = remove_any_nan(x, y)

    x_axis = Axis(DISPLAY_X, title=x_title)
    y_axis = Axis(DISPLAY_Y, title=y_title)

    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y))

    if color is not None:
        for ii, val in enumerate(np.unique(color.values)):
            mask = val == color
            canvas[x_scaled[mask], y_scaled[mask]] = ii + 1
    else:
        canvas[x_scaled, y_scaled] = 1

    plt_str = draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)
    return plt_str


def hist(x, bins=10, x_title=None, **kwargs):
    plt_str = _hist(x=x, bins=bins, x_title=x_title, **kwargs)
    print(plt_str)


def _hist(x, bins=10, x_title=None, **kwargs):
    counts, bin_edges = np.histogram(x, bins)

    y_axis = Axis(DISPLAY_Y, title="counts")
    x_axis = Axis(DISPLAY_X, title=x_title)

    counts_scaled = y_axis.fit_transform(counts)
    x_axis = x_axis.fit(bin_edges)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y))

    bin = 0
    bin_width = int((DISPLAY_X - 1) / len(counts)) - 1

    for count in counts_scaled:
        canvas[bin, :count] = 3
        canvas[bin + 1 : bin + 1 + bin_width, count] = 2
        canvas[bin + 1 + bin_width, :count] = 3
        bin += bin_width + 1

    # this bit doesn't seem entirely right
    display_max = (bin_width + 1) * len(counts)
    x_axis.scale = (display_max + bin_width) / (x_axis.limits[1] - x_axis.limits[0])

    plt_str = draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)
    return plt_str


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

    def ticks(self, n=5):
        """TODO. this functions is a mess"""
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / n, tol=1e-1
        )

        labels = np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )
        ticks = self.transform(labels)

        if ticks[-1] > self.display_length:
            ticks = ticks[:-1]
            labels = labels[:-1]

        return list(zip(ticks, labels))

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


def draw(canvas, x_axis, y_axis):
    plt_lines = _draw_plot(canvas)

    label_len = max([len(str(val)) for (t, val) in y_axis.ticks()])
    l_pad = label_len + 1

    y_lines = _draw_y_axis(canvas, y_axis, l_pad)
    x_lines = _draw_x_axis(canvas, x_axis, l_pad)

    return _join_plot_lines(plt_lines, y_lines, x_lines)


def _join_plot_lines(plt_lines, y_lines, x_lines):
    plt_str = "\n"

    empty_pad = len(plt_lines) - len(y_lines)
    plt_lines = ["\n"] * empty_pad + plt_lines

    for ax, plt in zip(y_lines, plt_lines):
        plt_str += ax + plt
    for ax in x_lines:
        plt_str += ax
    return plt_str


def _draw_plot(canvas):
    palette = {0: " ", 1: "+", 2: "x", 3: "o", 4: ".", 5: "_", 6: "|"}

    plt_lines = list()

    for i in reversed(range(canvas.shape[1])):
        plt_str = ""
        for j in range(canvas.shape[0]):
            plt_str += palette[canvas[j, i]]
        plt_str += "\n"
        plt_lines.append(plt_str)

    return plt_lines


def _draw_y_axis(canvas, y_axis, l_pad):
    y_lines = list()

    y_ticks = y_axis.ticks()

    for i in reversed(range(canvas.shape[1])):
        ax_line = ""
        if len(y_ticks) > 0 and i == y_ticks[-1][0]:
            ax_line += f"{str(y_ticks[-1][1]).rjust(l_pad)}┤"
            y_ticks.pop(-1)
        else:
            ax_line += " " * l_pad + "|"
        y_lines.append(ax_line)

    if y_axis.title is not None:
        y_lines.insert(0, y_axis.title)
    return y_lines


def _draw_x_axis(canvas, x_axis, l_pad):
    x_ticks = x_axis.ticks()

    upper_ax = " " * l_pad
    lower_ax = " " * l_pad
    marker = "├"

    for j in range(canvas.shape[0]):
        if len(x_ticks) > 0 and j == x_ticks[0][0]:
            lower_ax = lower_ax[: len(upper_ax)]
            label = str(round(x_ticks[0][1], 2))
            lower_ax += label + " " * 20

            upper_ax += marker
            marker = "┬"
            x_ticks.pop(0)
        else:
            upper_ax += "-"

    ax_lines = [upper_ax + "\n", lower_ax + "\n"]

    if x_axis.title is not None:
        title_pad = int(canvas.shape[0] / 2 - len(x_axis.title) / 2)
        title_str = " " * (l_pad + title_pad) + x_axis.title
        ax_lines.append(title_str)

    return ax_lines
