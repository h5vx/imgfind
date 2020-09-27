# coding=utf-8
import numpy as np
import pytest

from imgfind.core.image import get_dominant_colors
from tests.conftest import asset


@pytest.mark.parametrize(
    "asset_name,n_dominants,downscale_to,exp_palette,exp_freqs,exp_shape",
    (
        pytest.param(
            "sample_1280×853.jpeg",
            2,
            None,
            ((52, 45, 58), (178, 146, 169)),
            (0.53, 0.47),
            (853, 1280, 3),
            id="JPEG",
        ),
        pytest.param(
            "sample_640×426.png",
            2,
            None,
            ((52, 45, 56), (177, 144, 169)),
            (0.52, 0.48),
            (426, 640, 3),
            id="PNG",
        ),
        pytest.param(
            "sample_640×426.bmp",
            2,
            None,
            ((52, 45, 56), (177, 144, 169)),
            (0.52, 0.48),
            (426, 640, 3),
            id="BMP",
        ),
        pytest.param(
            "sample_640×426.tiff",
            2,
            None,
            ((52, 45, 56), (176, 144, 168)),
            (0.52, 0.48),
            (426, 640, 3),
            id="TIFF",
        ),
        pytest.param(
            "sample_170×256.ico",
            2,
            None,
            ((55, 48, 57), (173, 141, 167)),
            (0.52, 0.48),
            (170, 256, 3),
            id="ICO",
        ),
        pytest.param(
            "sample_640×426.gif",
            2,
            None,
            ((53, 45, 56), (176, 144, 169)),
            (0.52, 0.48),
            (426, 640, 3),
            id="GIF",
        ),
        pytest.param(
            "sample_640×426.png",
            2,
            1000,
            ((52, 45, 56), (177, 144, 169)),
            (0.52, 0.48),
            (426, 640, 3),
            id="PNG (shouldn't downscale)",
        ),
        pytest.param(
            "tiger_001.png",
            2,
            300,
            ((247, 245, 244), (143, 122, 96)),
            (0.58, 0.42),
            (234, 300, 3),
            id="PNG (transparent)",
        ),
    ),
)
def test_supported_images(asset_name, n_dominants, downscale_to, exp_palette, exp_freqs, exp_shape):
    image_path = asset(asset_name)
    shape, palette, freqs = get_dominant_colors(image_path, n_dominants, downscale_to)

    assert len(palette) == n_dominants
    assert len(shape) == 3
    assert len(freqs) == n_dominants

    np.testing.assert_equal(np.uint8(palette), exp_palette)
    np.testing.assert_allclose(freqs, exp_freqs, rtol=0.01)
    assert shape == exp_shape


@pytest.mark.parametrize(
    "asset_name",
    (pytest.param("sample1.webp", id="WEBP"),),
)
def test_unsupported_image(asset_name):
    image_path = asset(asset_name)

    try:
        get_dominant_colors(image_path, 2)
    except ValueError:
        pass
    except Exception as e:
        raise AssertionError(f"Expected ValueError exception, but got {e.__class__.__name__}")
    else:
        raise AssertionError(f"Unsupported image format passed, but got no exception")
