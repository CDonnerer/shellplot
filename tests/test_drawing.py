"""Test drawing module
"""

from shellplot.drawing import _draw_legend


def test_draw_legend():
    legend = {1: "one", 2: "two"}
    legend_lines = ["+ one", "* two"]
    assert legend_lines == _draw_legend(legend)
