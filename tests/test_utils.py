import pytest

from shellplot.utils import tolerance_round


def test_round_sensibly():
    assert tolerance_round(0.399997) == 0.4
    assert tolerance_round(102.1) == 102
    assert tolerance_round(1.499997) == 1.5
    assert tolerance_round(503.4) == 503
