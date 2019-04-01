import time


class FrameCounter(object):
    current = 0
    prev_time = 0
    process_time = 0

    def count_up(self) -> int:
        self.current += 1
        current_time = time.process_time()
        self.prev_time = current_time
        self.process_time = current_time - self.prev_time
        return self.current
