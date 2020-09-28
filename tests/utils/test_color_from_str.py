# coding=utf-8
import numpy as np
import pytest

from imgfind.utils.color import color_from_str


@pytest.mark.parametrize(
    "color,exp_result",
    (
        ("red", (1, 0, 0)),
        ("magenta", (1, 0, 1)),
        ("green", (0, 0.5, 0)),
        ("aliceblue", (0.94, 0.97, 1)),
        ("fff", (1, 1, 1)),
        ("000", (0, 0, 0)),
        ("123", (0.06, 0.13, 0.2)),
        ("0c0e15", (0.05, 0.05, 0.08)),
        ("0C0E15", (0.05, 0.05, 0.08)),
    ),
)
def test(color, exp_result):
    result = color_from_str(color)
    np.testing.assert_allclose(result, exp_result, atol=0.01)


@pytest.mark.parametrize("color", ("unknowncolor", "xxxxxx", "xxx", "abx", "1234567"))
def test_raises_error(color):
    try:
        color_from_str(color)
    except ValueError:
        pass
    else:
        raise AssertionError("Function should fail")
