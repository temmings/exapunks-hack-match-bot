from unittest import TestCase

from PIL import Image

from board_state_detector import BoardStateDetector
from game import Game
from icon import Icon


class TestBoardImageDetectorDetectIcon(TestCase):
    def setUp(self):
        image = Image.open('test/board1.png')
        self.detector = BoardStateDetector(image, row_size=Game.ROWS, column_size=Game.COLUMNS)

    def test_icon_green(self):
        image = Image.open('test/icon_green.png')
        self.assertEqual(Icon.Green, self.detector._detect_icon(image))

    def test_icon_pink(self):
        image = Image.open('test/icon_pink.png')
        self.assertEqual(Icon.Pink, self.detector._detect_icon(image))

    def test_icon_purple(self):
        image = Image.open('test/icon_purple.png')
        self.assertEqual(Icon.Purple, self.detector._detect_icon(image))

    def test_icon_red(self):
        image = Image.open('test/icon_red.png')
        self.assertEqual(Icon.Red, self.detector._detect_icon(image))

    def test_icon_yellow(self):
        image = Image.open('test/icon_yellow.png')
        self.assertEqual(Icon.Yellow, self.detector._detect_icon(image))

    def test_icon_bomb_green(self):
        image = Image.open('test/icon_bomb_green.png')
        self.assertEqual(Icon.BombGreen, self.detector._detect_icon(image))

    def test_icon_bomb_purple(self):
        image = Image.open('test/icon_bomb_purple.png')
        self.assertEqual(Icon.BombPurple, self.detector._detect_icon(image))

    def test_icon_bomb_yellow(self):
        image = Image.open('test/icon_bomb_yellow.png')
        self.assertEqual(Icon.BombYellow, self.detector._detect_icon(image))

    def test_icon_bomb_red(self):
        image = Image.open('test/icon_bomb_red.png')
        self.assertEqual(Icon.BombRed, self.detector._detect_icon(image))
