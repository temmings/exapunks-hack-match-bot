from unittest import TestCase

from board import Board


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board(2, 3)
