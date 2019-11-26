class Scale(object):

    def __init__(self, lower=0, higher=1000):
        self.low = lower
        self.high = higher

    def __call__(self, point):
        if point == self.low:
            return 0
        else:
            return 1
