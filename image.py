import numpy as np

from PIL import Image, ImageChops


def get_rmse(a: Image, b: Image) -> float:
    """
    Calculates the root mean square error (RSME) between two images
    reference: https://stackoverflow.com/questions/3098406/root-mean-square-difference-between-two-images-using-python-and-pil
    >>> a = Image.open('test/icon_green.png')
    >>> b = Image.open('test/icon_green.png')
    >>> get_rmse(a, b)
    0.0
    >>> a = Image.open('test/icon_green.png')
    >>> b = Image.open('test/icon_red.png')
    >>> rms = get_rmse(a, b)
    >>> 0.0 < rms
    True
    """
    # noinspection PyTypeChecker
    errors = np.asarray(ImageChops.difference(a, b)) / 255
    return np.sqrt(np.mean(np.square(errors)))


def diff_rmse(h1: list, h2: list) -> float:
    """
    Calculates the root mean square error (RSME) between two images
    """
    errors = (np.asarray(h1) - np.asarray(h2)) / 255
    return np.sqrt(np.mean(np.square(errors)))
