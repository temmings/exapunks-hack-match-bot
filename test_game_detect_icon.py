from unittest import TestCase

from PIL import Image

from game import Game
from icon import Icon


class TestGameDetectIcon(TestCase):
    def setUp(self):
        image = Image.open('test/board1.png')
        # noinspection PyTypeChecker
        self.game = Game(image, None, None, None)

    def test_icon_green(self):
        image = Image.open('test/icon_green.png')
        self.assertEqual(Icon.Green, self.game._detect_icon(image))

    def test_icon_pink(self):
        image = Image.open('test/icon_pink.png')
        self.assertEqual(Icon.Pink, self.game._detect_icon(image))

    def test_icon_purple(self):
        image = Image.open('test/icon_purple.png')
        self.assertEqual(Icon.Purple, self.game._detect_icon(image))

    def test_icon_red(self):
        image = Image.open('test/icon_red.png')
        self.assertEqual(Icon.Red, self.game._detect_icon(image))

    def test_icon_yellow(self):
        image = Image.open('test/icon_yellow.png')
        self.assertEqual(Icon.Yellow, self.game._detect_icon(image))

    def test_icon_bomb_green(self):
        image = Image.open('test/icon_bomb_green.png')
        self.assertEqual(Icon.BombGreen, self.game._detect_icon(image))

    def test_icon_bomb_purple(self):
        image = Image.open('test/icon_bomb_purple.png')
        self.assertEqual(Icon.BombPurple, self.game._detect_icon(image))

    def test_icon_bomb_yellow(self):
        image = Image.open('test/icon_bomb_yellow.png')
        self.assertEqual(Icon.BombYellow, self.game._detect_icon(image))

    def test_icon_bomb_red(self):
        image = Image.open('test/icon_bomb_red.png')
        self.assertEqual(Icon.BombRed, self.game._detect_icon(image))
