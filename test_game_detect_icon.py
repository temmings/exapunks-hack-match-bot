from unittest import TestCase

from PIL import Image

from board import Board
from controller import Controller
from game import Game
from icon import Icon
from solve import Solver


class TestGameDetectIcon(TestCase):
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
