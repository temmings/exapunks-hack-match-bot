from unittest import TestCase

from game import Game, Board, Character
from solver import HandmadeSolver


class TestHandmadeSolver(TestCase):
    def setUp(self):
        board = Board(10, 7)
        char = Character(board)
        self.game = Game(board, char)
        self.solver = HandmadeSolver(use_memo=False, store_memo=False)

    def test__solve_depth0(self):
        depth = 0
        prev_score = self.solver.eval(self.game)
        score, actions = self.solver._solve(self.game, depth, prev_score, [])
        self.assertGreaterEqual(score, prev_score)
        self.assertEqual(depth, len(actions))

    def test__solve_depth1(self):
        depth = 1
        prev_score = self.solver.eval(self.game)
        score, actions = self.solver._solve(self.game, depth, prev_score, [])
        self.assertGreaterEqual(score, prev_score)
        self.assertEqual(depth, len(actions))

    def test__solve_depth2(self):
        depth = 2
        prev_score = self.solver.eval(self.game)
        score, actions = self.solver._solve(self.game, depth, prev_score, [])
        self.assertGreaterEqual(score, prev_score)
        self.assertEqual(depth, len(actions))

    def test__solve_depth3(self):
        depth = 3
        prev_score = self.solver.eval(self.game)
        score, actions = self.solver._solve(self.game, depth, prev_score, [])
        self.assertGreaterEqual(score, prev_score)
        self.assertEqual(depth, len(actions))
