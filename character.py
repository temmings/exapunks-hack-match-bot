from board import Board
from icon import Icon
from traceable import Traceable
from void_controller import VoidController


class Character(Traceable):
    MIN_POSITION = 0
    MAX_POSITION = 6
    # position range (0, 6)
    __position = 3
    _having_icon = None

    def __init__(self, board: Board, controller=VoidController()):
        self.board = board
        self.controller = controller

    @property
    def position(self) -> int:
        return self.__position

    @property
    def having_icon(self):
        return self._having_icon

    def left(self):
        assert(self.MIN_POSITION < self.position)
        self.__position -= 1
        self.controller.left()

    def right(self):
        assert(self.position < self.MAX_POSITION)
        self.__position += 1
        self.controller.right()

    def grab(self):
        assert(self.having_icon is None)
        success, icon = self.board.pop_icon(self.position)
        if icon == Icon.Empty:
            return
        self.trace('g(%d:%s)' % (self.position, icon), end=', ')
        if success:
            self._having_icon = icon
            self.controller.grab()

    def throw(self):
        assert(self.having_icon is not None)
        self.trace('t(%d:%s)' % (self.position, self.having_icon), end=', ')
        self.board.push_icon(self.position, self.having_icon)
        self._having_icon = None
        self.controller.throw()

    def swap(self):
        self.trace('s(%d)' % self.position, end=', ')
        self.board.swap_icon(self.position)
        self.controller.swap()

    def go_position(self, destination):
        assert(self.MIN_POSITION <= destination <= self.MAX_POSITION)
        while self.position < destination:
            self.right()
        while self.position > destination:
            self.left()

    def swap_position(self, destination):
        self.go_position(destination)
        self.swap()

    def grab_position(self, destination):
        self.go_position(destination)
        self.grab()

    def throw_position(self, destination):
        self.go_position(destination)
        self.throw()
