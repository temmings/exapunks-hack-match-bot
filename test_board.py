from unittest import TestCase

import numpy as np

from board import Board
from icon import Icon


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board(row_size=4, column_size=3)
        self.board.replace(np.array([
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
            [Icon.Yellow.value, Icon.Pink.value, Icon.Green.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]))

    def test_swap_icon(self):
        self.board.swap_icon(1)
        self.assertEqual(np.array([
            [Icon.Red.value, Icon.Pink.value, Icon.BombPurple.value],
            [Icon.Yellow.value, Icon.Purple.value, Icon.Green.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]).tolist(), self.board.board.tolist())

    def test_pop_icon(self):
        icon = self.board.pop_icon(1)
        self.assertEqual(Icon.Pink, icon)

        self.assertEqual(np.array([
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Green.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]).tolist(), self.board.board.tolist())

    def test_push_icon(self):
        self.board.push_icon(1, Icon.Green)
        self.assertEqual(np.array([
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
            [Icon.Yellow.value, Icon.Pink.value, Icon.Green.value],
            [Icon.Empty.value, Icon.Green.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]).tolist(), self.board.board.tolist())

    def test_max_icon_height(self):
        self.assertEqual(1, self.board.max_icon_height)
        self.board.replace(np.array([
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
            [Icon.Yellow.value, Icon.Pink.value, Icon.Green.value],
            [Icon.Empty.value, Icon.Green.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]))
        self.assertEqual(2, self.board.max_icon_height)

    def test_get_positions(self):
        self.assertEqual(np.array([
                [False, False, False],
                [False, False, True],
                [False, False, False],
                [False, False, False],
            ]).tolist(),
            self.board.get_positions(Icon.Green).tolist())

        self.assertEqual(np.array([
                [False, False, False],
                [True,  False, False],
                [False, False, False],
                [False, False, False],
            ]).tolist(),
            self.board.get_positions(Icon.Yellow).tolist())

    def test_get_icon(self):
        self.assertEqual(Icon.Pink, self.board.get_icon(1, 1))
        self.assertEqual(Icon.Empty, self.board.get_icon(2, 2))

    def test_empty_row(self):
        self.assertEqual([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ], self.board.empty_row(rows=1).tolist())

        self.assertEqual([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ], self.board.empty_row(rows=2).tolist())

    def test_random_row(self):
        self.assertTrue((np.array([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]) != self.board.random_row(rows=1)).all())

        self.assertTrue((np.array([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]) != self.board.random_row(rows=2)).all())

    def test_pack(self):
        self.board.replace(np.array([
            [Icon.Red.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Pink.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Empty.value],
        ]))

        self.assertEqual(np.array([
            [Icon.Red.value, Icon.Empty.value, Icon.Pink.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
        ]).tolist(), self.board.pack(self.board.board).tolist())
