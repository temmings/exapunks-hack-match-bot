class Controller(object):
    def __init__(self, release_wait_second: float):
        self.release_wait_second = release_wait_second

    def start(self):
        raise NotImplemented

    def left(self):
        raise NotImplemented

    def right(self):
        raise NotImplemented

    def pop(self):
        raise NotImplemented

    def push(self):
        raise NotImplemented

    def swap(self):
        raise NotImplemented
