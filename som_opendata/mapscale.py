class Scale(object):

    def __init__(self, lower=0, higher=100):
        self.low = lower
        self.high = higher

    def __call__(self, val):
        if val == self.low:
            return 0
        else:
            return (val - self.low) / (self.high - self.low)
