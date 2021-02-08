"""Drawing module.

Functions for taking the elements of the plot (e.g. canvas, axis, legend) and
converts them to strings. Please note that drawing is entirely agnostic to the
type of plot.
"""
from typing import List

PALETTE = {
    # empty space
    0: " ",
    # scatter points
    1: "+",
    2: "*",
    3: "o",
    4: "x",
    5: "@",
    6: "■",
    # line drawing
    10: "·",
    11: ":",
    # bar drawing
    20: "|",
    21: "_",
    22: "-",
    23: "┐",
}


def draw(canvas, x_axis, y_axis, legend=None) -> str:
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
    canvas_lines = _draw_canvas(canvas)

    left_pad = max([len(str(val)) for (t, val) in y_axis.gen_tick_labels()]) + 1
    y_lines = _draw_y_axis(y_axis, left_pad)
    x_lines = _draw_x_axis(x_axis, left_pad)

    if legend is not None:
        legend_lines = _draw_legend(legend)
    else:
        legend_lines = None

    return _join_plot_lines(canvas_lines, y_lines, x_lines, legend_lines)


# ------------------------------------------------------------------------------
# Drawing functions for individual plot elements (canvas, x-axis, y-axis, legend)
# ------------------------------------------------------------------------------


def _draw_canvas(canvas) -> List[str]:
    plt_lines = list()

    for i in reversed(range(canvas.shape[1])):
        plt_str = ""
        for j in range(canvas.shape[0]):
            plt_str += PALETTE[canvas[j, i]]
        plt_lines.append(plt_str)

    return plt_lines


def _draw_y_axis(y_axis, left_pad) -> List[str]:
    y_lines = list()

    y_ticks = list(y_axis.gen_tick_labels())

    for i in reversed(range(y_axis.display_max + 1)):
        ax_line = ""
        if len(y_ticks) > 0 and i == y_ticks[-1][0]:
            ax_line += f"{str(y_ticks[-1][1]).rjust(left_pad)}┤"
            y_ticks.pop(-1)
        else:
            ax_line += " " * left_pad + "|"
        y_lines.append(ax_line)

    if y_axis.label is not None:
        label_pad = left_pad - len(y_axis.label) // 2
        label_str = " " * label_pad + y_axis.label
        y_lines.insert(0, label_str)
    return y_lines


def _draw_x_axis(x_axis, left_pad) -> List[str]:
    x_ticks = list(x_axis.gen_tick_labels())

    upper_ax = " " * left_pad + "└"
    lower_ax = " " * left_pad + " "
    marker = "┬"
    overpad = 50

    for j in range(x_axis.display_max + 1):
        if len(x_ticks) > 0 and j == x_ticks[0][0]:
            lower_ax = lower_ax[: len(upper_ax)]
            lower_ax += str(x_ticks[0][1]) + " " * overpad
            upper_ax += marker
            x_ticks.pop(0)
        else:
            upper_ax += "-"

    ax_lines = [upper_ax + "\n", lower_ax[: len(lower_ax) - overpad] + "\n"]

    if x_axis.label is not None:
        label_pad = (x_axis.display_max + 1) // 2 - len(str(x_axis.label)) // 2
        label_str = " " * (left_pad + 1 + label_pad) + str(x_axis.label)
        ax_lines.append(label_str)

    return ax_lines


def _draw_legend(legend) -> List[str]:
    legend_lines = list()

    for marker, name in legend.items():
        legend_str = f"{PALETTE[marker]} {name}"
        legend_lines.append(legend_str)
    return legend_lines


# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------


def _join_plot_lines(plt_lines, y_lines, x_lines, legend_lines):
    plt_str = "\n"
    plt_lines = _pad_lines(plt_lines, y_lines)
    legend_lines = _pad_lines(legend_lines, y_lines)

    for ax, plt, leg in zip(y_lines, plt_lines, legend_lines):
        plt_str += ax + plt + leg + "\n"

    for ax in x_lines:
        plt_str += ax

    return plt_str


def _pad_lines(lines, ref_lines):
    if lines is None:
        lines = list()

    empty_pad = len(ref_lines) - len(lines)
    return [""] * empty_pad + lines
