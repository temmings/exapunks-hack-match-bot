from unittest import TestCase

from PIL import Image

from board import Board
from controller import Controller
from game import Game
from icon import Icon
from solve import Solver


class TestGame(TestCase):
    def setUp(self):
        self.image = Image.open('test/board1.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, 7)
        self.assertListEqual(columns,
                             [Icon.Green, Icon.Red, Icon.Green, Icon.Green, Icon.Red, Icon.BombPurple, Icon.Yellow])

    def test_detect_column1(self):
        columns = self.game._detect_column(self.image, 1, 7)
        self.assertListEqual(columns,
                             [Icon.Green, Icon.Pink, Icon.Purple, Icon.Green, Icon.Pink, Icon.Pink, Icon.Purple])

    def test_detect_column2(self):
        columns = self.game._detect_column(self.image, 2, 7)
        self.assertListEqual(columns,
                             [Icon.Yellow, Icon.Purple, Icon.Red, Icon.Purple, Icon.Pink, Icon.Red, Icon.Purple])

    def test_detect_column3(self):
        columns = self.game._detect_column(self.image, 3, 7)
        self.assertListEqual(columns,
                             [Icon.Yellow, Icon.Green, Icon.Yellow, Icon.Green, Icon.Green, Icon.Pink, Icon.Purple])

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, 7)
        self.assertListEqual(columns, [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink]
                             )

    def tearDown(self):
        self.image.close()


class TestGame2(TestCase):
    def setUp(self):
        self.image = Image.open('test/board2.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, 7)
        self.assertListEqual(columns,
                             [Icon.Green, Icon.Red, Icon.Green, Icon.Green, Icon.Red, Icon.Unknown, Icon.Yellow])

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, 7)
        self.assertListEqual(columns,
                             [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty])

    def test_detect_column5(self):
        columns = self.game._detect_column(self.image, 5, 7)
        self.assertListEqual(columns,
                             [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty])

    def tearDown(self):
        self.image.close()
