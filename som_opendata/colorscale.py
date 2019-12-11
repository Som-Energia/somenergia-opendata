from colour import Color


class Gradient(object):
    """
    A Gradient interpolates between two colors in HSL space.
	Colors are any text representing a web color:
	'navyblue', '#fafe40'...

    Input values are clamped into the 0 to 1 interval.

	>>> gradient = Gradient('red', '#00F')
	>>> gradient(0.0)
	'#ff0000'
	>>> gradient(1.0)
	'#0000ff'
	>>> gradient(0.5)
	'#ff00ff'
    """

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
