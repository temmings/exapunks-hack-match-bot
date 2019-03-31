import math
import operator
from functools import reduce

from PIL import Image


def diff_rms(a: Image, b: Image) -> float:
    """
    >>> a = Image.open('test/icon_green.png')
    >>> b = Image.open('test/icon_green.png')
    >>> diff_rms(a, b)
    0.0
    >>> a = Image.open('test/icon_green.png')
    >>> b = Image.open('test/icon_red.png')
    >>> diff_rms(a, b)
    24.969473550217273
    """
    h1 = a.histogram()
    h2 = b.histogram()

    # Root-Mean-Square Difference: 二乗平均平方根
    rms = math.sqrt(
        reduce(operator.add,
               map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    return rms
