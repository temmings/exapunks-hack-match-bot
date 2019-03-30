from icon import Icon


class Board(object):
    def __init__(self, row_number: int, column_number: int):
        self.rows = self.init_board(row_number, column_number)

    def init_board(self, row_number: int, column_number: int) -> list:
        column = [Icon.Empty for _ in range(0, column_number)]
        rows = [column for _ in range(0, row_number)]
        return rows

    def print_board(self):
        for i, y in enumerate(self.rows):
            print('%d: ' % i, end='')
            for x in y:
                print(x.value, end='')
            print()
