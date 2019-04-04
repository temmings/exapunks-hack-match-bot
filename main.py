#!/usr/bin/env python
# coding: utf-8
#
import time
import win32gui

from board import Board
from board_state_detector import BoardStateDetector
from character import Character
from win32controller import Win32Controller, InputIntervalSecond
from game import Game
from capture import WindowSize
from win32capture import Win32Capture
from solver import HandmadeSolver

DEBUG_SAVE_BOARD = False
DEBUG_PRINT_BOARD = True
WINDOW_NAME = 'EXAPUNKS'
INPUT_INTERVAL_SECOND = InputIntervalSecond(0.020)


def main():
    capture = Win32Capture(WINDOW_NAME)

    if capture.window_size == WindowSize.HD_PLUS:
        # (x0, y0, x1, y1)
        # (540 * 420)
        game_window_position = (370, 138, 790, 678)
        # score_window = (828, 251, 1237, 717)
    else:
        raise NotImplemented()
    
    rows, columns = 9, 7

    board = Board(rows, columns)
    char = Character(board)
    game = Game(board, char)
    game.enable_debug()

    #solver = RandomSolver()
    solver = HandmadeSolver()
    solver.enable_debug()

    game_window = capture.crop(game_window_position)
    detector = BoardStateDetector(game_window, rows, columns)
    detector.enable_debug()

    hwnd = win32gui.FindWindowEx(0, 0, 0, WINDOW_NAME)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(1)
    controller = Win32Controller(INPUT_INTERVAL_SECOND)
    controller.start()

    # main loop
    def proc():
        print('current frame: %d' % game.current_frame)
        print('process time: %f' % game.process_time)

        # 10フレーム毎にボードの状態を判定し、更新
        if 0 == game.current_frame % 10:
            window = capture.crop(game_window_position)
            if DEBUG_SAVE_BOARD:
                window.save('capture/frame_%05d.png' % game.current_frame)
            new_board = detector.get_board_from_image(window)
            game.board.replace(new_board)

        solver.solve(game)

        if DEBUG_PRINT_BOARD:
            print('current board:')
            game.board.print()
            print()

    game.main_loop(proc)

    exit(0)


if __name__ == '__main__':
    main()
