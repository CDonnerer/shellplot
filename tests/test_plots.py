# -*- coding: utf-8 -*-

import pytest

import numpy as np
import pandas as pd

from shellplot.plots import _add_hbar, _add_vbar, _barh, _boxplot, hist, plot

# -----------------------------------------------------------------------------
# 'Integration' style 'tests' that only check everything runs end to end
# -----------------------------------------------------------------------------


def test_barh():
    x = np.array([10, 56, 121, 67])
    labels = np.array(["one", "two", "three", "four"])
    plt_str = _barh(x, labels=labels)
    assert isinstance(plt_str, str)


def test_boxplot():
    x = np.random.randn(1000)
    plt_str = _boxplot(x)
    assert isinstance(plt_str, str)


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
            "  └┬---┬----┬---┬----┬",
            "   0.0 2.2  4.4 6.6  8.8",
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
            "  └┬---┬----┬---┬----┬",
            "   0.0 2.2  4.4 6.6  8.8",
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


# -----------------------------------------------------------------------------
# Test canvas elements
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_canvas_vbar():
    return np.array(
        [
            [0, 0, 0, 0, 0],
            [20, 20, 20, 0, 0],
            [0, 0, 0, 22, 0],
            [20, 20, 20, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_add_vbar(expected_canvas_vbar):
    canvas = np.zeros(shape=(5, 5), dtype=int)
    canvas = _add_vbar(canvas, start=1, width=1, height=3)
    np.testing.assert_equal(canvas, expected_canvas_vbar)


@pytest.fixture
def expected_canvas_hbar():
    return np.array(
        [
            [22, 0, 0, 22, 0],
            [22, 0, 0, 22, 0],
            [0, 20, 20, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_add_hbar(expected_canvas_hbar):
    canvas = np.zeros(shape=(5, 5), dtype=int)
    canvas = _add_hbar(canvas, start=0, width=2, height=2)
    np.testing.assert_equal(canvas, expected_canvas_hbar)
