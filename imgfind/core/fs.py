# coding=utf-8
import os

import magic

from imgfind.core import settings


def is_supported_file(path: str, by_mime: bool = False):
    """
    :param path: Path to the file
    :param by_mime: Check support via mime-type instead of file extension
    :returns: True if file is supported
    """
    if not os.path.isfile(path):
        return False

    if by_mime:
        mime = magic.from_file(path, mime=True)
        return mime in settings.SUPPORTED_MIME_TYPES

    _, ext = os.path.splitext(path)
    ext = ext[1:].lower()
    return ext in settings.SUPPORTED_FILE_EXTENSIONS


# TODO: documentation
def supported_files_iter(path, recursive=True, by_mime=False):
    if os.path.isfile(path):
        if is_supported_file(path):
            return (path,)
        return

    if not recursive:
        for f in os.listdir(path):
            f = os.path.join(path, f)
            if is_supported_file(f, by_mime):
                yield f
        return

    for root, dirs, files in os.walk(path):
        files = (os.path.join(root, f) for f in files)

        for f in files:
            if is_supported_file(f, by_mime):
                yield f
