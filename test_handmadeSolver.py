from unittest import TestCase

from board import Board
from icon import Icon
from point import Point
from solver import HandmadeSolver


class TestHandmadeSolver(TestCase):
    def setUp(self):
        self.solver = HandmadeSolver()
        self.board = Board(6, 2)

    def test_find_bomb_none(self):
        self.board.update([
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.BombYellow, Icon.Red],
            [Icon.Yellow, Icon.Green],
        ])
        self.assertEqual(
            (None, []),
            self.solver.find_bomb(self.board))

    def test_find_bomb_found(self):
        self.board.update([
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.Empty, Icon.Empty],
            [Icon.BombYellow, Icon.Red],
            [Icon.Yellow, Icon.BombYellow],
        ])
        self.assertEqual(
            (Icon.BombYellow, [Point(0, 4), Point(1, 5)]),
            self.solver.find_bomb(self.board))

