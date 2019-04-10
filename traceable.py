class Traceable(object):
    _enable_trace = False

    def enable_trace(self):
        self._enable_trace = True

    def trace(self, msg, end='\n'):
        if self._enable_trace:
            print(msg, end=end)
