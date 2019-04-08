class Traceable(object):
    __enable_trace = False

    def enable_trace(self):
        self.__enable_trace = True

    def trace(self, msg, end='\n'):
        if self.__enable_trace:
            print(msg, end=end)
