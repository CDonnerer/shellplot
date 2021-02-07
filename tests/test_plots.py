# -*- coding: utf-8 -*-

import pytest

import numpy as np
import pandas as pd

from shellplot.figure import figure
from shellplot.plots import barh, boxplot, hist, plot

# -----------------------------------------------------------------------------
# Test `plot` function
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_linear_plot():
    return "\n".join(
        [
            "",
            "  y",
            " 9┤                  +",
            "  |                +  ",
            "  |              +    ",
            " 6┤            +      ",
            "  |          +        ",
            "  |        +          ",
            " 3┤      +            ",
            "  |    +              ",
            "  |  +                ",
            " 0┤+                  ",
            "  └┬-----┬-----┬-----┬",
            "   0     3     6     9",
            "            x",
        ]
    )


@pytest.mark.parametrize(
    "x",
    [
        (np.arange(0, 10, 1)),
        (pd.Series(np.arange(0, 10, 1))),
    ],
)
def test_plot_linear(x, expected_linear_plot):
    plt_str = plot(
        x=x,
        y=x,
        figsize=(19, 10),
        xlim=(0, 9),
        ylim=(0, 9),
        xlabel="x",
        ylabel="y",
        return_type="str",
    )
    assert plt_str == expected_linear_plot

    fig = figure(figsize=(19, 10), xlim=(0, 9), ylim=(0, 9), xlabel="x", ylabel="y")
    fig.plot(x, x)
    assert fig.draw() == expected_linear_plot

    fig.clear()
    plot(x, x, fig=fig)
    assert fig.draw() == expected_linear_plot


def test_plot_linear_pd_labels(expected_linear_plot):
    x = pd.Series(np.arange(0, 10, 1), name="x")
    y = pd.Series(np.arange(0, 10, 1), name="y")

    plt_str = plot(
        x=x,
        y=y,
        figsize=(19, 10),
        xlim=(0, 9),
        ylim=(0, 9),
        xlabel="x",
        ylabel="y",
        return_type="str",
    )
    assert plt_str == expected_linear_plot


@pytest.fixture
def expected_linear_plot_color():
    return "\n".join(
        [
            "",
            " 9┤                  @",
            "  |                @  ",
            "  |              x    ",
            " 6┤            x      ",
            "  |          o        ",
            "  |        o          + 0",
            " 3┤      *            * 1",
            "  |    *              o 2",
            "  |  +                x 3",
            " 0┤+                  @ 4",
            "  └┬-----┬-----┬-----┬",
            "   0     3     6     9",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x, color",
    [
        (np.arange(0, 10, 1), np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4])),
        (
            pd.Series(np.arange(0, 10, 1)),
            pd.Series(np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4])),
        ),
    ],
)
def test_plot_linear_color(x, color, expected_linear_plot_color):
    plt_str = plot(
        x=x,
        y=x,
        color=color,
        figsize=(19, 10),
        return_type="str",
    )
    assert plt_str == expected_linear_plot_color


