# -*- coding: utf-8 -*-

import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate

from csvSource import CsvSource
from intelligentSource import IntelligentSource


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"


class IntelligentSource_test(unittest.TestCase):

    from testutils import assertNsEqual

    def setUp(self):
        self.maxDiff=None

    def createSource(self, firstDatum, secondDatum):

        content = ns()
        for datum, lines in firstDatum.iteritems():
            content[datum] = '\n'.join(lines)
        firstSource = CsvSource(content)
        content = ns()
        for datum, lines in secondDatum.iteritems():
            content[datum] = '\n'.join(lines)
        secondSource = CsvSource(content)

        return IntelligentSource(firstSource, secondSource)


    def test__get__firstSourceResponse(self):
        source = self.createSource(
            ns(members=[headers, data_SantJoan]),
            ns(members=[headers, data_Perignan]),
        )
        result = source.get('members', ['2018-01-01'], ns())
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '09'
              comunitat_autonoma: Catalunya
              codi_provincia: '08'
              provincia: Barcelona
              codi_ine: '08217'
              municipi: Sant Joan Despí
              count_2018_01_01: '1000'
        """)

    def test__get__secondSourceResponse(self):
        source = self.createSource(
            ns(members=[
                headers,
                data_SantJoan
            ]),
            ns(members=[
                headers+'\tcount_2018_02_01',
                data_SantJoan+'\t201'
            ]),
        )
        result = source.get('members', ['2018-02-01'], ns())
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '09'
              comunitat_autonoma: Catalunya
              codi_provincia: '08'
              provincia: Barcelona
              codi_ine: '08217'
              municipi: Sant Joan Despí
              count_2018_02_01: '201'
        """)

    def test__get__combineSourceResponse(self):
        source = self.createSource(
            ns(members=[
                headers,
                data_SantJoan
            ]),
            ns(members=[
                headers+'\tcount_2018_02_01',
                data_SantJoan+'\t201'
            ]),
        )
        result = source.get('members', ['2018-01-01', '2018-02-01'], ns())
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '09'
              comunitat_autonoma: Catalunya
              codi_provincia: '08'
              provincia: Barcelona
              codi_ine: '08217'
              municipi: Sant Joan Despí
              count_2018_01_01: '1000'
              count_2018_02_01: '201'
        """)



    @unittest.skip('TODO')
    def test__get__failedAllSources(self):
        source = self.createSource(
            ns(members=[
                headers,
                data_SantJoan
            ]),
            ns(members=[
                headers,
                data_SantJoan
            ]),
        )
        result = source.get('members', ['2018-02-01'], ns())
        self.assertNsEqual(ns(data=result), """\
            data:S
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '09'
              comunitat_autonoma: Catalunya
              codi_provincia: '08'
              provincia: Barcelona
              codi_ine: '08217'
              municipi: Sant Joan Despí
              count_2018_02_01: '201'
        """)


    def test__set__updateFristSource(self):
        source = self.createSource(
            ns(members=[
                headers,
                data_SantJoan
            ]),
            ns(members=[
                headers+'\tcount_2018_02_01',
                data_SantJoan+'\t201'
            ]),
        )
        source.get('members', ['2018-01-01', '2018-02-01'], ns())
        self.assertEqual(source.sources[0].data['members'],
            u'''codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01\tcount_2018_02_01\n''' +
            u'''ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000\t201''')
