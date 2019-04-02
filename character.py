from board import Board


class Character(object):
    MIN_POSITION = 0
    MAX_POSITION = 6
    # position range (0, 6)
    __position = 3
    __having_icon = None

    def __init__(self, board: Board):
        self.board = board

    @property
    def position(self) -> int:
        return self.__position

    @property
    def having_icon(self):
        return self.__having_icon

    def left(self):
        assert(self.MIN_POSITION < self.position)
        self.__position -= 1

    def right(self):
        assert(self.position < self.MAX_POSITION)
        self.__position += 1

    def grab_icon(self):
        assert(self.having_icon is None)
        icon = self.board.pop_icon(self.position)
        self.__having_icon = icon

    def throw_icon(self):
        assert(self.having_icon is not None)
        self.board.push_icon(self.position, self.having_icon)
        self.__having_icon = None

    def swap(self):
        self.board.swap_icon(self.position)

    def go_position(self, destination):
        assert(self.MIN_POSITION <= destination <= self.MAX_POSITION)
        while self.position < destination:
            self.right()
        while self.position > destination:
            self.left()
