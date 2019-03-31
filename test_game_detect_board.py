from unittest import TestCase

from PIL import Image

from board import Board
from controller import Controller
from game import Game
from icon import Icon
from solve import Solver

class TestGameDetectBoard(TestCase):
    def setUp(self):
        self.image = Image.open('test/board1.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Green, Icon.Red, Icon.Green, Icon.Green, Icon.Red, Icon.BombPurple, Icon.Yellow], columns)

    def test_detect_column1(self):
        columns = self.game._detect_column(self.image, 1, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Green, Icon.Pink, Icon.Purple, Icon.Green, Icon.Pink, Icon.Pink, Icon.Purple], columns)

    def test_detect_column2(self):
        columns = self.game._detect_column(self.image, 2, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Yellow, Icon.Purple, Icon.Red, Icon.Purple, Icon.Pink, Icon.Red, Icon.Purple], columns)

    def test_detect_column3(self):
        columns = self.game._detect_column(self.image, 3, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Yellow, Icon.Green, Icon.Yellow, Icon.Green, Icon.Green, Icon.Pink, Icon.Purple], columns)

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, self.game.COLUMNS)
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink], columns)
