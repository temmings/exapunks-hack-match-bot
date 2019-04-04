from unittest import TestCase

from PIL import Image

from board_state_detector import BoardStateDetector
from icon import Icon


class TestBoardStateDetector2(TestCase):
    def setUp(self):
        self.image = Image.open('test/board2.png')
        self.detector = BoardStateDetector(self.image, row_size=9, column_size=7)

    def test_detect_column0(self):
        columns = self.detector._detect_column(self.image, 0)
        self.assertListEqual(
            [Icon.Red, Icon.Yellow, Icon.Purple, Icon.Yellow, Icon.Red, Icon.Green, Icon.Pink], columns)

    def test_detect_column1(self):
        columns = self.detector._detect_column(self.image, 1)
        self.assertListEqual(
            [Icon.Purple, Icon.Green, Icon.Red, Icon.Yellow, Icon.Red, Icon.Pink, Icon.Yellow], columns)

    def test_detect_column4(self):
        columns = self.detector._detect_column(self.image, 4)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty], columns)

    def test_detect_column5(self):
        columns = self.detector._detect_column(self.image, 5)
        self.assertListEqual(
            [Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty, Icon.Empty], columns)
