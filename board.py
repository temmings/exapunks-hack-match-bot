import operator
from functools import reduce

from point import Point
from icon import Icon


class Board(object):
    """
    ゲームのボードを表現する。
    """
    def __init__(self, row_number: int, column_number: int):
        self.rows = self.init_board(row_number, column_number)

    @staticmethod
    def init_board(row_number: int, column_number: int) -> list:
        column = [Icon.Empty for _ in range(0, column_number)]
        rows = [column for _ in range(0, row_number)]
        return rows

    def update(self, rows: list):
        self.rows = rows

    def print(self):
        for i, y in enumerate(self.rows):
            print('%d: ' % i, end='')
            for x in y:
                print(x.value, end='')
            print()

    def get_icon(self, x, y) -> Icon:
        return self.rows[y][x]

    def get_rows(self, amount):
        return self.rows[0:amount]

    def get_joined_rows(self, amount):
        return reduce(operator.add, self.rows[0:amount])

    def get_reversed_rows(self, amount):
        return reversed(self.rows)[0:amount]

    def get_joined_reversed_rows(self, amount):
        return reduce(operator.add, reversed(self.rows)[0:amount])

    def get_positions(self, icon: Icon) -> list:
        result = []
        for y, row in enumerate(self.rows):
            for x, item in enumerate(row):
                if item == icon:
                    result.append(Point(x, y))
        return result

