#!/usr/bin/env python3
# coding: utf-8
import argparse
import multiprocessing as mp
import os
import shutil
from itertools import count
from typing import List

from imgfind.core import fs, tasks
from imgfind.utils import color


def print_results(results: List[tasks.RatioCalculationResult], threshold: int = 10):
    termsize = shutil.get_terminal_size((80, 20))

    print("=" * termsize.columns)
    print("RESULTS".center(termsize.columns))
    print("=" * termsize.columns)

    results = filter(lambda r: r.ratio > (threshold / 100), results)
    results = sorted(results, key=lambda k: k.ratio)

    if not results:
        print("Not even close")
        return

    print(f"{'#':>3s} | {'R':^4s} | Path")
    for result, index in zip(results, count(start=len(results), step=-1)):
        print("{:3d} | {:>3d}% | {}".format(index, int(result.ratio * 100), result.task.path))


def main():
    cpu_count = os.cpu_count() or 1
    default_proc_count = max(1, int(cpu_count * 0.8))

    p = argparse.ArgumentParser()
    p.add_argument("-n", help="Number of dominant colors to calculate", type=int, default=2)
    p.add_argument(
        "-p",
        "--processes",
        help=f"Number of calculation processes; on your system it defaults to {default_proc_count}",
        type=int,
        default=default_proc_count,
    )
    p.add_argument("--downscale", help="Downscale largest side to specified size before processing", type=int)
    p.add_argument("--by-mime", help="Accept files by mime type rather than by extension", action="store_true")
    p.add_argument("-r", "--recurse", help="Recurse into directories", action="store_true")
    p.add_argument("path", help="Path to search for images", default=".")
    p.add_argument("color", help="Color to search in CSS format (red, blue, f00, 0c0e15)")
    args = p.parse_args()

    results = []

    def result_callback(result: tasks.RatioCalculationResult):
        print("{:80s}\t{:.0f}%".format(result.task.path, result.ratio * 100))
        results.append(result)

    def error_callback(error: tasks.TaskExecutionError):
        print("{:80s}\t{}".format(error.task.path, error.original_exception))

    pool = mp.Pool(args.processes)

    for path in fs.supported_files_iter(args.path, recursive=args.recurse, by_mime=args.by_mime):
        task = tasks.RatioCalculationTask(
            path=path,
            num_dominants=args.n,
            color=color.color_from_str(args.color),
            downscale_to=args.downscale,
        )
        pool.apply_async(
            tasks.matching_ratio_calculation,
            args=(task,),
            callback=result_callback,
            error_callback=error_callback,
        )

    pool.close()
    pool.join()

    print_results(results, threshold=10)


if __name__ == "__main__":
    main()
