import unittest
from .colorscale import greens

class ColorScale_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test_greens_zero(self):
        self.assertEqual(greens(0), '(223, 233, 194)')

    def test_greens_maxim(self):
        self.assertEqual(greens(1), '(60, 72, 20)')

    def _test_greens_inBetween(self):
        self.assertEqual(greens(0.5), '(150, 182, 52)')
