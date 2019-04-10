from random import randrange

from game import Game
from solver import Solver


class RandomSolver(Solver):
    def solve(self, game: Game):
        n = randrange(game.columns)
        (
            lambda g, n: g.char.swap_position(n),
            lambda g, n: g.char.grab_position(n) if game.char.having_icon is None else g.char.throw_position(n),
            lambda g, n: g.char.throw_position(n) if game.char.having_icon is not None else g.char.grab_position(n),
        )[randrange(0, 3)](game, n)
