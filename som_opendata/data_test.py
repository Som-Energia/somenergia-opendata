# -*- coding: utf-8 -*-
import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate
from .data import (
    ExtractData,
    )
from datafromcsv import DataFromCSV
import b2btest


e = ExtractData()

class Data_Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None
        self.b2bdatapath = 'b2bdata'


    def test__extractObjects__oneDateNoExist(self):
        self.assertEqual(e.extractObjects('members', ['2018_07_01'], DataFromCSV()),
            []
        )

    def test__extractObjects__oneDateExist(self):
        members_table = e.extractObjects('members', ['2015_01_01'], DataFromCSV())

        s = u'\n'.join(
            [u' '.join([elem for elem in row]) for row in members_table]
        ).encode('utf-8')
        self.assertB2BEqual(s)
