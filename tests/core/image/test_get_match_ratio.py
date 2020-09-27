# coding=utf-8
import numpy as np
import pytest
from skimage.color import rgb_colors as rgb

from imgfind.core.image import get_dominant_colors, get_match_ratio
from tests.conftest import asset


@pytest.mark.parametrize(
    "asset_name,n_dominants,color,exp_ratio",
    (
        pytest.param("100_magenta.png", 2, rgb.magenta, 0.81),
        pytest.param("100_magenta.png", 2, rgb.darkmagenta, 0.43),
        pytest.param("100_magenta.png", 2, rgb.grey, 0),
        pytest.param("100_magenta.png", 2, rgb.green, 0),
        pytest.param("100_magenta.png", 2, rgb.pink, 0),
        pytest.param("100_magenta.png", 2, rgb.pink, 0),
        pytest.param("50_magenta_50_green.png", 2, rgb.magenta, 0.41),
        pytest.param("50_magenta_50_green.png", 2, rgb.green, 0.46),
        pytest.param("50_magenta_50_green.png", 3, rgb.magenta, 0.41),
        pytest.param("50_magenta_50_green.png", 3, rgb.green, 0.46),
        pytest.param("45_magenta_25_cyan.png", 3, rgb.cyan, 0.25),
        pytest.param("45_magenta_25_cyan.png", 3, rgb.magenta, 0.57),
    ),
)
def test_matching_ratio(asset_name, n_dominants, color, exp_ratio):
    image_path = asset(asset_name)
    _, palette, freqs = get_dominant_colors(image_path, n_dominants)
    ratios = get_match_ratio(color, palette, freqs)

    np.testing.assert_allclose(ratios, exp_ratio, atol=0.01)
