import unittest
from .colorscale import greens

class ColorScale_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test_greens_zero(self):
        self.assertEqual(greens(0), '#e3f4d8')

    def test_greens_maxim(self):
        self.assertEqual(greens(1), '#2d5016')
