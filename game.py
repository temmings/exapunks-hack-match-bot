import time
import typing
from queue import Queue

from PIL import Image

from board import Board
from character import Character
from frame_counter import FrameCounter
from icon import Icon, IconFileDict
from point import Point
from solver import Solver
from image import diff_rmse, get_rmse


class Game(object):
    FRAME_RATE = 60
    ROWS = 9
    COLUMNS = 7

    debug = False

    prev_captures = Queue()

    def __init__(self, image: Image, solver: Solver, board: Board, char: Character):
        self.frame = FrameCounter()
        self.image = image
        self.solver = solver
        self.board = board
        self.char = char

        # guess icon size (x, y)
        #self.icon_size = Point(image.width // self.COLUMNS, image.height // self.ROWS)
        self.icon_size = Point(60, 60)

        # 処理時間を稼ぐため、アイコンのヒストグラムを先に取得しておく
        self.icon_histogram_dict = {
            k: Image.open(v).histogram() for k, v in IconFileDict.items()
        }

        # 5世代のキャプチャ画像を取り出せるようにしておく
        for _ in range(5):
            self.prev_captures.put(None)

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
        # 直前のキャプチャを比較すると状態が同一なことがあるため、
        # キューに数世代前のキャプチャを持っておき、それと比較する
        prev_image = self.prev_captures.get()
        if not prev_image:
            return True
        return 0.0 < get_rmse(prev_image, self.image)

    @property
    def current_frame(self) -> int:
        return self.frame.current

    def enable_debug(self):
        self.debug = True

    def load_image(self, image: Image):
        self.prev_captures.put(self.image)
        self.image = image

    def _detect_board(self, image: Image) -> list:
        new_board = []
        map(new_board.append,
            [self._detect_column(image, n) for n in range(self.ROWS)])
        return new_board

    def _detect_column(self, image: Image, row_index: int) -> list:
        detect_cols = []
        for n in range(self.COLUMNS):
            x0 = self.icon_size.x * n
            y0 = self.icon_size.y * row_index
            x1 = x0 + self.icon_size.x
            y1 = y0 + self.icon_size.y

            im_icon = image.crop((x0, y0, x1, y1))
            if self.debug:
                filename = 'capture/icon-%d-%d.png' % (row_index, n)
                im_icon.save(filename)
            icon = self._detect_icon(im_icon)
            detect_cols.append(icon)
        return detect_cols

    def _detect_icon(self, image: Image) -> Icon:
        h1 = image.histogram()
        # key: Icon, value: rms
        # TODO: ホットスポット。 200～300ms くらい掛かっている
        rmse_dict = {
            k: diff_rmse(h1, v) for k, v in self.icon_histogram_dict.items()
        }
        # RMSEで画像を比較し、一番近しいアイコンを採用する
        # 0.08(値は適当)を超えているものは該当なしとして空白とする
        candidate = min(rmse_dict.items(), key=lambda x: x[1])
        if 0.08 < candidate[1]:
            return Icon.Empty
        return candidate[0]
