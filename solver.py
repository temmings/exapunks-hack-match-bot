from collections import Counter
from random import randrange
import typing

from board import Board
from game import Game
from icon import Icon, IconTypeDict, IconType

EvalScore = typing.NewType('EvalScore', int)
Answer = typing.NewType('Answer', typing.List[typing.Callable])


class Solver(object):
    debug = False

    def solve(self, game: Game):
        raise NotImplemented('')

    def enable_debug(self):
        self.debug = True

    def trace(self, msg, end='\n'):
        if self.debug:
            print(msg, end=end)


class RandomSolver(Solver):
    def solve(self, game: Game):
        destination = randrange(0, 7)
        print('current position: %d' % game.char.position)
        print('go_position(%d)' % destination)
        game.char.go_position(destination)

        answer = Answer([])
        r = randrange(0, 3)
        if r == 0:
            answer += game.char.swap
        elif r == 1:
            if game.char.having_icon is None:
                icon = game.board.get_surface()[game.char.position]
                answer += lambda: game.char.grab(icon)
        elif r == 2:
            if game.char.having_icon is not None:
                answer += game.char.throw

        return answer


class HandmadeSolver(Solver):
    def solve(self, game: Game, depth=10):
        self.trace('character position: %d' % game.char.position)
        self.trace('character having icon: %s' % game.char.having_icon)
        score = self.eval(game.board)
        print('board score: %d' % score)

        answer = Answer([])
        score = eval(game.board)

        return answer

    @staticmethod
    def eval(board) -> EvalScore:
        score = EvalScore(0)

        map_between = lambda func, lst: map(func, lst, lst[1:])
        # 横に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.rows):
            neighbors = map_between(lambda a, b: a == b, board.get_row(n))
            score += list(neighbors).count(True) * 1

        # 縦に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.columns):
            neighbors = map_between(lambda a, b: a == b, board.get_column(n))
            score += list(neighbors).count(True) * 1

        counter = Counter(board.board)

        # 利用不可能なアイコンが存在するのは悪い (各-1点)
        score += sum([v for k, v in counter.items() if Icon(k) in IconType.Normal and v < IconType.Normal.value]) * -1

        # 利用不可能なボムが存在するのは普通 (各0点)
        score += sum([v for k, v in counter.items() if Icon(k) in IconType.Normal and v < IconType.Bomb.value]) * 0

        # 利用可能なボムが存在するのは良い (利用可能ボムごとに各5点)
        score += len([k for k, v in counter.items() if Icon(k) in IconType.Bomb and IconType.Bomb.value <= v]) * 5

        return score

    @staticmethod
    def find_bomb(board: Board):
        for bomb in IconTypeDict[IconType.Bomb]:
            # IconType value is join count of action
            positions = board.get_positions(bomb)
            if IconType.Bomb.value <= len(positions):
                return bomb, positions
        return None, []
