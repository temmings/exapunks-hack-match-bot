from functools import reduce
from random import randrange

from board import Board
from character import Character
from icon import Icon, IconTypeDict, IconType


class Solver(object):
    debug = False

    def solve(self, board: Board, char: Character):
        raise NotImplemented('')

    def enable_debug(self):
        self.debug = True

    def trace(self, msg, end='\n'):
        if self.debug:
            print(msg, end=end)


class RandomSolver(Solver):
    def solve(self, board: Board, char: Character):
        destination = randrange(0, 7)
        print('current position: %d' % char.position)
        print('go_position(%d)' % destination)
        char.go_position(destination)

        r = randrange(0, 3)
        if r == 0:
            char.swap()
        elif r == 1:
            if char.having_icon is None:
                icon = board.get_surface()[char.position]
                char.grab(icon)
        elif r == 2:
            if char.having_icon is not None:
                char.throw()


class HandmadeSolver(Solver):
    ONE_ACTION_PATTERN = {
        (0, 0, 1, 0, 1, 1, 1): lambda c: c.go_position(2) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (0, 0, 1, 1, 0, 1, 1): lambda c: c.go_position(2) and c.grab() and c.go_position(4) and c.throw() and c.swap(),
        (0, 0, 1, 1, 1, 0, 1): lambda c: c.go_position(6) and c.grab() and c.go_position(5) and c.throw() and c.swap(),
        (0, 1, 0, 0, 1, 1, 1): lambda c: c.go_position(1) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (0, 1, 0, 1, 0, 1, 1): lambda c: c.go_position(1) and c.grab() and c.go_position(4) and c.throw() and c.swap(),
        (0, 1, 0, 1, 1, 0, 1): lambda c: c.go_position(6) and c.grab() and c.go_position(4) and c.throw() and c.swap(),
        (0, 1, 0, 1, 1, 1, 0): lambda c: c.go_position(1) and c.grab() and c.go_position(2) and c.throw() and c.swap(),
        (0, 1, 1, 1, 0, 0, 1): lambda c: c.go_position(6) and c.grab() and c.go_position(4) and c.throw() and c.swap(),
        (0, 1, 1, 1, 0, 1, 0): lambda c: c.go_position(5) and c.grab() and c.go_position(4) and c.throw() and c.swap(),
        (1, 0, 0, 0, 1, 1, 1): lambda c: c.go_position(0) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (1, 0, 0, 0, 1, 1, 1): lambda c: c.go_position(0) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (1, 1, 0, 1, 0, 0, 1): lambda c: c.go_position(6) and c.grab() and c.go_position(2) and c.throw() and c.swap(),
        (1, 1, 0, 1, 0, 1, 0): lambda c: c.go_position(5) and c.grab() and c.go_position(2) and c.throw() and c.swap(),
        (1, 1, 0, 1, 1, 0, 0): lambda c: c.go_position(4) and c.grab() and c.go_position(2) and c.throw() and c.swap(),
        (1, 1, 1, 0, 0, 0, 1): lambda c: c.go_position(6) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (1, 1, 1, 0, 0, 1, 0): lambda c: c.go_position(5) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
        (1, 1, 1, 0, 1, 0, 0): lambda c: c.go_position(4) and c.grab() and c.go_position(3) and c.throw() and c.swap(),
    }

    def solve(self, board: Board, char: Character):
        self.trace('character position: %d' % char.position)
        self.trace('character having icon: %s' % char.having_icon)

        self.trace('find one action pattern', end='')

        empty_row = [Icon.Empty] * board.columns
        rows = list(filter(lambda x: x != empty_row, board.get_rows(9).copy()))
        if not rows:
            return
        row = rows[0]
        for pattern, action in self.ONE_ACTION_PATTERN.items():
            self.trace('.', end='')
            zipped = zip(pattern, row)
            matched = list(filter(lambda x: x[0] == 1 and x[1] != Icon.Empty, zipped))
            if not matched:
                continue
            _, icons = zip(*matched)
            if reduce(lambda a, b: a == b, icons):
                self.trace('\nfound pattern: %s' % str(pattern))
                action(char)
        print()

    @staticmethod
    def find_bomb(board: Board):
        for bomb in IconTypeDict[IconType.Bomb]:
            # IconType value is join count of action
            positions = board.get_positions(bomb)
            if IconType.Bomb.value <= len(positions):
                return bomb, positions
        return None, []
