# coding=utf-8
from typing import Optional, Tuple, Union

import attr

from imgfind.core.image import get_dominant_colors, get_match_ratio


@attr.s()
class RatioCalculationTask(object):
    path = attr.ib()  # type: str
    num_dominants = attr.ib()  # type: int
    color = attr.ib()  # type: Tuple[Union[int, float]]
    downscale_to = attr.ib(default=None)  # type: Optional[int]


@attr.s()
class RatioCalculationResult(object):
    task = attr.ib()  # type: RatioCalculationTask
    ratio = attr.ib()  # type: float


@attr.s()
class TaskExecutionError(Exception):
    original_exception = attr.ib()  # type: Exception
    task = attr.ib()  # type: RatioCalculationTask


def matching_ratio_calculation(task: RatioCalculationTask) -> RatioCalculationResult:
    try:
        _, palette, freqs = get_dominant_colors(task.path, task.num_dominants, task.downscale_to)
        ratio = get_match_ratio(task.color, palette, freqs)
    except Exception as e:
        raise TaskExecutionError(e, task)

    return RatioCalculationResult(task, ratio)
