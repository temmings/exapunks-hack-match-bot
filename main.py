#!/usr/bin/env python
# coding: utf-8
#
import time
import win32gui

from board import Board
from character import Character
from win32controller import Win32Controller
from game import Game
from capture import Capture, WindowSize
from solver import RandomSolver

DEBUG_SAVE_BOARD = False
DEBUG_PRINT_BOARD = True
WINDOW_NAME = 'EXAPUNKS'


def main():
    capture = Capture(WINDOW_NAME)

    if capture.window_size == WindowSize.HD_PLUS:
        # (x0, y0, x1, y1)
        game_window_position = (370, 138, 790, 700)
        # score_window = (828, 251, 1237, 717)
    else:
        raise NotImplemented()

    board = Board(Game.ROWS, Game.COLUMNS)
    controller = Win32Controller(0.020)
    solver = RandomSolver()
    solver.enable_debug()
    char = Character(controller)
    game = Game(capture.crop(game_window_position), solver, board, char)
    game.enable_debug()

    hwnd = win32gui.FindWindowEx(0, 0, 0, WINDOW_NAME)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(1)
    controller.start()

    # main loop
    def proc():
        game_window = capture.crop(game_window_position)
        game.load_image(game_window)

        print('current frame: %d (frame rate: %d fps)' % (game.current_frame, game.FRAME_RATE))
        print('prev time: %f' % game.frame.prev_time)
        print('curr time: %f' % game.frame.current_time)

        if DEBUG_SAVE_BOARD:
            game_window.save('capture/game_frame_%05d.png' % game.current_frame)

        if DEBUG_PRINT_BOARD:
            print('current board:')
            game.board.print()
            print()

    game.main_loop(proc)
    exit(0)


if __name__ == '__main__':
    main()
