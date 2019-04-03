import time
import typing

import numpy as np

from board import Board
from character import Character
from frame_counter import FrameCounter
from icon import Icon


class Game(object):
    FRAME_RATE = 60
    FRAME_SECOND = 1.0 / FRAME_RATE
    ROWS, COLUMNS = (9, 7)

    def __init__(self, board: Board, char: Character):
        self.debug = False
        self.frame = FrameCounter()
        self.board = board
        self.char = char
        self.score = 0

    def main_loop(self, callback: typing.Callable):
        while self.is_alive:
            self.score = self.eval(self.board)
            callback()
            self.frame.count_up()
            if self.frame.process_time < self.FRAME_SECOND:
                time.sleep(self.FRAME_SECOND - self.process_time)
        self.trace('game over.')

    def eval(self, board: Board):
        score = 0
        has_effect = True
        while has_effect:
            has_action, board, _score = self.effect(board)
            score += _score
        return score

    def effect(self, board) -> typing.Tuple[bool, np.ndarray, int]:
        # TODO: 実装
        score = 0
        new_board = board
        return False, new_board, score

    def generate_row(self, board: Board):
        new_row = self.board.randomize_row()
        new_board = np.append(board.board, 0, new_row, axis=0)
        if (board.board == Icon.Empty.value).all():
            new_board = np.delete[new_board, self.ROWS]
        board.replace(new_board)

    @property
    def is_alive(self) -> bool:
        return self.board.max_icon_height < self.ROWS

    def trace(self, msg):
        if self.debug:
            print(msg)

    def enable_debug(self):
        self.debug = True

    @property
    def current_frame(self) -> int:
        return self.frame.current

    @property
    def process_time(self) -> int:
        return self.frame.process_time

