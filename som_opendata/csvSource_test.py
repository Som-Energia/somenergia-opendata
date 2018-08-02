# -*- coding: utf-8 -*-

import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate
from .data import (
    ExtractData,
    )
from csvSource import CsvSource
import b2btest
from missingDataError import MissingDataError


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"



class CsvSource_Test(unittest.TestCase):

    from testutils import assertNsEqual 

    def setUp(self):
        self.maxDiff=None

    def createSource(self, datums):

        content = ns()
        for datum, lines in datums.iteritems():
            content[datum] = '\n'.join(lines)

        return CsvSource(content)

    def raisesAssertion(self, source, request, expected, missedDates, missedLocations):
        with self.assertRaises(MissingDataError) as ctx:
            source.get(*request)
        self.assertEquals(ctx.exception.data, expected)
        self. assertEquals(ctx.exception.missedDates, missedDates)
        self. assertEquals(ctx.exception.missedLocations, missedLocations)


    def test__get__oneDateRequestExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.assertNsEqual(
            ns(data=source.get('members', ['2018-01-01'], ns())), """\
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

    def test__get__oneDateRequestNoExist(self):
        source = self.createSource(
            ns(members=[])
            )
        self.raisesAssertion(
            source=source,
            request=['members', ['2018-01-01'], ns()],
            expected=[],
            missedDates=['2018-01-01'],
            missedLocations=None
            )

    def test__get__twoDatesRequestOneExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.raisesAssertion(
            source=source,
            request=['members', ['2018-01-01','2018-02-01'], ns()],
            expected=[
                 [u'codi_pais', u'pais', u'codi_ccaa', u'comunitat_autonoma', u'codi_provincia', u'provincia', u'codi_ine', u'municipi', u'count_2018_01_01'],
                 [u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000'],
                ],
            missedDates=['2018-02-01'],
            missedLocations=None
            )

    def test__get__filterNoExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.raisesAssertion(
            source=source,
            request=['members', ['2018-01-01'], ns(codi_ccaa=['05'])],
            expected=[],
            missedDates=None,
            missedLocations=None
            )

    def test__set__oneRow(self):
        source = self.createSource(
            ns(members=[headers,
            data_Perignan])
            )
        source.set('members',
            [[u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000']
            ]
        )
        self.assertEqual(source.data['members'],
            u'''codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01\n''' +
            u'''FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10\n''' +
            u'''ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000''')

    def test__set__twoRow(self):
        source = self.createSource(
            ns(members=[headers,
            data_Perignan])
            )
        source.set('members',
            [[u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000'],
             [u'ES', u'España', u'09', u'Catalunya', u'17', u'Girona', u'17007', u'Amer', u'2000']
            ]
        )
        self.assertEqual(source.data['members'],
            u'''codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01\n''' +
            u'''FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10\n''' +
            u'''ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000\n''' +
            u'''ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000''')



    @unittest.skip('TODO')
    def test__set__oneDate(self):
        source = self.createSource(
            headers,
            data_SantJoan,
            )
        source.set('members',
            [u'codi_pais', u'pais', u'codi_ccaa', u'comunitat_autonoma', u'codi_provincia', u'provincia', u'codi_ine', u'municipi', u'count_2018_01_01'],
            [u'ES', u'España', u'09', u'Catalunya', u'08', u'Barcelona', u'08217', u'Sant Joan Despí', u'1000']
        )
        self.assertEqual(source.data,
            u'''codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01\n''' +
            u'''FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10\n''' +
            u'''ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000''')
