import time
import typing

from PIL import Image

from board import Board
from icon import Icon, IconFileDict
from solve import Solver
from image import diff_rms


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game(object):
    FRAME_RATE = 10
    ROWS = 9
    COLUMNS = 7

    def __init__(self, image: Image, solver: Solver, board: Board):
        self.frame = FrameCounter()
        self.prev_image = None
        self.image = image
        self.solver = solver
        self.board = board

        # guess icon size (x, y)
        self.icon_size = Point(image.width // self.COLUMNS, image.height // self.ROWS)

    @property
    def is_alive(self) -> bool:
        return True

    @property
    def current_frame(self) -> int:
        return self.frame.current

    def load_image(self, image: Image):
        self.prev_image = self.image
        self.image = image

    def main_loop(self, func: typing.Callable):
        while self.is_alive:
            self.board.rows = self._detect_board(self.image)
            func()
            time.sleep(1 / self.FRAME_RATE)
            self.frame.count_up()

    def _detect_board(self, image: Image) -> list:
        new_board = []
        for n in range(0, self.ROWS + 1):
            new_board.append(self._detect_column(image, n, self.COLUMNS))
        return new_board

    def _detect_column(self, image: Image, row_number: int, column_number) -> list:
        detect_cols = []
        for i in range(0, column_number):
            im_icon = image.crop((
                i * self.icon_size.x, row_number * self.icon_size.y,
                (i + 1) * self.icon_size.x, (row_number + 1) * self.icon_size.y
            ))
            im_icon.save('capture/icon-%d.png' % i)
            icon = self._detect_icon(im_icon)
            detect_cols.append(icon)
        return detect_cols

    @staticmethod
    def _detect_icon(image: Image) -> Icon:
        # key: Icon, value: rms
        rms_dict = {
            k: diff_rms(image, Image.open(v)) for k, v in IconFileDict.items()
        }
        # RMS の一番小さいアイコンを候補とする
        candidate = min(rms_dict.items(), key=lambda x: x[1])
        if candidate[1] < 30:
            return candidate[0]
        return Icon.Empty

    """
    @staticmethod
    def _detect_icon(image: Image) -> Icon:
        for icon, icon_rgb in IconColorDict.items():
            rgb = list(image.convert('RGB').getdata())
            if icon_rgb.value in rgb:
                return icon
        return Icon.Empty
    """


class FrameCounter(object):
    current = 0

    def count_up(self) -> int:
        self.current += 1
        return self.current
