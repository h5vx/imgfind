# coding=utf-8
from typing import Tuple, Union

import cv2
import numpy as np
from skimage import color, io, transform


def downscale_image(img: np.ndarray, max_side_size: int) -> np.ndarray:
    """
    Downscale image preserving aspect ratio
    :param img: Image to downscale
    :param max_side_size: Size of largest side of new image
    :return: Downscaled image
    """
    scale_factor = max_side_size / max(img.shape[:2])

    if scale_factor >= 1:
        return img

    new_shape = int(img.shape[0] * scale_factor), int(img.shape[1] * scale_factor)
    return transform.resize(img, new_shape, preserve_range=True)


def get_dominant_colors(path: str, n: int, downscale_to: int = None) -> (Tuple[int], np.ndarray, np.ndarray):
    """
    Calculate dominant colors of image
    :param path: URL or path to image file
    :param n: Number of dominant colors to calculate
    :param downscale_to: Downscale image before processing, so largest side size will be equal to specified value
    :returns: Processed image shape, dominant colors palette of size *n*, and amounts of each color in palette
    """
    # Most of the code taken from there:
    # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    img = io.imread(path)

    # Resize before any operations
    if downscale_to:
        img = downscale_image(img, downscale_to)

    # Convert grayscale images to RGB
    if len(img.shape) == 2:
        img = color.gray2rgb(img)

    # Remove alpha channel if present
    if img.shape[-1] == 4:
        img = img[:, :, :-1]

    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    indices = np.argsort(counts)[::-1]
    freqs = counts[indices] / counts.sum()

    return img.shape, palette[indices], freqs


def get_match_ratio(color_: Tuple[Union[int, float]], palette: np.ndarray, freqs: np.ndarray) -> np.float:
    """
    Calculates how close the *color* is to the palette colors, considering amounts of each color
    Uses CIEDE 2000 standard to measure color distance
    :param color_: Source color in RGB (0 to 1) float array representation
    :param palette: Array of colors in RGB (0 to 255) float array representation
    :param freqs: Array with amounts (0 to 1) for each color in palette
    :returns: Matching ratio (0 to 1)
    """
    limit = np.float64(25)
    palette = color.rgb2lab(palette / 255)
    color_ = color.rgb2lab(np.float64(color_))

    deltas = color.deltaE_ciede2000(color_, palette, kL=2)
    deltas_inverted = limit - deltas
    deltas_inverted[deltas_inverted < 0] = 0

    ratios = deltas_inverted / limit * freqs
    return ratios.max()
