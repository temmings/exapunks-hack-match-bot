import typing
from collections import namedtuple
from itertools import product

import numpy as np

from board import Board
from character import Character
from game import Game
from icon import Icon
from solver import Solver

Score = typing.NewType('Score', int)
EvalScore = typing.NewType('EvalScore', int)
ScoreWithActions = namedtuple('ScoreWithActions', ('score', 'actions'))


class HandmadeSolver(Solver):
    def solve(self, game: Game, depth=10):
        score = self.eval(game)
        self.trace('board score: %d' % score)
        score, actions = self.__solve(
            game, depth=depth, prev_score=score, actions=[])
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
        if 0 == depth:
            return prev_score, actions

        # 同一局面を迎えたら、メモ化したスコアとアクションを返却する
        key = game.board.board.tobytes()
        if key in self.memo_board:
            memo = self.memo_board[key]
            return memo.score, memo.actions

        candidates = {}
        for action in [action(n) for action, n in product(self.CAN_ACTIONS, range(game.columns))]:
            # 思考用のゲームボードを作成
            board = Board(game.rows, game.columns)
            board.replace(np.array(game.board.board, copy=True))
            vgame = Game(board, Character(board))
            action(vgame)
            vgame.effect(vgame.board)
            score = self.eval(vgame)
            candidates[score] = (vgame, actions + [action])

        better_score = max(candidates.keys())
        better_state, better_actions = candidates[better_score]

        score, actions = self.__solve(
            better_state, depth=depth - 1,
            prev_score=better_score, actions=better_actions)

        key = better_state.board.board.tobytes()
        self.memo_board[key] = ScoreWithActions(score, actions)
        return score, actions

    @staticmethod
    def eval(game: Game) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが低いほうが良い(高さごとに50点)
        score += (game.board.row_size - game.board.max_icon_height - 1) * 50

        # アイコンの存在しない列が存在するのは悪い
        for n in range(game.board.column_size):
            col = game.board.get_column(n)
            if (col == Icon.Empty.value).all():
                score -= 100

        # アイコンを保持していないほうが良い
        score += 10 if game.char.having_icon is None else -10

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い (各2点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.row_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_row(n))
            count = list(neighbors).count(True)
            score += count * 2

        # 縦に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.column_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_column(n))
            count = list(neighbors).count(True)
            score += count * 1

        return score
