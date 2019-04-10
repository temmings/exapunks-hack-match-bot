import time


class FrameCounter(object):
    def __init__(self):
        self.current = 0
        self.prev_time = time.process_time()
        self.process_time = 0

    def count_up(self) -> int:
        self.current += 1
        current_time = time.process_time()
        self.process_time = current_time - self.prev_time
        self.prev_time = current_time
        return self.current
