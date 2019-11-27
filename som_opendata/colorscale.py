from colour import Color


class Gradient(object):

    def __init__(self, fro, to):
        self.fro = Color(fro)
        self.to = Color(to)

    def __call__(self, point):
        if point <= 0:
            return self.fro.hex_l
        elif point >= 1:
            return self.to.hex_l
        else:
            hsl_diff = [e - l for e, l in zip(self.to.hsl, self.fro.hsl)]
            if hsl_diff[0] > 0.5:
                hsl_diff[0] -= 1
            elif hsl_diff[0] < (-0.5):
                hsl_diff[0] += 1

            res = [l + dif * point for l, dif in zip(self.fro.hsl, hsl_diff)]
            return Color(hsl=res).hex_l
