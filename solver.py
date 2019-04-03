from random import randrange
import typing

from game import Game

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

    @staticmethod
    def eval(board) -> EvalScore:
        score = EvalScore(0)

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.row_size):
            neighbors = map_between(lambda a, b: a == b, board.get_row(n))
            score += list(neighbors).count(True) * 1

        # 縦に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.column_size):
            neighbors = map_between(lambda a, b: a == b, board.get_column(n))
            score += list(neighbors).count(True) * 1

        return score