@pytest.fixture
def expected_linear_multi_plot():
    return "\n".join(
        [
            "",
            " 9┤*                 +",
            "  |  *             +  ",
            "  |    *         +    ",
            " 6┤      *     +      ",
            "  |        * +        ",
            "  |        + *        ",
            " 3┤      +     *      ",
            "  |    +         *    ",
            "  |  +             *  + up",
            " 0┤+                 ** down",
            "  └┬-----┬-----┬-----┬",
            "   0     3     6     9",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x, y",
    [
        (
            np.vstack((np.arange(0, 10, 1), np.arange(0, 10, 1))),
            np.vstack((np.arange(0, 10, 1), np.arange(9, -1, -1))),
        ),
        (
            pd.DataFrame({"up": np.arange(0, 10, 1), "down": np.arange(0, 10, 1)}),
            pd.DataFrame({"up": np.arange(0, 10, 1), "down": np.arange(9, -1, -1)}),
        ),
    ],
)
def test_plot_multi_linear(x, y, expected_linear_multi_plot):
    if isinstance(x, np.ndarray):
        label = ["up", "down"]
    else:
        label = None

    plt_str = plot(
        x=x,
        y=y,
        figsize=(19, 10),
        xlim=(0, 9),
        ylim=(0, 9),
        label=label,
        return_type="str",
    )
    assert plt_str == expected_linear_multi_plot


@pytest.fixture
def expected_linear_line_plot():
    return "\n".join(
        [
            "",
            "  y",
            " 9┤         +",
            "  |        · ",
            "  |       ·  ",
            " 6┤      +   ",
            "  |     ·    ",
            "  |    ·     ",
            " 3┤   +      ",
            "  |  ·       ",
            "  | ·        ",
            " 0┤+         ",
            "  └┬--┬--┬--┬",
            "   0  3  6  9",
            "        x",
        ]
    )


@pytest.mark.parametrize(
    "x",
    [
        (pd.Series(np.arange(0, 10, 3))),
    ],
)
def test_plot_linear_line(x, expected_linear_line_plot):
    plt_str = plot(
        x=x,
        y=x,
        line=True,
        figsize=(10, 10),
        xlim=(0, 9),
        ylim=(0, 9),
        xlabel="x",
        ylabel="y",
        return_type="str",
    )
    assert plt_str == expected_linear_line_plot


# -----------------------------------------------------------------------------
# Test `hist` function
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_hist():
    return "\n".join(
        [
            "",
            "counts",
            " 9┤                   --------   ",
            "  |                  |        |  ",
            "  |                  |        |  ",
            " 6┤                  |        |  ",
            "  |                  |        |  ",
            "  |                  |        |  ",
            " 3┤          --------|        |  ",
            "  |         |        |        |  ",
            "  | --------|        |        |  ",
            " 0┤|        |        |        |  ",
            "  └┬--------┬--------┬--------┬--",
            "   0        1        2        3",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x",
    [
        (
            np.array(
                # fmt: off
                [
                    0,
                    1, 1, 1,
                    2, 2, 2,
                    3, 3, 3, 3, 3, 3,
                ]
            )
        ),
        (
            pd.Series(
                np.array(
                    # fmt: off
                    [
                        0,
                        1, 1, 1,
                        2, 2, 2,
                        3, 3, 3, 3, 3, 3,
                    ]
                )
            )
        ),
    ],
)
def test_hist(x, expected_hist):
    plt_str = hist(
        x=x,
        bins=3,
        figsize=(30, 10),
        return_type="str",
    )
    assert plt_str == expected_hist

    fig = figure(figsize=(30, 10), ylabel="counts")  # TODO: consistent?
    fig.hist(x, bins=3)
    assert fig.draw() == expected_hist


@pytest.mark.parametrize(
    "bins, figsize",
    [
        (30, (20, 10)),
        (20, (20, 10)),
        (np.linspace(0, 1, 20), (20, 10)),
        ([0, 1, 2, 3, 4, 5], (5, 5)),
        ("not a bin", (20, 10)),
    ],
)
def test_hist_bin_failure(bins, figsize):
    x = np.random.randn(100)
    with pytest.raises(ValueError):
        hist(
            x=x,
            bins=bins,
            figsize=figsize,
        )


# -----------------------------------------------------------------------------
# Test `barh` function
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_barh():
    return "\n".join(
        [
            "",
            "      |----------------              ",
            "  four┤                |             ",
            "      |----------------------------- ",
            " three┤                             |",
            "      |----------------------------- ",
            "   two┤             |                ",
            "      |-------------                 ",
            "   one┤  |                           ",
            "      |--                            ",
            "      └┬------┬------┬-------┬------┬",
            "       0      30     60      90     120",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x, labels",
    [
        (np.array([10, 56, 121, 67]), np.array(["one", "two", "three", "four"])),
        (
            pd.Series(
                data=np.array([10, 56, 121, 67]),
                index=np.array(["one", "two", "three", "four"]),
            ),
            None,
        ),
    ],
)
def test_barh(x, labels, expected_barh):
    plt_str = barh(x, labels=labels, figsize=(30, 9), return_type="str")
    assert plt_str == expected_barh

    fig = figure(figsize=(30, 9))
    fig.barh(x, labels=labels)
    assert fig.draw() == expected_barh

    fig.clear()
    barh(x, labels=labels, fig=fig)
    assert fig.draw() == expected_barh


# -----------------------------------------------------------------------------
# Test `boxplot` function
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_boxplot():
    return "\n".join(
        [
            "",
            "    |                                         ",
            "    |                                         ",
            "    |         ---------------                 ",
            "    ||       |       |       |               |",
            " box┤|-------|       |       |---------------|",
            "    ||       |       |       |               |",
            "    |         ---------------                 ",
            "    |                                         ",
            "    |                                         ",
            "    └┬-------┬-------┬-------┬-------┬-------┬",
            "     0       1       2       3       4       5",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x, labels",
    [
        (np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5]), ["box"]),
        (
            pd.Series(data=np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5]), name="box"),
            None,
        ),
    ],
)
def test_boxplot(x, labels, expected_boxplot):
    plt_str = boxplot(x, labels=labels, figsize=(41, 9), return_type="str")
    assert plt_str == expected_boxplot


@pytest.fixture
def expected_multi_boxplot():
    return "\n".join(
        [
            "",
            "      |                                         ",
            "      |         ---------------                 ",
            "      ||       |       |       |               |",
            " box_3┤|-------|       |       |---------------|",
            "      ||       |       |       |               |",
            "      |         ---------------                 ",
            "      |                                         ",
            "      |                                         ",
            "      |         ---------------                 ",
            "      ||       |       |       |               |",
            " box_2┤|-------|       |       |---------------|",
            "      ||       |       |       |               |",
            "      |         ---------------                 ",
            "      |                                         ",
            "      |                                         ",
            "      |         ---------------                 ",
            "      ||       |       |       |               |",
            " box_1┤|-------|       |       |---------------|",
            "      ||       |       |       |               |",
            "      |         ---------------                 ",
            "      |                                         ",
            "      └┬-------┬-------┬-------┬-------┬-------┬",
            "       0       1       2       3       4       5",
            "",
        ]
    )


@pytest.mark.parametrize(
    "x, labels",
    [
        ([np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5])] * 3, ["box_1", "box_2", "box_3"]),
        (
            pd.DataFrame(
                {
                    "box_1": np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5]),
                    "box_2": np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5]),
                    "box_3": np.array([0, 1, 1, 1, 2, 2, 3, 3, 3, 5]),
                }
            ),
            None,
        ),
    ],
)
def test_multi_boxplot(x, labels, expected_multi_boxplot):
    plt_str = boxplot(x, labels=labels, figsize=(41, 21), return_type="str")
    assert plt_str == expected_multi_boxplot
