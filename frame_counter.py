import time


class FrameCounter(object):
    current = 0
    prev_time = 0
    current_time = 0

    def count_up(self) -> int:
        self.current += 1
        self.prev_time = self.current_time
        self.current_time = time.process_time()
        return self.current
