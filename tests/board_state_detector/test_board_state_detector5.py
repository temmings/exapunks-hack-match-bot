from unittest import TestCase

from PIL import Image

from capture import BoardStateDetector
from game import Icon
from point import Point


class TestBoardStateDetector5(TestCase):
    def setUp(self):
        self.image = Image.open('images/board5.png')
        self.detector = BoardStateDetector(
            self.image, row_size=9, column_size=7, icon_size=Point(60, 60))

    def test_detect_column0(self):
        self.assertListEqual(
            [Icon.Green, Icon.Red, Icon.Red, Icon.Purple, Icon.Purple, Icon.Green, Icon.Red],
            self.detector.detect_column(self.image, 0))

    def test_detect_column1(self):
        self.assertListEqual(
            [Icon.Red, Icon.Pink, Icon.Yellow, Icon.Yellow, Icon.Green, Icon.Pink, Icon.Pink],
            self.detector.detect_column(self.image, 1))

    def test_detect_column2(self):
        self.assertListEqual(
            [Icon.Yellow, Icon.Green, Icon.Green, Icon.Yellow, Icon.Pink, Icon.Purple, Icon.Purple],
            self.detector.detect_column(self.image, 2))

    def test_detect_column3(self):
        self.assertListEqual(
            [Icon.Yellow, Icon.Pink, Icon.Green, Icon.Pink, Icon.Pink, Icon.Purple, Icon.Red],
            self.detector.detect_column(self.image, 3))

    def test_detect_column4(self):
        self.assertListEqual(
            [Icon.Pink, Icon.Yellow, Icon.Yellow, Icon.Green, Icon.Yellow, Icon.Red, Icon.Yellow],
            self.detector.detect_column(self.image, 4))

    def test_detect_column5(self):
        self.assertListEqual(
            [Icon.Empty, Icon.BombGreen, Icon.Pink, Icon.Green, Icon.Green, Icon.Pink, Icon.Purple],
            self.detector.detect_column(self.image, 5))

    def test_detect_column6(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Green, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Purple],
            self.detector.detect_column(self.image, 6))

    def test_detect_column7(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Red, Icon.Empty, Icon.Empty, Icon.Purple, Icon.Empty],
            self.detector.detect_column(self.image, 7))

    def test_detect_column8(self):
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Red, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty],
            self.detector.detect_column(self.image, 8))
