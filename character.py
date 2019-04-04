from board import Board
from void_controller import VoidController


class Character(object):
    MIN_POSITION = 0
    MAX_POSITION = 6
    # position range (0, 6)
    __position = 3
    __having_icon = None
    
    debug = False

    def __init__(self, board: Board, controller=VoidController()):
        self.board = board
        self.controller = controller

    @property
    def position(self) -> int:
        return self.__position

    @property
    def having_icon(self):
        return self.__having_icon

    def trace(self, msg, end='\n'):
        if self.debug:
            print(msg, end=end)

    def enable_debug(self):
        self.debug = True

    def left(self):
        assert(self.MIN_POSITION < self.position)
        self.trace('<', end=',')
        self.__position -= 1
        self.controller.left()

    def right(self):
        assert(self.position < self.MAX_POSITION)
        self.trace('>', end=',')
        self.__position += 1
        self.controller.right()

    def grab(self):
        assert(self.having_icon is None)
        if self.having_icon is not None:
            return
        self.trace('g', end=',')
        success, icon = self.board.pop_icon(self.position)
        if success:
            self.__having_icon = icon
            self.controller.grab()

    def throw(self):
        assert(self.having_icon is not None)
        if self.having_icon is None:
            return
        self.trace('t', end=',')
        self.board.push_icon(self.position, self.having_icon)
        self.__having_icon = None
        self.controller.throw()

    def swap(self):
        self.trace('s', end=',')
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
