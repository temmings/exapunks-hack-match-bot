import operator
import numpy as np
from functools import reduce

from point import Point
from icon import Icon, IconToStringDict


class Board(object):
    """
    ゲームのボードを表現する。
    実際のゲーム画面とは上下が逆転した形で扱う。
    """
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.__board = self.__init_board(rows, columns)

    @staticmethod
    def __init_board(rows: int, columns: int) -> list:
        return np.full((rows, columns), Icon.Empty).tolist()[0:]

    def update(self, new_board: list):
        self.__board = new_board

    def print(self):
        for i, y in enumerate(reversed(self.__board), start=1):
            print('%d: ' % (self.rows - i), end='')
            for x in y:
                print(IconToStringDict[x], end='')
            print()

    def get_icon(self, x, y) -> Icon:
        return self.__board[y][x]

    def get_rows(self, amount):
        return self.__board[0:amount]

    def get_joined_rows(self, amount):
        return reduce(operator.add, self.__board[0:amount])

    def get_reversed_rows(self, amount):
        return reversed(self.__board)[0:amount]

    def get_joined_reversed_rows(self, amount):
        return reduce(operator.add, reversed(self.__board)[0:amount])

    def get_positions(self, icon: Icon) -> list:
        result = []
        for y, row in enumerate(self.__board):
            for x, item in enumerate(row):
                if item == icon:
                    result.append(Point(x, y))
        return result

    def get_surface(self) -> list:
        result = [Icon.Empty] * self.columns
        for i in range(self.columns):
            for row in self.__board:
                if row[i] != Icon.Empty:
                    result[i] = row[i]
                    break
        return result
