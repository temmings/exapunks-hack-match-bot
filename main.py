import win32gui

from board import Board
from controller import Controller
from game import Game
from capture import Capture, WindowSize
from solve import Solver

DEBUG = True
WINDOW_NAME = 'EXAPUNKS'


def main():
    capture = Capture(WINDOW_NAME)
    hwnd = win32gui.FindWindowEx(0, 0, 0, WINDOW_NAME)
    win32gui.SetForegroundWindow(hwnd)

    if capture.window_size == WindowSize.HD_PLUS:
        # (x0, y0, x1, y1)
        game_window = (370, 138, 790, 700)
        # score_window = (828, 251, 1237, 717)
    else:
        raise NotImplemented()

    board = Board(Game.ROWS, Game.COLUMNS)
    controller = Controller()
    solver = Solver(board, controller)
    game = Game(capture.crop(game_window), solver, board)
    game.enable_debug()
    controller.start()

    # main loop
    def proc():
        im = capture.crop(game_window)
        game.load_image(im)
        if DEBUG:
            im.save('capture/game_frame_%05d.png' % game.current_frame)
            print('current frame: %d' % game.current_frame)
            print('current board:')
            game.board.print_board()
            print()

    game.main_loop(proc)
    exit(0)


if __name__ == '__main__':
    main()
