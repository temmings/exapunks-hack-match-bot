import typing

import numpy as np

from board import Board
from character import Character
from game import Game
from solver import Solver, EvalScore


class HandmadeSolver(Solver):
    def solve(self, game: Game, depth=10):
        score = self.eval(game.board)
        self.trace('evaluated board score: %d' % score)
        self.trace('have icon: %s' % game.char.having_icon)

        can_actions = (
            lambda i: lambda g: g.char.swap_position(i),
            lambda i: lambda g: g.char.throw_position(i) if g.char.having_icon is not None else g.char.grab_position(i),
            lambda i: lambda g: g.char.grab_position(i) if g.char.having_icon is None else g.char.throw_position(i),
        )
        candidates = {}
        for n in range(game.columns):
            for action in can_actions:
                # 思考用のゲームボードを作成
                vboard = Board(game.rows, game.columns)
                vboard.replace(np.array(game.board.board, copy=True))
                vgame = Game(vboard, Character(vboard))
                score, actions = self.__solve(vgame, depth=depth, prev_score=score, action=action(n), actions=[])
                candidates[score] = actions

        # 最終スコアが高い行動を選択する
        max_score = max(candidates.keys())
        self.trace('action score: %d' % max_score)
        self.trace('do action: ', end='')
        for f in candidates[max_score]:
            f(game)
        self.trace('')

    def __solve(self, game: Game, depth: int, prev_score: EvalScore, action: typing.Callable, actions: typing.List[typing.Callable]):
        if depth == 0:
            return prev_score, actions
        action(game)
        actions.append(action)
        game.effect(game.board)
        score = self.eval(game.board)

        # 前局面よりも2倍以上高いボードスコアを見つけたら採用する
        if prev_score < score:
            return score, actions

        # ゲームオーバーに逹っしたであろう局面からは探索しない
        if score < -50000:
            return score, actions

        can_actions = (
            lambda i: lambda g: g.char.swap_position(i),
            lambda i: lambda g: g.char.throw_position(i) if g.char.having_icon is not None else g.char.grab_position(i),
            lambda i: lambda g: g.char.grab_position(i) if g.char.having_icon is None else g.char.throw_position(i),
        )
        for n in range(game.columns):
            for action in can_actions:
                # 思考用のゲームボードを作成
                vboard = Board(game.rows, game.columns)
                vboard.replace(np.array(game.board.board, copy=True))
                vgame = Game(vboard, Character(vboard))
                return self.__solve(vgame, depth=depth - 1, prev_score=score, action=action(n), actions=actions.copy())

    @staticmethod
    def eval(board: Board) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが行のサイズに逹っした = ゲームオーバー
        if board.max_icon_height >= board.row_size:
            return EvalScore(-99999)

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # アイコン群の高さが低いほうが良い(高さごとに-10点)
        score += board.max_icon_height * -10

        # 横に隣接した同一アイコンが多いほど良い (各5点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.row_size):
            neighbors = map_between(lambda a, b: a == b, board.get_row(n))
            score += list(neighbors).count(True) * 2

        # 縦に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(board.column_size):
            neighbors = map_between(lambda a, b: a == b, board.get_column(n))
            score += list(neighbors).count(True) * 1

        return score
