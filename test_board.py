from unittest import TestCase

from board import Board
from icon import Icon


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board(2, 3)

    def test_get_surface(self):
        self.board.update([
            [Icon.Red, Icon.Empty, Icon.Pink],
            [Icon.Green, Icon.Yellow, Icon.BombYellow],
        ])
        self.assertEqual(
            [Icon.Red, Icon.Yellow, Icon.Pink],
            self.board.get_surface()
        )

    def test_get_surface_with_empty(self):
        self.board.update([
            [Icon.Red, Icon.Empty, Icon.Pink],
            [Icon.Green, Icon.Empty, Icon.BombYellow],
        ])
        self.assertEqual(
            [Icon.Red, Icon.Empty, Icon.Pink],
            self.board.get_surface()
        )
