import time
import typing
from PIL import Image

from board import Board
from icon import Icon, IconColorDict
from solve import Solver


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
        self.icon_size = Point(60, 60)
        #self.icon_size = Point(image.width // self.COLUMNS, image.height // self.ROWS)

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
            self.board.rows = self._detect_board(self.image, self.board)
            func()
            time.sleep(1 / self.FRAME_RATE)
            self.frame.count_up()

    def _detect_board(self, image: Image, board: Board) -> list:
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
        x = 11
        y = 38
        rgb = image.convert('RGB').getpixel((x, y))
        # TODO: refactoring
        margin = 53
        for k, v in IconColorDict.items():
            if k.value[0] - margin < rgb[0] < k.value[0] + margin and \
                    k.value[1] - margin < rgb[1] < k.value[1] + margin and \
                    k.value[2] - margin < rgb[2] < k.value[2] + margin:
                return v
        return Icon.Empty


class FrameCounter(object):
    current = 0

    def count_up(self) -> int:
        self.current += 1
        return self.current
