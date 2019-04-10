#!/usr/bin/env python
# coding: utf-8
#
import time

from game import Game, Board, Character, Mode
from solver import HandmadeSolver
from controller import VoidController, Win32Controller, InputIntervalSecond
from point import Point

#MODE = Mode.RealGame
MODE = Mode.VirtualGame
DEBUG_SAVE_BOARD = True
WINDOW_NAME = 'EXAPUNKS'
INPUT_INTERVAL_SECOND = InputIntervalSecond(0.080)


def main():
    rows, columns = 10, 7

    board = Board(rows, columns)
    if MODE == Mode.RealGame:
        controller = Win32Controller(INPUT_INTERVAL_SECOND)
    else:
        controller = VoidController()
    char = Character(board, controller=controller)
    char.enable_trace()
    game = Game(board, char)
    game.enable_trace()

    solver = HandmadeSolver()
    #solver = RandomSolver()
    #solver.enable_trace()

    if MODE == Mode.RealGame:
        import win32gui
        from capture import WindowSize, Win32Capture, BoardStateDetector

        capture = Win32Capture(WINDOW_NAME)

        if capture.window_size == WindowSize.HD_PLUS:
            icon_size = Point(60, 60)
            start_point = Point(370, 138)
            x0 = start_point.x
            y0 = start_point.y
            x1 = x0 + icon_size.x * columns
            y1 = y0 + icon_size.y * rows
            game_window_position = (x0, y0, x1, y1)
            # score_window = (828, 251, 1237, 717)
        else:
            raise NotImplemented()

        game_window = capture.crop(game_window_position)
        detector = BoardStateDetector(game_window, rows, columns, icon_size)
        if DEBUG_SAVE_BOARD:
            detector.enable_debug()

        hwnd = win32gui.FindWindowEx(0, 0, 0, WINDOW_NAME)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        controller.start()

    # main loop
    def proc(g: Game):
        if MODE == Mode.RealGame:
            # ボードの状態を画面から判定し、更新する
            window = capture.crop(game_window_position)
            new_board = detector.get_board_from_image(window)
            g.board.replace(new_board)
            if DEBUG_SAVE_BOARD:
                window.save('tmp/frame_%05d.png' % g.current_frame)
                with open('tmp/frame_%05d.txt' % g.current_frame, 'w') as f:
                    f.write(g.board.serialize())
        solver.solve(g)

    game.main_loop(proc)

    exit(0)


if __name__ == '__main__':
    main()
