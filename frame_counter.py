import time


class FrameCounter(object):
    current = 0
    prev_time = time.clock()
    current_time = time.clock()

    def count_up(self) -> int:
        self.current += 1
        self.prev_time = self.current_time
        self.current_time = time.clock()
        return self.current
