import unittest
from .colorscale import Gradient

class Gradient_Test(unittest.TestCase):

    def test_gradient_zero(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(0), '#e0ecbb')

    def test_gradient_one(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(1), '#384413')

    def test_gradient_middle(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(0.5), '#a4c738')

    def test_gradient_interpolatesLuminance(self):
        gradient = Gradient('#aa0000','#cc0000')
        self.assertEqual(gradient(0.5), '#bb0000')

    def test_gradient_interpolatesSaturation(self):
        gradient = Gradient('#aaaaaa','#ff0000')
        self.assertEqual(gradient(0.5), '#ca6060')

    def test_gradient_interpolatesHue(self):
        gradient = Gradient('#aa0000','#00aa00')
        self.assertEqual(gradient(0.5), '#aaaa00')

    def test_gradient_interpolatesHueZeroCross(self):
        gradient = Gradient('#aa0055','#aa5500')
        self.assertEqual(gradient(0.6), '#aa1100')

    def test_gradient_interpolatesHueZeroCrossBackwards(self):
        gradient = Gradient('#aa5500','#aa0055')
        self.assertEqual(gradient(0.6), '#aa0011')

    def test_gradient_underZero_clamps(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(-1), '#e0ecbb')

    def test_gradient_aboveOne_clamps(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(2), '#384413')

    def test_gradient_takesColorNames(self):
        gradient = Gradient('green', 'blue')
        self.assertEqual(gradient(0.5), '#00bfbf')


