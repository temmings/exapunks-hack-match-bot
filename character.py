from controller import Controller
from icon import Icon


class Character(object):
    MIN_POSITION = 0
    MAX_POSITION = 6
    # position range (0, 6)
    __position = 3
    __having_icon = None

    def __init__(self, controller: Controller):
        self.controller = controller

    @property
    def position(self) -> int:
        return self.__position

    @property
    def having_icon(self):
        return self.__having_icon

    def left(self):
        assert(self.MIN_POSITION < self.position)
        if self.position == self.MIN_POSITION:
            return
        self.__position -= 1
        self.controller.left()

    def right(self):
        assert(self.position < self.MAX_POSITION)
        if self.position == self.MAX_POSITION:
            return
        self.__position += 1
        self.controller.right()

    def grab(self, icon: Icon):
        assert(self.having_icon is None)
        self.__having_icon = icon
        self.controller.pop()

    def throw(self):
        assert(self.having_icon is not None)
        self.__having_icon = None
        self.controller.push()

    def swap(self):
        self.controller.swap()

    def go_position(self, destination):
        while self.position != destination:
            if self.position < destination:
                self.right()
            else:
                self.left()

