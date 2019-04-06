import numpy as np
from PIL import Image, ImageChops

from icon import Icon, IconFileDict
from point import Point

RMSE_THRESHOLD = 0.10


class BoardStateDetector(object):
    debug = False

    # 各アイコンのヒストグラムを事前に取得しておく
    icon_histogram_dict = {
        k: Image.open(v).histogram() for k, v in IconFileDict.items()
    }

    def __init__(self, image: Image, row_size: int, column_size: int):
        self.image = image
        self.row_size = row_size
        self.column_size = column_size

        # guess icon size (x, y)
        self.icon_size = Point(image.width // self.column_size,
                               image.height // self.row_size)

    def get_board_from_image(self, image: Image) -> np.ndarray:
        new_board = []
        for n in range(self.row_size):
            new_board.append(self._detect_column(image, n))
        return np.asarray(new_board, dtype=np.uint16)

    def enable_debug(self):
        self.debug = True

    def _detect_column(self, image: Image, row_index: int) -> list:
        detect_cols = []
        for n in range(self.column_size):
            x0 = self.icon_size.x * n
            y0 = self.icon_size.y * row_index
            x1 = x0 + self.icon_size.x
            y1 = y0 + self.icon_size.y

            im_icon = image.crop((x0, y0, x1, y1))
            if self.debug:
                filename = 'capture/icon-%d-%d.png' % (row_index, n)
                im_icon.save(filename)
            icon = self._detect_icon(im_icon)
            detect_cols.append(icon.value)
        return detect_cols

    @classmethod
    def _detect_icon(cls, image: Image) -> Icon:
        h1 = image.histogram()
        # key: Icon, value: rms
        # TODO: ホットスポット。 200～300ms くらい掛かっている
        rmse_dict = {
            k: cls.diff_rmse(h1, v) for k, v in cls.icon_histogram_dict.items()
        }
        # RMSEで画像を比較し、一番近しいアイコンを採用する
        # 0.10(値は適当)を超えているものは該当なしとして空白とする
        candidate = min(rmse_dict.items(), key=lambda x: x[1])
        if RMSE_THRESHOLD < candidate[1]:
            return Icon.Empty
        return candidate[0]

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
        # noinspection PyTypeChecker
        errors = np.asarray(ImageChops.difference(a, b)) / 255
        return np.sqrt(np.mean(np.square(errors)))

    @staticmethod
    def diff_rmse(h1: list, h2: list) -> float:
        """
        Calculates the root mean square error (RSME) between two images
        """
        errors = (np.asarray(h1) - np.asarray(h2)) / 255
        return np.sqrt(np.mean(np.square(errors)))
