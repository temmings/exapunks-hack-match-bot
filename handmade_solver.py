import copy
import typing

import numpy as np

from board import Board
from character import Character
from game import Game
from solver import Solver

Score = typing.NewType('Score', int)
EvalScore = typing.NewType('EvalScore', int)


class HandmadeSolver(Solver):
    CAN_ACTIONS = (
        lambda n: lambda g: g.char.grab_position(n) if g.char.having_icon is None else g.char.throw_position(n),
        lambda n: lambda g: g.char.throw_position(n) if g.char.having_icon is not None else g.char.grab_position(n),
        lambda n: lambda g: g.char.swap_position(n),
    )

    def solve(self, game: Game, depth=1):
        current_board_score = self.eval(game)
        self.trace('max height: %d' % game.board.max_icon_height)
        self.trace('have icon: %s' % game.char.having_icon)
        self.trace('evaluated board score: %d' % current_board_score)

        score, actions = self.__solve(
            game, depth=depth, prev_score=current_board_score, actions=[])

        self.trace('action score: %d' % score)
        self.trace('do action: ', end='')
        for action in actions:
            action(game)
        self.trace('')

    memo = {}

    def __solve(self, game: Game, depth: int,
                prev_score: EvalScore, actions: list):

        # 同一局面を迎えたら、メモ化したスコアとアクションを返却する
        key = game.board.board.tobytes()
        if key in self.memo:
            value = self.memo[key]
            return value[0], value[1]

        if depth == 0:
            return prev_score, actions

        # ゲームオーバー局面からは探索しない
        if not game.is_alive:
            return -99999, actions

        candidates = {}
        for action in self.CAN_ACTIONS:
            for n in range(game.columns):
                vgame = self.new_game(game)
                action(n)(vgame)
                game_score = vgame.effect(vgame.board)
                score = self.eval(vgame)
                _actions = copy.deepcopy(actions)
                _actions.append(action(n))

                score, actions = self.__solve(
                    vgame, depth=depth - 1, prev_score=score,
                    actions=_actions)
                candidates[score] = (vgame, actions)

        if not candidates.keys():
            return prev_score, actions
        max_score = max(candidates.keys())
        vgame, actions = candidates[max_score]
        key = vgame.board.board.tobytes()
        self.memo[key] = (max_score, actions)
        return max_score, actions

    @staticmethod
    def new_game(game):
        """
        思考用のゲームボードを作成
        """
        vboard = Board(game.rows, game.columns)
        vboard.replace(np.array(game.board.board, copy=True))
        return Game(vboard, Character(vboard))

    @staticmethod
    def eval(game: Game) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが低いほうが良い(高さごとに50点)
        score += (game.board.row_size - game.board.max_icon_height) * 50

        # アイコンを保持していないほうが良い
        score += 10 if game.char.having_icon is None else -10

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い (各5点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.row_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_row(n))
            count = list(neighbors).count(True)
            score += count * 2

        return score
