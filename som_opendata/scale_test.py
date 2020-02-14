import unittest
from .scale import LinearScale, LogScale
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

    def test_nice_noChange(self):
        scale = LinearScale(higher=10000)
        scale.nice()
        self.assertEqual(scale.high, 10000)

    def test_nice_nicerHighNoAdjustment(self):
        scale = LinearScale(higher=999)
        scale.nice()
        self.assertEqual(scale.high, 1000)

    def test_nice_nicerHighAdjustmentTo20(self):
        scale = LinearScale(higher=101)
        scale.nice()
        self.assertEqual(scale.high, 200)

    def test_nice_nicerHighAdjustmentTo50(self):
        scale = LinearScale(higher=499)
        scale.nice()
        self.assertEqual(scale.high, 500)

    def test_nice_nicerLowNoAdjustment(self):
        scale = LinearScale(lower=11, higher=1000)
        scale.nice()
        self.assertEqual(scale.low, 10)

    def test_nice_nicerLowAdjustmentTo20(self):
        scale = LinearScale(lower=255, higher=1000)
        scale.nice()
        self.assertEqual(scale.low, 200)

    def test_nice_nicerLowAdjustmentTo50(self):
        scale = LinearScale(lower=550, higher=1000)
        scale.nice()
        self.assertEqual(scale.low, 500)


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

