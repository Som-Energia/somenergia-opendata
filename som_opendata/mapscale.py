from math import log10

class Scale(object):

    def __init__(self, lower=0, higher=100):
        self.low = lower
        self.high = higher

    def __call__(self, val):
        if self.low == self.high:
            return 1
        else:
            return (val - self.low) / (self.high - self.low)


class LogScale(object):

    def __init__(self, higher):
        self.high = higher

    def __call__(self, val):
        if val <= 0:
            return 0
        else:
            return log10(val)/log10(self.high)
