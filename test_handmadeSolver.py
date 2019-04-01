from unittest import TestCase

from board import Board
from icon import Icon
from point import Point
from solver import HandmadeSolver


class TestHandmadeSolver(TestCase):
    def setUp(self):
        self.solver = HandmadeSolver()
        self.board = Board(2, 2)

    def test_find_bomb_none(self):
        self.board.update([
            [Icon.Yellow, Icon.Green],
            [Icon.BombYellow, Icon.Red],
        ])
        self.assertEquals(
            (None, []),
            self.solver.find_bomb(self.board))

    def test_find_bomb_found(self):
        self.board.update([
            [Icon.Yellow, Icon.BombYellow],
            [Icon.BombYellow, Icon.Red],
        ])
        self.assertEquals(
            (Icon.BombYellow, [Point(1, 0), Point(0, 1)]),
            self.solver.find_bomb(self.board))

