from __future__ import division
from math import log10, ceil, floor


def niceFloorValue(value, allowedMultiples=[1, 2, 5]):
    if value == 0:
        return value

    niceLow = int(10 ** floor(log10(value)))
    for val in sorted(allowedMultiples, reverse=True):
        if niceLow * val <= value:
            return int(niceLow * val)


    return niceLow

def niceCeilValue(value, allowedDivisors=[1, 2, 5]):
    niceHigh = 10 ** ceil(log10(value))
    for val in sorted(allowedDivisors, reverse=True):
        if niceHigh / val >= value:
            return int(niceHigh / val)

class LinearScale(object):

    def __init__(self, lower=0, higher=100):
        self.low = lower
        self.high = higher

    def __call__(self, val):
        if self.low == self.high:
            return 1
        return (val - self.low) / (self.high - self.low)

    def inverse(self, val):
        return self.low + val * (self.high - self.low)

    def nice(self):
        self.high = niceCeilValue(self.high)
        self.low = niceFloorValue(self.low)
        return self

    def ticks(self, count=4):

        stepValue = int((self.high - self.low) / count)
        niceStepFloor = niceFloorValue(stepValue, allowedMultiples=[1, 2, 2.5, 5, 7.5])
        niceStepCeil = niceCeilValue(stepValue, allowedDivisors=[1, 2, 4, 5])

        if abs(stepValue - niceStepFloor) < abs(stepValue - niceStepCeil):
            stepValue = niceStepFloor
        else:
            stepValue = niceStepCeil

        ticks = {self.low, self.high}
        nextTick = self.low + stepValue
        for step in range(count):
            if nextTick > self.high:
                break
            ticks.add(nextTick)
            nextTick = nextTick + stepValue
        result = list(ticks)
        return sorted(result)


class LogScale(object):

    def __init__(self, higher, lower=1):
        if higher * lower < 0:
            raise ValueError("Lower and higher must have same sign")

        if higher * lower == 0:
            raise ValueError("Math domain error: Log(0) not defined")

        self.low = lower
        self.high = higher

    def __call__(self, val):
        if val * self.high < 0:
            raise ValueError("Value must have same sign as lower and higher")

        if val == 0:
            val = 10**(-10)
            if val * self.low < 0:
                val *= -1

        return log10(val / self.low) / log10(self.high / self.low)

    def inverse(self, val):
        return self.low * (self.high / self.low) ** val

    def nice(self):
        self.low = niceFloorValue(self.low)
        self.high = niceCeilValue(self.high)
        return self

    def ticks(self, count=4):
        ticks = {self.low, self.high}

        for i in [step / count for step in range(1, count)]:
            value = self.inverse(i)
            ticks.add(niceFloorValue(value))

        return sorted(list(ticks))
