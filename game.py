import time
import typing

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
        self.__is_alive = True

    def main_loop(self, callback: typing.Callable):
        while self.is_alive:
            self.score = self.eval(self.board)
            callback()
            self.frame.count_up()
            if self.frame.process_time < self.FRAME_SECOND:
                time.sleep(self.FRAME_SECOND - self.process_time)
        self.trace('game over.')

    def eval(self, board: Board):
        has_action = True
        while has_action:
            has_action, board, _score = self.action(board)
            self.score += _score
        return self.score

    def action(self, board):
        raise NotImplemented

    def generate_row(self, board: Board):
        last_row = board.get_row(self.ROWS-1)
        if True in (last_row != Icon.Empty.value):
            self.__is_alive = False

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

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

