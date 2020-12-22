"""Drawing module.

Functions for taking the elements of the plot (e.g. canvas, axis, legend) and
converts them to strings. Please note that drawing is entirely agnostic to the
type of plot.
"""


PALETTE = {
    # empty space
    0: " ",
    # scatter points
    1: "+",
    2: "*",
    3: "o",
    4: "x",
    5: "_",
    6: "|",
    # bar drawing
    20: "|",
    21: "_",
    22: "-",
    23: "┐",
}


def draw(canvas, x_axis, y_axis, legend=None):
    plt_lines = _draw_canvas(canvas)

    label_len = max([len(str(val)) for (t, val) in y_axis.tick_labels()])
    l_pad = label_len + 1

    y_lines = _draw_y_axis(canvas, y_axis, l_pad)
    x_lines = _draw_x_axis(canvas, x_axis, l_pad)

    if legend is not None:
        legend_lines = _draw_legend(legend)
    else:
        legend_lines = None

    return _join_plot_lines(plt_lines, y_lines, x_lines, legend_lines)


def _draw_legend(legend):
    legend_lines = list()

    for marker, name in legend.items():
        legend_str = f"{PALETTE[marker]} {name}"
        legend_lines.append(legend_str)
    return legend_lines


def _pad_lines(lines, ref_lines):
    if lines is None:
        lines = list()

    empty_pad = len(ref_lines) - len(lines)
    return [""] * empty_pad + lines


def _join_plot_lines(plt_lines, y_lines, x_lines, legend_lines):
    plt_str = "\n"

    plt_lines = _pad_lines(plt_lines, y_lines)
    legend_lines = _pad_lines(legend_lines, y_lines)

    for ax, plt, leg in zip(y_lines, plt_lines, legend_lines):
        plt_str += ax + plt + leg + "\n"

    for ax in x_lines:
        plt_str += ax

    return plt_str


def _draw_canvas(canvas):

    plt_lines = list()

    for i in reversed(range(canvas.shape[1])):
        plt_str = ""
        for j in range(canvas.shape[0]):
            plt_str += PALETTE[canvas[j, i]]
        plt_lines.append(plt_str)

    return plt_lines


def _draw_y_axis(canvas, y_axis, l_pad):
    y_lines = list()

    y_ticks = y_axis.tick_labels()

    for i in reversed(range(canvas.shape[1])):
        ax_line = ""
        if len(y_ticks) > 0 and i == y_ticks[-1][0]:
            ax_line += f"{str(y_ticks[-1][1]).rjust(l_pad)}┤"
            y_ticks.pop(-1)
        else:
            ax_line += " " * l_pad + "|"
        y_lines.append(ax_line)

    if y_axis.title is not None:
        title_pad = l_pad - len(y_axis.title) // 2
        title_str = " " * title_pad + y_axis.title
        y_lines.insert(0, title_str)
    return y_lines


def _draw_x_axis(canvas, x_axis, l_pad):
    x_ticks = x_axis.tick_labels()

    upper_ax = " " * l_pad + "└"
    lower_ax = " " * l_pad + " "
    marker = "┬"

    for j in range(canvas.shape[0]):
        if len(x_ticks) > 0 and j == x_ticks[0][0]:
            lower_ax = lower_ax[: len(upper_ax)]
            label = str(round(x_ticks[0][1], 2))
            lower_ax += label + " " * 20

            upper_ax += marker
            x_ticks.pop(0)
        else:
            upper_ax += "-"

    ax_lines = [upper_ax + "\n", lower_ax + "\n"]

    if x_axis.title is not None:
        title_pad = int(canvas.shape[0] / 2 - len(x_axis.title) / 2)
        title_str = " " * (l_pad + title_pad) + x_axis.title
        ax_lines.append(title_str)

    return ax_lines
