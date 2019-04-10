from PIL import Image


class Capture(object):
    @property
    def window_size(self):
        raise NotImplemented()

    def crop(self, rect: tuple) -> Image:
        raise NotImplemented()