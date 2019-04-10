from unittest import TestCase

from PIL import Image

from board_state_detector import BoardStateDetector
from icon import Icon
from point import Point


class TestBoardStateDetector3(TestCase):
    def setUp(self):
        self.image = Image.open('images/board3.png')
        self.detector = BoardStateDetector(
            self.image, row_size=9, column_size=7, icon_size=Point(60, 60))

    def test_detect_column0(self):
        self.assertListEqual(
            [Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Purple, Icon.Purple, Icon.Green, Icon.Pink],
            self.detector.detect_column(self.image, 0))

    def test_detect_column1(self):
        self.assertListEqual(
            [Icon.Pink, Icon.Pink, Icon.Yellow, Icon.Yellow, Icon.Red, Icon.Purple, Icon.Purple],
            self.detector.detect_column(self.image, 1))

    def test_detect_column2(self):
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Red, Icon.Red, Icon.Pink, Icon.Red, Icon.Purple],
            self.detector.detect_column(self.image, 2))

    def test_detect_column3(self):
        self.assertListEqual(
            [Icon.Green, Icon.Red, Icon.BombRed, Icon.Green, Icon.Pink, Icon.Yellow, Icon.Pink],
            self.detector.detect_column(self.image, 3))

    def test_detect_column4(self):
        self.assertListEqual(
            [Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Green, Icon.Purple],
            self.detector.detect_column(self.image, 4))

    def test_detect_column5(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Purple, Icon.Yellow, Icon.Purple, Icon.Red, Icon.Purple, Icon.Green],
            self.detector.detect_column(self.image, 5))

    def test_detect_column6(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Yellow, Icon.Purple, Icon.Empty, Icon.Empty, Icon.Pink, Icon.Red],
            self.detector.detect_column(self.image, 6))

    def test_detect_column7(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Green, Icon.Empty, Icon.Empty, Icon.Empty, Icon.BombYellow],
            self.detector.detect_column(self.image, 7))
