import time


class RequestTimer:

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        end = time.clock()
        self.latency = end - self.start
