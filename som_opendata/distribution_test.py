# -*- coding: utf-8 -*-
import unittest
from distribution import (
    parse_tsv,
    tuples2objects,
    )
from yamlns import namespace as ns

class Distribution_Test(unittest.TestCase):
    
    def test__parse_tsv__1col_1row(self):
        fixture = 'item'
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__2col_1row(self):
        fixture = 'item1\titem2'
        self.assertEqual(parse_tsv(fixture), [['item1', 'item2']])


    def test__parse_tsv__1col_2row(self):
        fixture = 'item1\nitem2'
        self.assertEqual(parse_tsv(fixture), [['item1'],['item2']])


    def test__parse_tsv__empty_line_ignored(self):
        fixture = 'item\n'
        self.assertEqual(parse_tsv(fixture), [['item']])



    def test__parse_tsv__line_with_spaces_ignored(self):
        fixture = 'item\n  '
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__fields_are_stripped(self):
        fixture = '  item  '
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__fields_are_really_stripped(self):
        fixture = '  item1  \t item2  '
        self.assertEqual(parse_tsv(fixture), [['item1', 'item2']])


    from testutils import assertNsEqual 
    
    def test__tuple2object__1value_1attribute(self):
        fixture = parse_tsv(
            'name\n'
            'value\n'
            )
        self.assertNsEqual(tuples2objects(fixture), ns(name='value'))


# vim: et sw=4 ts=4