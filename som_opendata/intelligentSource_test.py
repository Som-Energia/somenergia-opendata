# -*- coding: utf-8 -*-

import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate
from .data import (
    ExtractData,
    )
from csvSource import CsvSource
from intelligentSource import IntelligentSource


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"


class IntelligentSource_test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None

    def createSource(self, datumA, datumB):

        content = ns()
        for datum, lines in datumA.iteritems():
            content[datum] = '\n'.join(lines)
        sourceA = CsvSource(content)
        content = ns()
        for datum, lines in datumB.iteritems():
            content[datum] = '\n'.join(lines)
        sourceB = CsvSource(content)

        return IntelligentSource(sourceA, sourceB)



