import unittest
from .mapscale import Scale
class Scale_test(unittest.TestCase):

    def test_scale_min(self):
        scale = Scale(0, 1000)
        point = scale(0)
        self.assertEqual(point, 0)

    def _test_scale_max(self):
        scale = Scale(0, 1000)
        point = scale(1000)
        self.assertEqual(point, 1)
