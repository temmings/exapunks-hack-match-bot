import time
import typing

from PIL import Image

from board import Board
from character import Character
from frame_counter import FrameCounter
from icon import Icon, IconFileDict
from solver import Solver
from image import diff_rms


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game(object):
    FRAME_RATE = 60
    ROWS = 9
    COLUMNS = 7

    debug = False

    def __init__(self, image: Image, solver: Solver, board: Board, char: Character):
        self.frame = FrameCounter()
        self.prev_image = None
        self.image = image
        self.solver = solver
        self.board = board
        self.char = char

        # guess icon size (x, y)
        #self.icon_size = Point(image.width // self.COLUMNS, image.height // self.ROWS)
        self.icon_size = Point(60, 60)

    def main_loop(self, callback: typing.Callable):
        while self.is_alive:
            self.board.update(self._detect_board(self.image))
            self.solver.solve(self.board, self.char)
            callback()
            time.sleep(1.0 / self.FRAME_RATE)
            self.frame.count_up()
        self.trace('game over.')

    def trace(self, msg):
        if self.debug:
            print(msg)

    @property
    def is_alive(self) -> bool:
        if self.prev_image is None:
            return True
        return 0.0 < diff_rms(self.prev_image, self.image)

    @property
    def current_frame(self) -> int:
        return self.frame.current

    def enable_debug(self):
        self.debug = True

    def load_image(self, image: Image):
        self.prev_image = self.image
        self.image = image

    def _detect_board(self, image: Image) -> list:
        new_board = []
        for n in range(0, self.ROWS + 1):
            new_board.append(self._detect_column(image, n))
        return new_board

    def _detect_column(self, image: Image, row_index: int) -> list:
        detect_cols = []
        for n in range(0, self.COLUMNS):
            x0 = self.icon_size.x * n
            y0 = self.icon_size.y * row_index
            x1 = x0 + self.icon_size.x
            y1 = y0 + self.icon_size.y

            im_icon = image.crop((x0, y0, x1, y1))
            #if self.debug:
            #    filename = 'capture/icon-%d-%d.png' % (row_index, n)
            #    im_icon.save(filename)
            icon = self._detect_icon(im_icon)
            detect_cols.append(icon)
        return detect_cols

    memo = {}
    def _detect_icon(self, image: Image) -> Icon:
        """
        TODO: めっちゃホットスポット
        """

        # key: Icon, value: rms
        rms_dict = {
            k: diff_rms(image, v) for k, v in IconFileDict.items()
        }
        # RMS の一番小さいアイコンを候補とする
        # 30 を超えているものは該当なしとして空白とする(値は適当)
        candidate = min(rms_dict.items(), key=lambda x: x[1])
        if candidate[1] < 30:
            return candidate[0]
        return Icon.Empty
