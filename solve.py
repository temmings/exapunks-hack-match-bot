from board import Board
from controller import Controller


class Solver(object):
    def __init__(self, board: Board, controller: Controller):
        self.board = board
        self.controller = controller
