import pytest

from shellplot.utils import tolerance_round


@pytest.mark.parametrize(
    "number,expected",
    [
        (0.399997, 0.4),
        (102.1, 102),
        (1.499997, 1.5),
        (503.4, 503),
    ]
)
def test_tolerance_round(number, expected):
    assert tolerance_round(number) == expected
