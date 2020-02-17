import unittest
from .scale import LinearScale, LogScale, niceCeilValue, niceFloorValue
from somutils import testutils


class LinearScale_Test(unittest.TestCase):

    def test_call_min(self):
        scale = LinearScale(0, 1000)
        self.assertEqual(scale(0), 0)

    def test_call_max(self):
        scale = LinearScale(0, 1000)
        self.assertEqual(scale(1000), 1)

    def test_call_middle(self):
        scale = LinearScale(500, 1000)
        self.assertEqual(scale(750), 0.5)

    def test_call_outRangeLow(self):
        scale = LinearScale(0, 100)
        self.assertEqual(scale(-25), -0.25)

    def test_call_outRangeHigh(self):
        scale = LinearScale(0, 100)
        self.assertEqual(scale(125), 1.25)

    def test_call_minEqualMax(self):
        scale = LinearScale(100, 100)
        self.assertEqual(scale(100), 1)

    def test_inverse_min(self):
        scale = LinearScale()
        self.assertEqual(scale(scale.inverse(0)), 0)

    def test_inverse_max(self):
        scale = LinearScale(higher=100)
        self.assertEqual(scale(scale.inverse(1)),1)

    def test_inverse_midle(self):
        scale = LinearScale()
        self.assertEqual(scale(scale.inverse(0.5)),0.5)

    def test_inverse_outRange(self):
        scale = LinearScale()
        self.assertEqual(scale(scale.inverse(-0.25)), -0.25)
        self.assertEqual(scale(scale.inverse(1.25)), 1.25)

    def test_inverse_min_set(self):
        scale = LinearScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(0)), 0)

    def test_inverse_max_set(self):
        scale = LinearScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(1)), 1)

    def test_inverse_midlle_setMin(self):
        scale = LinearScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(0.5)),0.5)

    def test_inverse_outRange_minSet(self):
        scale = LinearScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(-0.25)), -0.25)
        self.assertEqual(scale(scale.inverse(1.25)), 1.25)

    def test_call_wayDown(self):
        scale = LinearScale(lower=100, higher=0)
        self.assertEqual(scale(75), .25)

    def test_inverse_wayDown(self):
        scale = LinearScale(lower=100, higher=0)
        self.assertEqual(scale.inverse(.25), 75)

    def test_niceCeilValue_adjustmentTo10n(self):
        self.assertEqual(niceCeilValue(999), 1000)

    def test_niceCeilValue_adjustmentTo2x10n(self):
        self.assertEqual(niceCeilValue(101), 200)

    def test_niceCeilValue_adjustmentTo5x10n(self):
        self.assertEqual(niceCeilValue(499), 500)

    def test_niceFloorValue_adjustmentTo10n(self):
        self.assertEqual(niceFloorValue(11), 10)

    def test_niceFloorValue_adjustmentTo2x10n(self):
        self.assertEqual(niceFloorValue(255), 200)

    def test_niceFloorValue_adjustmentTo5x10n(self):
        self.assertEqual(niceFloorValue(550), 500)

    def test_nice_noChange(self):
        scale = LinearScale(higher=10000)
        scale.nice()
        self.assertEqual(scale.high, 10000)

    def test_nice_lowHighAdjustment(self):
        scale = LinearScale(lower=23, higher=835)
        scale.nice()
        self.assertEqual(scale.low, 20)
        self.assertEqual(scale.high, 1000)

    def test_ticks_defaultCount(self):
        scale = LinearScale(higher=1000)
        self.assertEqual(scale.ticks(), [0, 250, 500, 750, 1000])

    def test_ticks_lowerSet(self):
        scale = LinearScale(lower= 200, higher=1000)
        self.assertEqual(scale.ticks(), [200, 400, 600, 800, 1000])

    def test_ticks_8count(self):
        scale = LinearScale(higher=2000)
        self.assertEqual(scale.ticks(8), [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000])


class LogScale_Test(unittest.TestCase):

    def test_call_min(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(100), 0)

    def test_call_max(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(10000), 1)

    def test_call_middle(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(1000), 0.5)

    def test_call_outRangeLow(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(-1), 0)

    def test_call_outRangeHigh(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(100000), 1.5)
    def test_inverse_min(self):
        scale = LogScale(higher=1000)
        self.assertEqual(scale(scale.inverse(0)), 0)

    def test_inverse_max(self):
        scale = LogScale(higher=1000)
        self.assertEqual(scale(scale.inverse(1)), 1)

    def test_inverse_middle(self):
        scale = LogScale(higher=1000)
        self.assertEqual(scale(scale.inverse(0.5)), 0.5)

    def test_inverse_outRange(self):
        scale = LogScale(higher=1000)
        self.assertEqual(scale(scale.inverse(-0.25)), -0.25)
        self.assertEqual(scale(scale.inverse(1.25)), 1.25)

    def test_inverse_min_setMin(self):
        scale = LogScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(0)), 0)

    def test_inverse_middle_setMin(self):
        scale = LogScale(lower=100, higher=1000)
        self.assertEqual(scale(scale.inverse(0.5)), 0.5)

    def test_inverse_outRange_setMin(self):
        scale = LogScale(higher=1000)
        self.assertEqual(scale(scale.inverse(-0.25)), -0.25)
        self.assertEqual(scale(scale.inverse(1.25)), 1.25)

    def test_call_minGreaterMax(self):
        with self.assertRaises(ValueError) as context:
            LogScale(lower=1000, higher=10)
        self.assertEqual(
            "Lower value is greater than higher value",
            str(context.exception)
        )

    def test_call_scaleStartNotValid(self):
        with self.assertRaises(ValueError) as context:
            LogScale(lower=0, higher=10)
        self.assertEqual(
            "Log not defined for values <= 0",
            str(context.exception)
        )

# TODO: Negative max and min in log
# TODO: Fail on diferent sign log
# TODO: Inverted limits log
# TODO: Inverted limits linear

