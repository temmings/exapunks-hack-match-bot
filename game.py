import time
import typing

import numpy as np

from board import Board
from character import Character
from frame_counter import FrameCounter
from icon import Icon, IconType, IconTypeDict, IconBombEraseDict
from mode import Mode

Score = typing.NewType('Score', int)


class Game(object):
    FRAME_RATE = 15
    FRAME_SECOND = 1.0 / FRAME_RATE
    SCORE_BASE = 100

    def __init__(self, board: Board, char: Character):
        self.debug = False
        self.frame = FrameCounter()
        self.board = board
        self.char = char
        self.score = 0
        self.rows, self.columns = board.row_size, board.column_size
        self.__is_alive = True

    def main_loop(self, callback: typing.Callable, mode: Mode):
        while self.is_alive:
            # 1秒毎に行が追加される
            if mode == Mode.VirtualGame:
                if 0 == self.current_frame % self.FRAME_RATE:
                    self.add_generate_row(self.board)
                self.score += self.effect(self.board)
            self.trace('process time: %f' % self.process_time, end=', ')
            self.trace('game frame: %d' % self.frame.current, end=', ')
            self.trace('game score: %d' % self.score)
            callback(self)
            print()
            self.trace('game board:')
            self.board.print()
            print()
            self.frame.count_up()
            if self.frame.process_time < self.FRAME_SECOND:
                time.sleep(self.FRAME_SECOND - self.process_time)
            self.__is_alive = self.__is_alive and \
                              (self.board.board != Icon.Empty.value).any()
        self.trace('game over.')

    def effect(self, board: Board, prev_board=None, multiply=1, score=Score(0)) -> Score:
        if prev_board is not None and (board.board == prev_board).all():
            return score
        prev_board = np.array(board.board, copy=True)
        for icon_type in IconType:
            for icon in IconTypeDict[icon_type]:
                score += self.erase_icon(board, icon, icon_type) * multiply
        packed_bord = board.pack(board.board)
        board.replace(packed_bord)
        return self.effect(board, prev_board, multiply=multiply+1, score=score)

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
                score += self.SCORE_BASE * count
            elif icon_type == IconType.Bomb:
                score += self.bomb_effect(board, icon)
        return score

    def bomb_effect(self, board: Board, icon: Icon) -> Score:
        assert(icon in IconTypeDict[IconType.Bomb])
        ys, xs = np.where(board.board == IconBombEraseDict[icon])
        if ys.size == 0:
            return Score(0)
        score = Score(0)
        for y, x in zip(ys, xs):
            board.board[y, x] = Icon.Empty.value
            score += self.SCORE_BASE
        return score

    def add_generate_row(self, board: Board):
        new_row = board.random_row(rows=1)
        new_board = np.vstack((new_row, board.board))
        if (board.board[-1, :] == Icon.Empty.value).all():
            new_board = np.delete(new_board, -1, axis=0)
            board.replace(new_board)
        else:
            self.__is_alive = False

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    def trace(self, msg, end='\n'):
        if self.debug:
            print(msg, end=end)

    def enable_debug(self):
        self.debug = True

    @property
    def current_frame(self) -> int:
        return self.frame.current

    @property
    def process_time(self) -> int:
        return self.frame.process_time

