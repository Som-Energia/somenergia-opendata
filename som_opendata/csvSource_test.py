# -*- coding: utf-8 -*-

import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate
from .data import (
    ExtractData,
    )
from csvSource import CsvSource
import b2btest



headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"



class CsvSource_Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None

    def createSource(self, *lines):
        content = '\n'.join(lines)
        return CsvSource(content)


    def test__get__oneDateRequestExist(self):
        source = self.createSource(
            headers,
            data_SantJoan,
            )
        self.assertEqual(source.get('members', ['2018-01-01'], ns()), [
            [u'codi_pais', u'pais', u'codi_ccaa', u'comunitat_autonoma', u'codi_provincia', u'provincia', u'codi_ine', u'municipi', u'count_2018_01_01'],
            [u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000'],
            ])

    def test__get__oneDateRequestNoExist(self):
        source = self.createSource(
            )
        self.assertEqual(source.get('members', ['2018-01-01'], ns()),
            []
        )

    def test__get__twoDatesRequestOneExist(self):
        source = self.createSource(
            headers,
            data_SantJoan,
            )
        self.assertEqual(source.get('members', ['2018-01-01','2018-02-01'], ns()), [
            [u'codi_pais', u'pais', u'codi_ccaa', u'comunitat_autonoma', u'codi_provincia', u'provincia', u'codi_ine', u'municipi', u'count_2018_01_01'],
            [u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000'],
            ])

    @unittest.skip("Cal veure com es fan els b2b")
    def test__extractObjects__oneDateExistBackToBack(self):
        members_table = e.extractObjects('members', ['2015-01-01'], DataFromCSV())

        s = u'\n'.join(
            [u' '.join([elem for elem in row]) for row in members_table]
        ).encode('utf-8')
        self.assertB2BEqual(s)
