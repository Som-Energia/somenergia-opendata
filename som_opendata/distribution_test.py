# -*- coding: utf-8 -*-
import unittest
from distribution import parse_tsv

class Distribution_Test(unittest.TestCase):
    

    def test__parse_tsv(self):
        fixture = 'item'
        self.assertEqual(parse_tsv(fixture), [['item']])




# vim: et sw=4 ts=4