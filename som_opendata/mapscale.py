from math import log10

class LinearScale(object):

    def __init__(self, lower=0, higher=100):
        self.low = lower
        self.high = higher

    def __call__(self, val):
        if self.low == self.high:
            return 1
        else:
            return (val - self.low) / (self.high - self.low)

    def inverse(self, val):
        return self.low + val * (self.high - self.low)

class LogScale(object):

    def __init__(self, higher, lower=1):
        self.low = lower
        self.high = higher

    def __call__(self, val):
        if val <= 0:
            return 0
        else:
            return log10(val / self.low) / log10(self.high / self.low)

    def inverse(self, val):
        return self.low * (self.high /self.low) ** val
