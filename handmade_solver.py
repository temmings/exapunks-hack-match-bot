import copy
import typing
from collections import namedtuple
from itertools import product

import numpy as np

from game import Game
from icon import Icon
from solver import Solver

Score = typing.NewType('Score', int)
EvalScore = typing.NewType('EvalScore', int)
ScoreWithActions = namedtuple('ScoreWithActions', ('score', 'actions'))


class HandmadeSolver(Solver):
    def solve(self, game: Game, depth=2):
        score = self.eval(game)
        self.trace('board score: %d' % score)
        score, actions = self.__solve(
            game, depth=depth, prev_score=score, actions=[])
        self.trace('having icon: %s' % game.char.having_icon)
        self.trace('better actions: ', end='')
        for action in actions:
            action(game)
        self.trace('')
        self.trace('better action score: %d' % score)

    CAN_ACTIONS = (
        lambda n: lambda g: g.char.swap_position(n),
        lambda n: lambda g: g.char.grab_position(n) if g.char.having_icon is None else g.char.throw_position(n),
        lambda n: lambda g: g.char.throw_position(n) if g.char.having_icon is not None else g.char.grab_position(n),
    )
    memo_board = {}

    def __solve(self, game: Game, depth: int, prev_score, actions: list) -> (EvalScore, typing.List[typing.Callable]):
        assert(0 <= depth)

        # 同一局面を迎えたら、メモ化したスコアとアクションを返却する
        #key = (game.board.board.tobytes(), game.char.having_icon)
        #if key in self.memo_board:
        #    memo = self.memo_board[key]
        #    return memo.score, memo.actions

        candidates = {}
        for action in [action(n) for action, n in product(self.CAN_ACTIONS, range(game.columns))]:
            # 思考用のゲームボードを作成
            state = game.copy()
            action(state)
            game_score = state.effect(state.board)
            eval_score = self.eval(state)
            score = prev_score + eval_score

            if 0 < depth:
                return self.__solve(
                    state,
                    depth=depth-1,
                    prev_score=score,
                    actions=copy.deepcopy(actions) + [action])
            else:
                actions = actions.copy() + [action]
            candidates[score] = (state, actions)

        score = max(candidates.keys())
        state, actions = candidates[score]

        key = (state.board.board.tobytes(), game.char.having_icon)
        self.memo_board[key] = ScoreWithActions(score, actions)
        return score, actions

    @staticmethod
    def eval(game: Game) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが低いほうが良い
        score -= game.board.max_icon_height * 100

        # アイコンの存在しない列が存在するのは悪い
        for n in range(game.board.column_size):
            col = game.board.get_column(n)
            if (col == Icon.Empty.value).all():
                score -= 50

        # アイコンを掴んでないほうが良い
        score += 10 if game.char.having_icon is None else -10

        # 空白アイコンの数が多いほうが良い
        score += np.count_nonzero(game.board.board == Icon.Empty.value)

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.row_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_row(n))
            count = list(neighbors).count(True)
            score += count * 5

        # 縦に隣接した同一アイコンが多いほど良い
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.column_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_column(n))
            count = list(neighbors).count(True)
            score += count * 2

        return score
