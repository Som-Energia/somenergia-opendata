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

    def test__extractObjects__twoDatesOneExist(self):
        self.assertEqual(e.extractObjects('members', ['2018_01_01', '2018_07_01'], DataFromCSV()),
            [[u'codi_pais', u'pais', u'codi_ccaa', u'comunitat_autonoma', u'codi_provincia', u'provincia', u'codi_ine', u'municipi', u'count_2018_01_01'],
             [u'ES', u'España', u'09', u'Catalunya', u'17', u'Girona', u'17079', u'Girona', u'20'],
             [u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000']]
        )



    @unittest.skip("Cal veure com es fan els b2b")
    def test__extractObjects__oneDateExistBackToBack(self):
        members_table = e.extractObjects('members', ['2015_01_01'], DataFromCSV())

        s = u'\n'.join(
            [u' '.join([elem for elem in row]) for row in members_table]
        ).encode('utf-8')
        self.assertB2BEqual(s)
