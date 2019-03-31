import math
import operator
from functools import reduce

from PIL import Image


def diff_rms(a: Image, b: Image) -> float:
    h1 = a.histogram()
    h2 = b.histogram()

    # Root-Mean-Square Difference
    rms = math.sqrt(
        reduce(operator.add,
               map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    return rms
