import typing

from game import Game

EvalScore = typing.NewType('EvalScore', int)


class Solver(object):
    debug = False

    def solve(self, game: Game):
        raise NotImplemented('')

    def enable_debug(self):
        self.debug = True

    def trace(self, msg, end='\n'):
        if self.debug:
            print(msg, end=end)
