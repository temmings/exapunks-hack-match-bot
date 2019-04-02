import time
import typing

from board import Board
from character import Character
from frame_counter import FrameCounter


class Game(object):
    FRAME_RATE = 60
    ROWS, COLUMNS = (9, 7)

    debug = False

    def __init__(self, board: Board, char: Character):
        self.frame = FrameCounter()
        self.board = board
        self.char = char
        self.frame_second = 1.0 / self.FRAME_RATE

    def main_loop(self, callback: typing.Callable):
        while self.is_alive:
            callback()
            self.frame.count_up()
            if self.frame.process_time < self.frame_second:
                time.sleep(self.frame_second - self.process_time)
        self.trace('game over.')

    def trace(self, msg):
        if self.debug:
            print(msg)

    def enable_debug(self):
        self.debug = True

    @property
    def is_alive(self) -> bool:
        # TODO
        return True

    @property
    def current_frame(self) -> int:
        return self.frame.current

    @property
    def process_time(self) -> int:
        return self.frame.process_time

