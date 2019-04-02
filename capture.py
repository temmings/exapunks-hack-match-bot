#!/usr/bin/env python
# coding: utf-8
#
from PIL import Image

from point import Point


class WindowSize(object):
    HD_PLUS = Point(1600, 900)
    FULL_HD = Point(1920, 1080)


class Capture(object):
    @property
    def window_size(self):
        raise NotImplemented()

    def crop(self, rect: tuple) -> Image:
        raise NotImplemented()
