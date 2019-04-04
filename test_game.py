from unittest import TestCase

import numpy as np

from board import Board
from character import Character
from game import Game
from icon import Icon


class TestGame(TestCase):
    def setUp(self):
        board = (Board(row_size=5, column_size=3))
        board.replace(np.array([
            [Icon.Green.value, Icon.Green.value, Icon.Green.value],
            [Icon.BombRed.value, Icon.Green.value, Icon.Purple.value],
            [Icon.Red.value, Icon.BombRed.value, Icon.Yellow.value],
            [Icon.Red.value, Icon.Pink.value, Icon.Yellow.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]))
        self.game = Game(board, Character(board))

    def test_add_generate_row(self):
        self.game.add_generate_row(self.game.board)
        add_row = self.game.board.board[0, ]
        self.assertTrue((Icon.Empty.value != add_row).all())
        exist_row = self.game.board.board[1:, ]
        self.assertEqual(np.array([
            [Icon.Green.value, Icon.Green.value, Icon.Green.value],
            [Icon.BombRed.value, Icon.Green.value, Icon.Purple.value],
            [Icon.Red.value, Icon.BombRed.value, Icon.Yellow.value],
            [Icon.Red.value, Icon.Pink.value, Icon.Yellow.value],
        ]).tolist(), exist_row.tolist())

    def test_is_alive(self):
        self.game.add_generate_row(self.game.board)
        self.assertTrue(self.game.is_alive)
        self.game.add_generate_row(self.game.board)
        self.assertFalse(self.game.is_alive)

    def test_effect(self):
        score = self.game.effect(self.game.board)
        self.assertEqual([
            [Icon.Empty.value, Icon.Pink.value, Icon.Purple.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Yellow.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Yellow.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ], self.game.board.board.tolist())
        self.assertGreater(score, 0)
