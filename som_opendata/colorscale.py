def greens(point):
    lower =  [223,233,194]
    higher = [60,72,20]
    if not point:
        return '({})'.format(str(lower).strip('[').strip(']'))
    else:
       
        return '({})'.format(str(higher).strip('[').strip(']'))
