"""Drawing module.

Functions for taking the elements of the plot (e.g. canvas, axis, legend) and
converts them to strings. Please note that drawing is entirely agnostic to the
type of plot.

How it works:

1. Plot elements passed into here (ideally in container)

2. Each plot element has a lazy 'plot lines' generator:
    - `_draw_canvas`
    - `_draw_y_axis`
    - `_draw_x_axis`
    - `_draw_legend`
    - `_draw_title`

3. Elements are called in steps

    i/
    ->  [title line]

    ii/
    ->  [y axis label]

    iii/
    -> [y axis] [canvas] [legend]
    -> [y axis] [canvas] [legend]
    -> [y axis] [canvas] [legend]
    -> [y axis] [canvas] [legend]
    -> ...

    iv/
    -> [x axis]
    -> [x axis]
    -> [x axis label]


"""
import dataclasses
import itertools
from collections import namedtuple
from typing import List

import numpy as np

from shellplot.axis import Axis

MARKER_STYLES = {1: "+", 2: "*", 3: "o", 4: "x", 5: "@", 6: "■"}

LINE_STYLES = {10: "·", 11: ":", 12: "÷", 13: "×"}

PALETTE = {
    0: " ",
    20: "|",
    21: "_",
    22: "-",
    23: "┐",
}
PALETTE.update(MARKER_STYLES)
PALETTE.update(LINE_STYLES)

LegendItem = namedtuple("LegendItem", ["symbol", "name"])

# TODO: drawing should just receive a container (dataclass) of stuff


@dataclasses.dataclass
class PlotElements:
    canvas: np.ndarray
    x_axis: Axis
    y_axis: Axis
    legend: dict[str, str] = tuple()
    title: str = None


def draw(canvas, x_axis, y_axis, legend, title=None) -> str:
    """Draw figure from plot elements (i.e. canvas, x-axis, y-axis, legend)

    Internally, this functions draws all elements as list of strings, and then
    joins them into a single string.

    Parameters
    ----------
    canvas : np.ndarray
        The data to be drawn
    x_axis : shellplot.axis.Axis
        Fitted x-axis
    y_axis : shellplot.axis.Axis
        Fitted y-axis
    legend : dict[str, str], optional
        Legend of the plot

    Returns
    -------
    str
        The drawn figure

    """
    left_pad = (
        max([len(str(val)) for (t, val) in y_axis.generate_ticks_and_labels()]) + 1
    )

    title_lines = _draw_title(title, x_axis.display_max, left_pad)
    canvas_lines = _draw_canvas(canvas)
    y_lines = _draw_y_axis(y_axis, left_pad)
    x_lines = _draw_x_axis(x_axis, left_pad)
    legend_lines = _draw_legend(legend)

    return _create_plot_str(canvas_lines, y_lines, x_lines, legend_lines, title_lines)


# -------------------------------------------------------------------------------------
# Drawing functions for individual plot elements (canvas, x-axis, y-axis, legend)
# -------------------------------------------------------------------------------------


def _draw_title(title, x_display_max, left_pad) -> List[str]:
    if title:
        # TODO: this could handle multi line titles
        label_pad = (x_display_max + 1) // 2 - len(str(title)) // 2
        yield " " * (left_pad + 1 + label_pad) + str(title)


def _draw_canvas(canvas):
    for i in reversed(range(canvas.shape[1])):
        plt_str = ""
        for j in range(canvas.shape[0]):
            plt_str += PALETTE[canvas[j, i]]
        yield plt_str


def _draw_y_axis(y_axis, left_pad):
    axis_label = y_axis.label or ""
    yield " " * (left_pad - len(axis_label) // 2) + axis_label

    ticks_and_labels = {k: v for k, v in y_axis.generate_ticks_and_labels()}

    for i in reversed(range(y_axis.display_max + 1)):
        if i in ticks_and_labels:
            yield str(ticks_and_labels[i]).rjust(left_pad) + "┤"
        else:
            yield " " * left_pad + "|"


def _draw_x_axis(x_axis, left_pad):
    ticks_and_labels = {k: v for k, v in x_axis.generate_ticks_and_labels()}

    upper_ax = " " * left_pad + "└"
    lower_ax = " " * left_pad + " "

    for j in range(x_axis.display_max + 1):
        if j in ticks_and_labels:
            lower_ax = lower_ax[: len(upper_ax)]  # trim to account for label length
            lower_ax += str(ticks_and_labels[j])
            upper_ax += "┬"
        else:
            upper_ax += "-"
            lower_ax += " "

    yield upper_ax
    yield lower_ax

    if x_axis.label is not None:
        label_pad = (x_axis.display_max + 1) // 2 - len(str(x_axis.label)) // 2
        yield " " * (left_pad + 1 + label_pad) + str(x_axis.label)


def _draw_legend(legend):
    for item in legend:
        legend_str = f"  {PALETTE[item.symbol]} {item.name}"
        yield legend_str


# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------


def _create_plot_str(canvas_lines, y_lines, x_lines, legend_lines, title_lines):
    plt_str = "\n"

    for title_line in title_lines:
        plt_str += f"{title_line}\n"

    plt_str += f"{next(y_lines)}\n"  # pop out y axis title

    for ax, canvas, leg in itertools.zip_longest(
        y_lines, canvas_lines, legend_lines, fillvalue=""
    ):
        plt_str += f"{ax}{canvas}{leg}\n"

    for ax in x_lines:
        plt_str += f"{ax}\n"

    return plt_str[:-1]
