from random import randrange

from game import Game
from solver import Solver


class RandomSolver(Solver):
    def solve(self, game: Game):
        n = randrange(game.columns)
        r = randrange(0, 3)
        if r == 0:
            game.char.swap_position(n)
        elif r == 1:
            if game.char.having_icon is None:
                game.char.grab_position(n)
        elif r == 2:
            if game.char.having_icon is not None:
                game.char.throw_position(n)