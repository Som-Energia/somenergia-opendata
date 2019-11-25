class MapScale(object):

    def __init__(self, min, max, type='linear'):
        self.min = min
        self.max = max
        self.type = type

    def __call__(self, point):
        return 0