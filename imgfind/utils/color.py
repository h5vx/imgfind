# coding=utf-8
from typing import Tuple, Union

import numpy as np
from skimage.color import rgb_colors


# TODO: documentation
def color_from_str(color_str: str) -> Tuple[Union[int, float]]:
    result = rgb_colors.__dict__.get(color_str)

    if result:
        return result

    if len(color_str) == 3:
        color_str = "".join(c * 2 for c in color_str)  # "123" -> "112233"

    if len(color_str) == 6:
        try:
            rgb = tuple(bytes.fromhex(color_str))
            return tuple(np.float32(rgb) / 255)
        except ValueError:
            pass

    raise ValueError("Unknown color specification format")
