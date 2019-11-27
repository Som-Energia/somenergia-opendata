import unittest
from .mapscale import LinearScale, LogScale
from somutils import testutils

class Scale_test(unittest.TestCase):

    def test_LinearScale_min(self):
        scale = LinearScale(0, 1000)
        self.assertEqual(scale(0), 0)

    def test_LinearScale_max(self):
        scale = LinearScale(0, 1000)
        self.assertEqual(scale(1000), 1)

    def test_LinearScale_middle(self):
        scale = LinearScale(500, 1000)
        self.assertEqual(scale(750), 0.5)

    def test_LinearScale_outRangeLow(self):
        scale = LinearScale(0, 100)
        self.assertEqual(scale(-25), -0.25)

    def test_LinearScale_outRangeHigh(self):
        scale = LinearScale(0, 100)
        self.assertEqual(scale(125), 1.25)

    def test_LinearScale_minEqualMax(self):
        scale = LinearScale(100, 100)
        self.assertEqual(scale(100), 1)

    def test_logScale_min(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(100), 0)

    def test_logScale_max(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(10000), 1)

    def test_logScale_middle(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(1000), 0.5)

    def test_logScale_outRangeLow(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(-1), 0)

    def test_logScale_outRangeHigh(self):
        scale = LogScale(lower=100, higher=10000)
        self.assertEqual(scale(100000), 1.5)

    def test_inverseLin_min(self):
        scale = LinearScale()
        self.assertEqual(scale(scale.inverse(0)), 0)

    def test_inverseLin_max(self):
        scale = LinearScale(higher=100)
        self.assertEqual(scale(scale.inverse(1)),1)

    def test_inverseLin_midlle(self):
        scale = LinearScale()
        self.assertEqual(scale(scale.inverse(0.5)),0.5)        