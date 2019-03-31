from unittest import TestCase

from PIL import Image

from board import Board
from controller import Controller
from game import Game
from icon import Icon
from solve import Solver


class TestGameDetectBoard2(TestCase):
    def setUp(self):
        self.image = Image.open('test/board2.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink], columns)

    def test_detect_column1(self):
        columns = self.game._detect_column(self.image, 1, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Purple, Icon.Green, Icon.Red, Icon.Yellow, Icon.Red, Icon.Pink, Icon.Yellow], columns)

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty], columns)

    def test_detect_column5(self):
        columns = self.game._detect_column(self.image, 5, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty], columns)
