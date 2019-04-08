import typing

import numpy as np
from PIL import Image, ImageChops

from icon import Icon, IconFileDict
from point import Point
from traceable import Traceable


class BoardStateDetector(Traceable):
    RMSE_THRESHOLD = 0.15

    def __init__(self, image: Image, row_size: int, column_size: int, icon_size: Point):
        self.image = image
        self.row_size = row_size
        self.column_size = column_size
        self.icon_size = icon_size
        self.debug = False

        # 各アイコンのヒストグラムを取得
        self.icon_histogram_dict = {
            k: self.get_histogram(Image.open(v)) for k, v in IconFileDict.items()
        }

        import cv2 as cv
        im = np.array(image.convert('L'))
        template = cv.imread('test/__icon_under_mark.grey.png',  cv.IMREAD_GRAYSCALE)
        result = cv.matchTemplate(im, template, cv.TM_SQDIFF, None)
        offset = (np.unravel_index(result.argmin(), result.shape))
        self.offset = (0, 0)
        if offset[0] == 1:
            self.offset = (offset[0], offset[1])

    def enable_debug(self):
        self.debug = True

    def get_board_from_image(self, image: Image) -> np.ndarray:
        new_board = []
        for n in range(self.row_size):
            new_board.append(self.detect_column(image, n))
        return np.asarray(new_board, dtype=np.uint16)

    def detect_column(self, image: Image, row_index: int) -> typing.List[Icon]:
        detect_cols = []
        for n in range(self.column_size):
            x0 = self.offset[0] + self.icon_size.x * n
            y0 = self.offset[1] + self.icon_size.y * row_index
            x1 = x0 + self.icon_size.x
            y1 = y0 + self.icon_size.y
            im_icon = image.crop((x0, y0, x1, y1))
            if self.debug:
                filename = 'capture/icon-%d-%d.png' % (row_index, n)
                im_icon.save(filename)
            icon = self.detect_icon(im_icon)
            detect_cols.append(icon)
        return detect_cols

    def detect_icon(self, image: Image) -> Icon:
        h1 = self.get_histogram(image)
        # key: Icon, value: rms
        rmse_dict = {
            k: self.diff_rmse(h1, v) for k, v in self.icon_histogram_dict.items()
        }
        # RMSEで画像を比較し、一番近しいアイコンを採用する
        # RMSE_THRESHOLDを超えているものは該当なしとして空白とする
        candidate = min(rmse_dict.items(), key=lambda x: x[1])
        if self.RMSE_THRESHOLD < candidate[1]:
            return Icon.Empty
        return candidate[0]

    @staticmethod
    def get_histogram(image: Image):
        return np.bincount(np.asarray(image).ravel(), minlength=256)

    @staticmethod
    def get_rmse(a: Image, b: Image) -> float:
        """
        Calculates the root mean square error (RSME) between two images
        reference: https://stackoverflow.com/questions/3098406/root-mean-square-difference-between-two-images-using-python-and-pil
        >>> a = Image.open('test/icon_green.png')
        >>> b = Image.open('test/icon_green.png')
        >>> BoardStateDetector.get_rmse(a, b)
        0.0
        >>> a = Image.open('test/icon_green.png')
        >>> b = Image.open('test/icon_red.png')
        >>> rms = BoardStateDetector.get_rmse(a, b)
        >>> 0.0 < rms
        True
        """
        errors = np.asarray(ImageChops.difference(a, b).getdata()) / 255
        return np.sqrt(np.mean(np.square(errors)))

    @staticmethod
    def diff_rmse(h1: np.array, h2: np.array) -> float:
        """
        Calculates the root mean square error (RSME) between two images
        """
        errors = (h1 - h2) / 255
        return np.sqrt(np.mean(np.square(errors)))
