from colour import Color


class Gradient(object):

    def __init__(self, fro, to):
        self.low = Color(fro)
        self.end = Color(to)

    def __call__(self, point):
        if point <= 0:
            return self.low.hex_l
        elif point >= 1:
            return self.end.hex_l
        else:
            hsl_diff = [e - l for e, l in zip(self.end.hsl, self.low.hsl)]
            res = [l + dif * point for l, dif in zip(self.low.hsl, hsl_diff)]
            return Color(hsl=res).hex_l
