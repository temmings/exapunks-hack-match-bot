import numpy as np

from icon import Icon


class Board(object):
    """
    ゲームのボードを表現する。
    """

    def __init__(self, row_size: int, column_size: int):
        self.row_size = row_size
        self.column_size = column_size
        self.__board: np.ndarray = self.__init_board(row_size, column_size)

    @staticmethod
    def __init_board(row_size: int, column_size: int) -> np.ndarray:
        return np.full((row_size, column_size), Icon.Empty.value, dtype=int)

    def randomize_board(self, empty_rows=2) -> np.ndarray:
        # 5 行分のランダム配置
        x = 2 ** np.random.randint(10, size=(self.row_size - empty_rows, self.column_size))
        # 2行分の空白
        return np.append(x, np.zeros((empty_rows, self.column_size), dtype=int), axis=0)

    def randomize_row(self) -> np.ndarray:
        # 1 行分のランダム配置
        return 2 ** np.random.randint(10, size=(1, self.column_size))

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
        col = self.get_column(column)
        icon = Icon.Empty
        for n in range(self.row_size):
            if col[n] == Icon.Empty.value:
                continue
            icon = col[n]
            col[n] = Icon.Empty.value
            break
        return Icon(icon)

    def push_icon(self, column, icon: Icon):
        col = self.get_column(column)
        for n in range(self.row_size):
            if col[n] == Icon.Empty.value:
                col[n] = icon.value
                break

    def swap_icon(self, column):
        col = self.get_column(column)
        for n in range(self.row_size):
            if col[n] == Icon.Empty.value:
                continue
            col[n], col[n+1] = col[n+1], col[n]
            break

    @property
    def max_icon_height(self):
        return max(np.where(self.board != Icon.Empty.value)[0])

    def print(self):
        for i, y in enumerate(self.board, start=0):
            print('%d: ' % i, end='')
            for x in y:
                print(Icon.to_char(Icon(x)), end='')
            print()
