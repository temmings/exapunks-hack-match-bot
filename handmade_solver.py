import typing

import numpy as np

from board import Board
from character import Character
from game import Game
from solver import Solver, EvalScore


class HandmadeSolver(Solver):
    def solve(self, game: Game, depth=3):
        current_board_score = self.eval(game)
        self.trace('max height: %d' % game.board.max_icon_height)
        self.trace('evaluated board score: %d' % current_board_score)
        self.trace('have icon: %s' % game.char.having_icon)

        candidates = {}
        can_actions = (self.swap, self.grab, self.throw)
        for n in range(game.columns):
            for action in can_actions:
                # 思考用のゲームボードを作成
                vboard = Board(game.rows, game.columns)
                vboard.replace(np.array(game.board.board, copy=True))
                vgame = Game(vboard, Character(vboard))
                score, actions = self.__solve(
                    vgame, depth=depth, prev_score=current_board_score,
                    action=action(n), actions=[].copy())
                candidates[score] = actions

        # 最終スコアが高い行動を選択する
        max_score = max(candidates.keys())
        self.trace('action score: %d' % max_score)
        self.trace('do action: ', end='')
        if current_board_score == max_score:
            return
        for f in candidates[max_score]:
            f(game)
        self.trace('')

    def __solve(self, game: Game, depth: int, prev_score: EvalScore, action: typing.Callable,
                actions: typing.List[typing.Callable]):
        if depth == 0:
            return prev_score, actions
        action(game)
        actions.append(action)
        game.effect(game.board)
        score = self.eval(game)

        # 前局面よりも高いボードスコアを見つけたら採用する
        if prev_score < score:
            return score, actions

        # ゲームオーバーに逹っしたであろう局面からは探索しない
        if score < -50000:
            return score, actions

        candidates = {}
        can_actions = (self.swap, self.grab, self.throw)
        for n in range(game.columns):
            for action in can_actions:
                # 思考用のゲームボードを作成
                vboard = Board(game.rows, game.columns)
                vboard.replace(np.array(game.board.board, copy=True))
                vgame = Game(vboard, Character(vboard))
                score, actions = self.__solve(
                    vgame, depth=depth - 1, prev_score=score,
                    action=action(n), actions=actions.copy())
                candidates[score] = actions

        max_score = max(candidates.keys())
        return max_score, candidates[max_score]

    @staticmethod
    def eval(game: Game) -> EvalScore:
        score = EvalScore(0)

        # アイコン群の高さが行のサイズに逹っした = ゲームオーバー
        if game.board.row_size <= game.board.max_icon_height:
            return EvalScore(-99999)

        # アイコン群の高さが低いほうが良い(高さごとに-10点)
        score += game.board.max_icon_height * -20

        def map_between(func: typing.Callable, lst: list) -> iter:
            return map(func, lst, lst[1:])

        # 横に隣接した同一アイコンが多いほど良い (各5点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.row_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_row(n))
            score += list(neighbors).count(True) * 2

        # 縦に隣接した同一アイコンが多いほど良い (各1点)
        # 空白セルもここでスコアリングされる
        # (縦と横で重複して加点されるアイコンもある)
        for n in range(game.board.column_size):
            neighbors = map_between(lambda a, b: a == b, game.board.get_column(n))
            score += list(neighbors).count(True) * 1

        return score

    @staticmethod
    def swap(n):
        def f(game):
            game.char.swap_position(n)
        return f

    @staticmethod
    def grab(n):
        def f(game):
            if game.char.having_icon is not None:
                game.char.throw_position(n)
            else:
                game.char.grab_position(n)
        return f

    @staticmethod
    def throw(n):
        def f(game):
            if game.char.having_icon is None:
                game.char.grab_position(n)
            else:
                game.char.throw_position(n)
        return f
