# coding=utf-8
import os

tests_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(tests_path, "assets")


def asset(name):
    return os.path.join(assets_path, name)
