"""Test drawing module
"""
import pytest

import numpy as np

from shellplot.axis import Axis
from shellplot.drawing import (
    _draw_canvas,
    _draw_legend,
    _draw_x_axis,
    _draw_y_axis,
    _pad_lines,
)


def test_draw_legend():
    legend = {1: "one", 2: "two"}
    legend_lines = ["+ one", "* two"]
    assert legend_lines == _draw_legend(legend)


@pytest.mark.parametrize(
    "lines,ref_lines,expecte_padded_lines",
    [
        (["a", "b"], ["a", "b", "c"], ["", "a", "b"]),
        (None, ["a", "b", "c"], ["", "", ""]),
    ],
)
def test_pad_lines(lines, ref_lines, expecte_padded_lines):
    padded_lines = _pad_lines(lines, ref_lines)
    assert padded_lines == expecte_padded_lines


@pytest.mark.parametrize(
    "axis,expected_axis_lines",
    [
        (
            Axis(display_length=51, label="my_fun_label", limits=(0, 1)),
            [
                "└┬---------┬---------┬---------┬---------┬---------┬\n",
                " 0.0       0.2       0.4       0.6       0.8       1.0\n",
                "                    my_fun_label",
            ],
        ),
        (
            Axis(display_length=51, label="my_fun_label", limits=(0, 0.01)),
            [
                "└┬---------┬---------┬---------┬---------┬---------┬\n",
                " 0.0       0.002     0.004     0.006     0.008     0.01\n",
                "                    my_fun_label",
            ],
        ),
    ],
)
def test_draw_x_axis(axis, expected_axis_lines):
    x_lines = _draw_x_axis(x_axis=axis, left_pad=0)
    assert x_lines == expected_axis_lines


@pytest.mark.parametrize(
    "axis,label,limits, expected_axis_lines",
    [
        (
            Axis(display_length=16),
            "my_fun_label",
            (0, 1),
            [
                "    my_fun_label",
                "      0.99┤",
                "          |",
                "          |",
                "          |",
                "          |",
                "      0.66┤",
                "          |",
                "          |",
                "          |",
                "          |",
                "      0.33┤",
                "          |",
                "          |",
                "          |",
                "          |",
                "       0.0┤",
            ],
        ),
    ],
)
def test_draw_y_axis(axis, label, limits, expected_axis_lines):
    axis.label = label
    axis.limits = limits

    y_lines = _draw_y_axis(y_axis=axis, left_pad=10)
    assert y_lines == expected_axis_lines


@pytest.mark.parametrize(
    "canvas,expected_canvas_lines",
    [
        (
            np.array(
                [
                    [0, 0, 0, 0, 5],
                    [0, 0, 0, 4, 0],
                    [0, 0, 3, 0, 0],
                    [0, 2, 0, 0, 0],
                    [1, 0, 0, 0, 0],
                ]
            ),
            ["@    ", " x   ", "  o  ", "   * ", "    +"],
        ),
    ],
)
def test_draw_canvas(canvas, expected_canvas_lines):
    canvas_lines = _draw_canvas(canvas)
    assert canvas_lines == expected_canvas_lines
