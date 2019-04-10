from unittest import TestCase

from game import Board
from solver import HandmadeSolver


class TestHandmadeSolver(TestCase):
    def setUp(self):
        self.solver = HandmadeSolver()
        self.board = Board(6, 2)
