import time
import typing

import numpy as np

from board import Board
from character import Character
from frame_counter import FrameCounter
from icon import Icon, IconType, IconTypeDict, IconBombEraseDict

Score = typing.NewType('Score', int)


class Game(object):
    FRAME_RATE = 60
    FRAME_SECOND = 1.0 / FRAME_RATE

    def __init__(self, board: Board, char: Character):
        self.debug = False
        self.frame = FrameCounter()
        self.board = board
        self.char = char
        self.score = 0
        self.rows, self.columns = board.row_size, board.column_size

    def main_loop(self, callback: typing.Callable):
        while self.is_alive:
            self.score += self.effect(self.board)
            callback()
            self.frame.count_up()
            if self.frame.process_time < self.FRAME_SECOND:
                time.sleep(self.FRAME_SECOND - self.process_time)
        self.trace('game over.')

    def effect(self, board: Board, prev_board=None, score=Score(0)) -> Score:
        if prev_board is not None and (board.board == prev_board).all():
            return score
        prev_board = board.board.copy()
        for icon_type in IconType:
            for icon in IconTypeDict[icon_type]:
                score += self.erase_icon(board, icon, icon_type)
        packed_bord = board.pack(board.board)
        self.board.replace(packed_bord)
        return self.effect(board, prev_board, score)

    def erase_icon(self, board: Board, icon: Icon, icon_type: IconType) -> Score:
        ys, xs = np.where(board.board == icon)
        if ys.size == 0:
            return Score(0)
        count = 1
        erase_candidates = set()
        b = board.board
        score = Score(0)
        for y, x in zip(ys, xs):
            if x + 1 < b[0, :].size and b[y, x] == b[y, x+1]:
                count += 1
                erase_candidates.add((y, x))
                erase_candidates.add((y, x+1))
            if y + 1 < b[:, 0].size and b[y, x] == b[y+1, x]:
                count += 1
                erase_candidates.add((y, x))
                erase_candidates.add((y+1, x))
        if icon_type.value <= count:
            for y, x in erase_candidates:
                b[y, x] = Icon.Empty.value
        if icon_type == IconType.Normal:
            # TODO: 適当
            score += 100
        elif icon_type == IconType.Bomb:
            score += self.bomb_effect(board, icon)
        return score

    @staticmethod
    def bomb_effect(board: Board, icon: Icon) -> Score:
        assert(icon in IconTypeDict[IconType.Bomb])
        ys, xs = np.where(board.board == IconBombEraseDict[icon])
        if ys.size == 0:
            return Score(0)
        score = Score(0)
        for y, x in zip(ys, xs):
            board.board[y, x] = Icon.Empty.value
            # TODO: 適当
            score += 1000
        return score

    @staticmethod
    def add_generate_row(board: Board):
        new_row = board.random_row(rows=1)
        new_board = np.vstack((new_row, board.board))
        if (board.board[-1, :] == Icon.Empty.value).all():
            new_board = np.delete(new_board, -1, axis=0)
        board.replace(new_board)

    @property
    def is_alive(self) -> bool:
        return self.board.max_icon_height < self.rows

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

