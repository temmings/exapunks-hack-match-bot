from unittest import TestCase

from PIL import Image

from board_state_detector import BoardStateDetector
from icon import Icon
from point import Point


class TestBoardStateDetectorDetectIcon(TestCase):
    def setUp(self):
        image = Image.open('images/board1.png')
        self.detector = BoardStateDetector(
            image, row_size=9, column_size=7, icon_size=Point(60, 60))

    def test_icon_green(self):
        image = Image.open('images/icon_green.png')
        self.assertEqual(Icon.Green, self.detector.detect_icon(image))

    def test_icon_pink(self):
        image = Image.open('images/icon_pink.png')
        self.assertEqual(Icon.Pink, self.detector.detect_icon(image))

    def test_icon_purple(self):
        image = Image.open('images/icon_purple.png')
        self.assertEqual(Icon.Purple, self.detector.detect_icon(image))

    def test_icon_red(self):
        image = Image.open('images/icon_red.png')
        self.assertEqual(Icon.Red, self.detector.detect_icon(image))

    def test_icon_yellow(self):
        image = Image.open('images/icon_yellow.png')
        self.assertEqual(Icon.Yellow, self.detector.detect_icon(image))

    def test_icon_bomb_green(self):
        image = Image.open('images/icon_bomb_green.png')
        self.assertEqual(Icon.BombGreen, self.detector.detect_icon(image))

    def test_icon_bomb_purple(self):
        image = Image.open('images/icon_bomb_purple.png')
        self.assertEqual(Icon.BombPurple, self.detector.detect_icon(image))

    def test_icon_bomb_yellow(self):
        image = Image.open('images/icon_bomb_yellow.png')
        self.assertEqual(Icon.BombYellow, self.detector.detect_icon(image))

    def test_icon_bomb_red(self):
        image = Image.open('images/icon_bomb_red.png')
        self.assertEqual(Icon.BombRed, self.detector.detect_icon(image))
