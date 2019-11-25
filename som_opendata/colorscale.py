def greens(point):
    lower = [223, 233, 194]
    middle = [150, 182, 52]
    higher = [60, 72, 20]
    rangeDarker =[m - h for m, h in zip(middle, higher)]
    rangeBrighter = [l - m for l, m in zip(lower, middle)]

    if point < 0.5:
        val = [l - round(rBrig * point / 2)
                for l, rBrig in zip(lower, rangeBrighter)]
        return '({})'.format(str(val).strip('[').strip(']'))
    else:
        newPoint = (point - 0.5) * 2
        val = [m - round(rDark * newPoint)
                for m, rDark in zip(middle, rangeDarker)]
        return '({})'.format(str(val).strip('[').strip(']'))
