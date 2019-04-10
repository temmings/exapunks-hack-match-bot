import os
import sys
import typing
from collections import namedtuple
from itertools import product

import numpy as np
import dill

from game import Game, Icon
from solver import Solver

Score = typing.NewType('Score', int)
EvalScore = typing.NewType('EvalScore', int)
ScoreWithActions = namedtuple('ScoreWithActions', ('score', 'actions'))


class HandmadeSolver(Solver):
    MEMO_SERIALIZE_FILENAME = 'solver.memo.dat'
    CAN_ACTIONS = (
        lambda n: lambda g: g.char.swap_position(n),
        lambda n: lambda g: g.char.grab_position(n) if g.char.having_icon is None else g.char.throw_position(n),
    )
    memo_board = {}

    def __init__(self, use_memo=True, store_memo=False):
        self.use_memo = use_memo
        self.store_memo = store_memo
        if self.use_memo:
            self.load_memo()

    def __del__(self):
        if self.store_memo:
            self.save_memo()

    def solve(self, game: Game, depth=3):
        assert (1 <= depth)
        score = self.eval(game)
        self.trace('board score: %d' % score)
        score, actions = self._solve(
            game, depth=depth, score=score, actions=[])
        self.trace('having icon: %s' % game.char.having_icon)
        self.trace('better actions: ', end='')
        for action in actions:
            action(game)
        self.trace('')
        self.trace('better action score: %d' % score)
        if self.use_memo and \
                self.store_memo and \
                0 == game.current_frame % 1000:
            self.save_memo()

    def _solve(self, game: Game, depth: int, score: int,
               actions: typing.List[typing.Callable]) -> (EvalScore, typing.List[typing.Callable]):
        assert (0 <= depth)
        if 0 == depth:
            return score, actions

        # 同一局面を迎えたら、メモ化したスコアとアクションを返却する
        if self.use_memo and game in self.memo_board.keys():
            memo = self.memo_board[game]
            return memo.score, memo.actions

        candidates = {}
        for action in [action(n) for action, n in product(self.CAN_ACTIONS, range(game.columns))]:
            # 思考用のゲームを作成
            state = game.copy()
            # 可能なアクションを適用して、ゲーム状態をスコアリングする
            action(state)
            game_score = state.effect(state.board)
            eval_score = self.eval(state)

            # 再帰的に可能なアクションを試していく
            _score, _actions = self._solve(
                state,
                depth=depth - 1,
                score=eval_score,
                actions=actions.copy() + [action])
            candidates[_score] = _actions

        max_score = max(candidates.keys())
        actions = candidates[max_score]

        if self.use_memo:
            self.memo_board[game] = ScoreWithActions(max_score, actions)
        return max_score, actions

    @staticmethod
    def eval(game: Game) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが低いほうが良い
        score -= game.board.max_icon_height * 100

        # 空白アイコンの数が多いほうが良い
        score += np.count_nonzero(game.board.board == Icon.Empty.value)

        # アイコンを掴んでないほうが良い
        #score += 10 if game.char.having_icon is None else -10

        # アイコンの存在しない列が存在するのは悪い
        #for n in range(game.board.column_size):
        #    col = game.board.get_column(n)
        #    if (col == Icon.Empty.value).all():
        #        score -= 50

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        #for n in range(game.board.row_size):
        #    neighbors = map_between(lambda a, b: a == b, #game.board.get_row(n))
        #    count = list(neighbors).count(True)
        #    score += count * 2

        # 縦に隣接した同一アイコンが多いほど良い
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        #for n in range(game.board.column_size):
        #    neighbors = map_between(lambda a, b: a == b, #game.board.get_column(n))
        #    count = list(neighbors).count(True)
        #    score += count * 2

        return score

    def save_memo(self):
        try:
            with open(self.MEMO_SERIALIZE_FILENAME, 'wb') as f:
                dill.dump(self.memo_board, f)
        except KeyboardInterrupt:
            print('catch Ctrl-C.')
            print('saving memo: %s' % self.MEMO_SERIALIZE_FILENAME)
            with open(self.MEMO_SERIALIZE_FILENAME, 'wb') as f:
                dill.dump(self.memo_board, f)

    def load_memo(self) -> bool:
        if not os.path.isfile(self.MEMO_SERIALIZE_FILENAME):
            return False
        if 0 == os.path.getsize(self.MEMO_SERIALIZE_FILENAME):
            return False
        with open(self.MEMO_SERIALIZE_FILENAME, 'rb') as f:
            try:
                self.memo_board = dill.load(f)
            except (TypeError, EOFError):
                print('error: %s' % sys.exc_info()[1])
                return False
        return True
