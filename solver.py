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

    def trace(self, msg):
        if self.debug:
            print(msg)


class RandomSolver(Solver):
    def solve(self, board: Board, char: Character):
        r = randrange(0, 5)
        if r == 0:
            char.left() if char.position >= char.MIN_POSITION else char.right()
        elif r == 1:
            char.right() if char.position <= char.MAX_POSITION else char.left()
        elif r == 2:
            char.swap()
        elif r == 3:
            char.grab(Icon.Empty) if not char.having_icon else char.throw()
        elif r == 4:
            char.throw() if char.having_icon else char.grab(Icon.Empty)


class HandmadeSolver(Solver):
    LOOK_DEPTH = 2

    ONE_PASS_ACTION_PATTERNS = (
        (True, True, True, False, True)
    )

    def solve(self, board: Board, char: Character):
        self.trace('character position: %d' % char.position)
        self.trace('character having icon: %s' % char.having_icon)

        rows = board.get_joined_reversed_rows(self.LOOK_DEPTH)

        bomb, positions = self.find_bomb(board)
        # ボード上に利用可能なボムが存在する
        if bomb:
            pass

    @staticmethod
    def find_bomb(board: Board):
        for bomb in IconTypeDict[IconType.Bomb]:
            # IconType value is join count of action
            positions = board.get_positions(bomb)
            if IconType.Bomb.value <= len(positions):
                return bomb, positions
        return None, []
