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

    def test_gradient_underZero_clamps(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(-1), '#e0ecbb')

    def test_gradient_aboveOne_clamps(self):
        gradient = Gradient('#e0ecbb','#384413')
        self.assertEqual(gradient(2), '#384413')

    def test_gradient_reverseHueWay(self):
        gradient = Gradient('#bf4040', '#a640bf')
        self.assertEqual(gradient(0.5), '#bf408c')

    def test_gradient_takesColorNames(self):
        gradient = Gradient('green', 'blue')
        self.assertEqual(gradient(0.5), '#00bfbf')
