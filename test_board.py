from unittest import TestCase

import numpy as np

from board import Board
from icon import Icon


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board(3, 3)
        self.board.replace(np.asarray([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Pink.value, Icon.Green.value],
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
        ]))

    def test_swap_icon(self):
        self.board.swap_icon(1)
        self.assertEqual(np.asarray([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Purple.value, Icon.Green.value],
            [Icon.Red.value, Icon.Pink.value, Icon.BombPurple.value],
        ]).tolist(), self.board.board.tolist())

    def test_pop_icon(self):
        icon = self.board.pop_icon(1)
        self.assertEqual(Icon.Pink, icon)

        self.assertEqual(np.asarray([
            [Icon.Empty.value, Icon.Empty.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Empty.value, Icon.Green.value],
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
        ]).tolist(), self.board.board.tolist())

    def test_push_icon(self):
        self.board.push_icon(1, Icon.Green)
        self.assertEqual(np.asarray([
            [Icon.Empty.value, Icon.Green.value, Icon.Empty.value],
            [Icon.Yellow.value, Icon.Pink.value, Icon.Green.value],
            [Icon.Red.value, Icon.Purple.value, Icon.BombPurple.value],
        ]).tolist(), self.board.board.tolist())
