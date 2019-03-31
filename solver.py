from random import randrange

from board import Board
from character import Character
from icon import Icon


class Solver(object):
    debug = False

    def solve(self, board: Board, char: Character):
        raise NotImplemented('')

    def enable_debug(self):
        self.debug = True

    def trace(self, msg):
        if self.debug:
            print(msg)


class HandmadeSolver(Solver):
    def solve(self, board: Board, char: Character):
        self.trace('character position: %d' % char.position)
        self.trace('character having icon: %s' % char.having_icon)
        r = randrange(0, 5)
        if r == 0:
            self.trace('move left')
            char.left() if char.position >= char.MIN_POSITION else char.right()
        elif r == 1:
            self.trace('move right')
            char.right() if char.position <= char.MAX_POSITION else char.left()
        elif r == 2:
            self.trace('swap icon')
            char.swap()
        elif r == 3:
            self.trace('grab icon: %s' % Icon.Empty)
            char.grab(Icon.Empty) if not char.having_icon else char.throw()
        elif r == 4:
            self.trace('pop icon: %s' % Icon.Empty)
            char.throw() if char.having_icon else char.grab(Icon.Empty)
        else:
            self.trace('no action')
