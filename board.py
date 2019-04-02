import numpy as np

from icon import Icon


class Board(object):
    """
    ゲームのボードを表現する。
    実際のゲーム画面とは上下が逆転した形で扱う。
    """

    def __init__(self, row_size: int, column_size: int):
        self.row_size = row_size
        self.column_size = column_size
        self.__board: np.ndarray = self.__init_board(row_size, column_size)

    @staticmethod
    def __init_board(row_size: int, column_size: int) -> np.ndarray:
        return np.full((row_size, column_size), Icon.Empty.value, dtype=int)

    @property
    def board(self) -> np.ndarray:
        return self.__board

    def replace(self, new_board: np.ndarray):
        self.__board = new_board

    def get_icon(self, x, y) -> Icon:
        return Icon(self.board[y, x])

    def get_positions(self, icon: Icon) -> np.ndarray:
        return self.board == icon.value

    def get_row(self, amount) -> np.array:
        """
        :param amount: n
        :return: np.array
        """
        return self.board[amount]

    def get_column(self, amount) -> np.array:
        """
        :param amount: n
        :return: np.array
        """
        return self.board[:, amount]

    def pop_icon(self, column):
        raise NotImplemented

    def push_icon(self, column):
        raise NotImplemented

    def swap_icon(self, column):
        raise NotImplemented

    def print(self):
        for i, y in enumerate(reversed(self.board), start=1):
            print('%d: ' % (self.row_size - i), end='')
            for x in y:
                print(Icon.to_char(Icon(x)), end='')
            print()
