import unittest
from .mapscale import Scale
from somutils import testutils

class Scale_test(unittest.TestCase):

    def test_scale_min(self):
        scale = Scale(0, 1000)
        self.assertEqual(scale(0), 0)

    def test_scale_max(self):
        scale = Scale(0, 1000)
        self.assertEqual(scale(1000), 1)

    def test_scale_middle(self):
        scale = Scale(0,1000)
        self.assertEqual(scale(500), 0.5)

    def test_scale_outRangeLow(self):
        scale = Scale(0,100)
        self.assertEqual(scale(-25), -0.25)

    def test_scale_outRangeHigh(self):
        scale = Scale(0,100)
        self.assertEqual(scale(125), 1.25)