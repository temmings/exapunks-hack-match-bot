#!/usr/bin/env python
# coding: utf-8
#
import time
from enum import Enum

import win32gui

from board import Board
from board_state_detector import BoardStateDetector
from character import Character
from void_controller import VoidController
from game import Game
from win32controller import Win32Controller, InputIntervalSecond
from capture import WindowSize
from win32capture import Win32Capture
from handmade_solver import HandmadeSolver


class Mode(Enum):
    RealGame = 1
    VirtualGame = 2


MODE = Mode.RealGame
DEBUG_SAVE_BOARD = False
DEBUG_PRINT_BOARD = True
WINDOW_NAME = 'EXAPUNKS'
INPUT_INTERVAL_SECOND = InputIntervalSecond(0.050)


def main():
    rows, columns = 9, 7

    board = Board(rows, columns)
    controller = Win32Controller(INPUT_INTERVAL_SECOND) if MODE == Mode.RealGame else VoidController()
    char = Character(board, controller=controller)
    char.enable_debug()
    game = Game(board, char)
    game.enable_debug()

    solver = HandmadeSolver()
    #solver = RandomSolver()
    solver.enable_debug()

    if MODE == Mode.RealGame:
        capture = Win32Capture(WINDOW_NAME)

        if capture.window_size == WindowSize.HD_PLUS:
            # (x0, y0, x1, y1)
            # (540 * 420)
            game_window_position = (370, 138, 790, 678)
            # score_window = (828, 251, 1237, 717)
        else:
            raise NotImplemented()

        game_window = capture.crop(game_window_position)
        detector = BoardStateDetector(game_window, rows, columns)
        detector.enable_debug()

        hwnd = win32gui.FindWindowEx(0, 0, 0, WINDOW_NAME)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        controller.start()

    # main loop
    def proc():
        if MODE == Mode.RealGame:
            # ボードの状態を画面から判定し、更新する
            window = capture.crop(game_window_position)
            if DEBUG_SAVE_BOARD:
                window.save('capture/frame_%05d.png' % game.current_frame)
            new_board = detector.get_board_from_image(window)
            board.replace(new_board)

        solver.solve(game)

    game.main_loop(proc)

    exit(0)


if __name__ == '__main__':
    main()
