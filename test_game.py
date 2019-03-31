import unittest
from unittest import TestCase

from PIL import Image

from board import Board
from controller import Controller
from game import Game
from icon import Icon
from solve import Solver


class TestGameIcon(TestCase):
    def setUp(self):
        self.board = Board(1, 1)
        self.controller = Controller()
        self.solver = Solver(self.board, self.controller)

    def test_icon_green(self):
        image = Image.open('test/icon_green.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.Green, game._detect_icon(image))

    def test_icon_pink(self):
        image = Image.open('test/icon_pink.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.Pink, game._detect_icon(image))

    def test_icon_purple(self):
        image = Image.open('test/icon_purple.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.Purple, game._detect_icon(image))

    def test_icon_red(self):
        image = Image.open('test/icon_red.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.Red, game._detect_icon(image))

    def test_icon_yellow(self):
        image = Image.open('test/icon_yellow.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.Yellow, game._detect_icon(image))

    def test_icon_bomb_green(self):
        image = Image.open('test/icon_bomb_green.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.BombGreen, game._detect_icon(image))

    def test_icon_bomb_purple(self):
        image = Image.open('test/icon_bomb_purple.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.BombPurple, game._detect_icon(image))

    def test_icon_bomb_yellow(self):
        image = Image.open('test/icon_bomb_yellow.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.BombYellow, game._detect_icon(image))

    def test_icon_bomb_red(self):
        image = Image.open('test/icon_bomb_red.png')
        game = Game(image, self.solver, self.board)
        self.assertEqual(Icon.BombRed, game._detect_icon(image))


@unittest.skip("not implement")
class TestGameBoard1(TestCase):
    def setUp(self):
        self.image = Image.open('test/board1.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, 7)
        self.assertListEqual(
            [Icon.Green, Icon.Red, Icon.Green, Icon.Green, Icon.Red, Icon.BombPurple, Icon.Yellow],
            columns)

    def test_detect_column1(self):
        columns = self.game._detect_column(self.image, 1, 7)
        self.assertListEqual(
            [Icon.Green, Icon.Pink, Icon.Purple, Icon.Green, Icon.Pink, Icon.Pink, Icon.Purple],
            columns)

    def test_detect_column2(self):
        columns = self.game._detect_column(self.image, 2, 7)
        self.assertListEqual(
            [Icon.Yellow, Icon.Purple, Icon.Red, Icon.Purple, Icon.Pink, Icon.Red, Icon.Purple],
            columns)

    def test_detect_column3(self):
        columns = self.game._detect_column(self.image, 3, 7)
        self.assertListEqual(
            [Icon.Yellow, Icon.Green, Icon.Yellow, Icon.Green, Icon.Green, Icon.Pink, Icon.Purple],
            columns)

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, 7)
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink],
            columns)


@unittest.skip("not implement")
class TestGameBoard2(TestCase):
    def setUp(self):
        self.image = Image.open('test/board2.png')
        board = Board(Game.ROWS, Game.COLUMNS)
        controller = Controller()
        solver = Solver(board, controller)
        self.game = Game(self.image, solver, board)

    def test_detect_column0(self):
        columns = self.game._detect_column(self.image, 0, 7)
        self.assertListEqual(
            [Icon.Green, Icon.Red, Icon.Green, Icon.Green, Icon.Red, Icon.BombPurple, Icon.Yellow],
            columns)

    def test_detect_column4(self):
        columns = self.game._detect_column(self.image, 4, 7)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty],
            columns)

    def test_detect_column5(self):
        columns = self.game._detect_column(self.image, 5, 7)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty],
            columns)
