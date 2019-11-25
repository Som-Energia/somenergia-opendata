import unittest
from .mapscale import MapScale
class MapScale_test(unittest.TestCase):

    def test_mapscale_linear_zero(self):
        scale = MapScale(0, 1000, 'linear')
        point = scale(0)
        self.assertEqual(point, 0)
