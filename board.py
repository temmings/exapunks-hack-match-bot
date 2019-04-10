from __future__ import annotations
import numpy as np

from icon import Icon


class Board(object):
    """
    ゲームのボードを表現する。
    """

    def __init__(self, row_size: int, column_size: int):
        self.row_size = row_size
        self.column_size = column_size
        self.__board = self.init(row_size, column_size)

    @staticmethod
    def init(row_size: int, column_size: int) -> np.ndarray:
        return np.full((row_size, column_size), Icon.Empty.value, dtype=np.uint16)

    @staticmethod
    def pack(board: np.ndarray) -> np.ndarray:
        b = board.T
        for c in b:
            for n in range(c.size-1, 0, -1):
                if c[n-1] == Icon.Empty.value and c[n] == Icon.Empty.value:
                    continue
                if c[n-1] == Icon.Empty.value:
                    c[n-1], c[n] = c[n], c[n-1]
        return b.T

    def randomize(self, rows=1) -> np.ndarray:
        # ランダム配置
        x = self.random_row(rows=rows)
        # 空白
        return np.append(x, self.empty_row(rows=self.row_size - rows), axis=0)

    def random_row(self, rows=1, has_bomb=False) -> np.ndarray:
        return 2 ** np.random.randint(10 if has_bomb else 5, size=(rows, self.column_size), dtype=np.uint16)

    def empty_row(self, rows=1) -> np.ndarray:
        return np.zeros((rows, self.column_size), dtype=np.uint16)

    @property
    def board(self) -> np.ndarray:
        return self.__board

    def replace(self, new_board: np.ndarray):
        self.__board = new_board

    def get_icon(self, y, x) -> Icon:
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
        col = self.get_column(column)
        for n in range(self.row_size, 0, -1):
            if col[n-1] == Icon.Empty.value:
                continue
            icon = col[n-1]
            col[n-1] = Icon.Empty.value
            return True, Icon(icon)
        return False, Icon.Empty

    def push_icon(self, column, icon: Icon):
        col = self.get_column(column)
        for n in range(self.row_size):
            if col[n] == Icon.Empty.value:
                col[n] = icon.value
                break

    def swap_icon(self, column):
        col = self.get_column(column)
        for n in range(self.row_size-1, 0, -1):
            if col[n] == Icon.Empty.value:
                continue
            col[n], col[n-1] = col[n-1], col[n]
            break

    @property
    def max_icon_height(self):
        seq = np.where(self.board != Icon.Empty.value)[0]
        if seq.size == 0:
            return 0
        return max(np.where(self.board != Icon.Empty.value)[0])

    def serialize(self) -> str:
        output = []
        for i, y in enumerate(self.board, start=0):
            line = [Icon.to_char(Icon(x)) for x in y]
            output.append(''.join(line))
        return '\n'.join(output)

    def print(self):
        for i, line in enumerate(self.serialize().splitlines(keepends=False)):
            print('%2d: %s' % (i, line))

    def copy(self) -> Board:
        new_board = Board(self.row_size, self.column_size)
        new_board.replace(np.array(self.board, copy=True))
        return new_board
