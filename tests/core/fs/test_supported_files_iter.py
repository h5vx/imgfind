# coding=utf-8
import os

from imgfind.core.fs import supported_files_iter
from tests.conftest import assets_path

assets_files_count = os.listdir


def test_recursive():
    result = tuple(supported_files_iter(assets_path, recursive=True))

    assert len(result) == 13

    for path in result:
        assert os.path.isfile(path)


def test_non_recursive():
    result = tuple(supported_files_iter(assets_path, recursive=False))

    assert len(result) == 11

    dirname = os.path.dirname(result[0])

    for path in result:
        assert os.path.isfile(path)
        assert os.path.dirname(path) == dirname


def test_recursive_mime():
    result = tuple(supported_files_iter(assets_path, recursive=True, by_mime=True))

    assert len(result) == 11

    dirname = os.path.dirname(result[0])

    for path in result:
        assert os.path.isfile(path)
        assert os.path.dirname(path) == dirname
