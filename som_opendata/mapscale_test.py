import unittest
from .mapscale import MapScale
class MapScale_test(unittest.TestCase):

    def test_mapscale_linear_min(self):
        scale = MapScale(1, 1000, 'linear')
        point = scale(1)
        self.assertEqual(point, 0)

    def test_mapscale_linear_max(self):
        scale = MapScale(1, 1000, 'linear')
        point = scale(1000)
        self.assertEqual(point, 1)
