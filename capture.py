#!/usr/bin/env python
# coding: utf-8
#
from PIL import Image


class WindowSize(object):
    HD_PLUS = (1600, 900)
    FULL_HD = (1920, 1080)


class Capture(object):
    @property
    def window_size(self):
        raise NotImplemented()

    def crop(self, rect: tuple) -> Image:
        raise NotImplemented()
