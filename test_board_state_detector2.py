from unittest import TestCase

from PIL import Image

from board_state_detector import BoardStateDetector
from icon import Icon
from point import Point


class TestBoardStateDetector2(TestCase):
    def setUp(self):
        self.image = Image.open('test/board2.png')
        self.detector = BoardStateDetector(
            self.image, row_size=9, column_size=7, icon_size=Point(60, 60))

    def test_detect_column0(self):
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink],
            self.detector.detect_column(self.image, 0))

    def test_detect_column1(self):
        self.assertListEqual(
            [Icon.Purple, Icon.Green, Icon.Red, Icon.Yellow, Icon.Red, Icon.Pink, Icon.Yellow],
            self.detector.detect_column(self.image, 1))

    def test_detect_column2(self):
        self.assertListEqual(
            [Icon.Yellow, Icon.Purple, Icon.Green, Icon.Pink, Icon.Pink, Icon.Red, Icon.BombPurple],
            self.detector.detect_column(self.image, 2))

    def test_detect_column3(self):
        self.assertListEqual(
            [Icon.Pink, Icon.Green, Icon.Red, Icon.Yellow, Icon.Purple, Icon.Purple, Icon.Purple],
            self.detector.detect_column(self.image, 3))

    def test_detect_column45678(self):
        empty_column = [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty]
        self.assertListEqual(empty_column, self.detector.detect_column(self.image, 4))
        self.assertListEqual(empty_column, self.detector.detect_column(self.image, 5))
        self.assertListEqual(empty_column, self.detector.detect_column(self.image, 6))
        self.assertListEqual(empty_column, self.detector.detect_column(self.image, 7))
        self.assertListEqual(empty_column, self.detector.detect_column(self.image, 8))
