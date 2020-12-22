"""Test drawing module
"""
import pytest

from shellplot.drawing import _draw_legend, _pad_lines


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
