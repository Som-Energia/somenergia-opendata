def greens(point):
    lower = int('e3f4d8',16)
    higher = int('2d5016',16)
    if not point:
        return '#{}'.format(hex(lower).strip('0x'))
    else:
        return '#{}'.format(hex(higher).strip('0x'))