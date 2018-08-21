# -*- coding: utf-8 -*-
import b2btest
import unittest
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns
from csvSource import CsvSource
from missingDateError import MissingDateError



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
        self.b2bdatapath = 'b2bdata'

    def createSource(self, datums):

        content = ns()
        for datum, lines in datums.iteritems():
            content[datum] = '\n'.join(lines)

        return CsvSource(content)

    def raisesAssertion(self, source, datum, dates, missingDates):
        with self.assertRaises(MissingDateError) as ctx:
            source.get(datum=datum, dates=dates, filters=ns())

        self. assertEquals(ctx.exception.missingDates, missingDates)


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
            ns(members=[headers,
            data_SantJoan])
            )
        self.raisesAssertion(
            source=source,
            datum='members',
            dates=['2018-02-01'],
            missingDates=['2018-02-01'],
            )

    def test__get__twoDatesRequestOneExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.raisesAssertion(
            source=source,
            datum='members',
            dates=['2018-01-01','2018-02-01'],
            missingDates=['2018-02-01'],
            )

    def test__get__filterExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.assertNsEqual(
            ns(data=source.get('members', ['2018-01-01'], ns(codi_pais=['ES']))), """\
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

    def test__get__filterNotExist(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        self.assertEqual(
            source.get('members', ['2018-01-01'], ns(codi_pais=['PA'])),
                []
            )



    def test__set__oneDate(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        source.update('members',
            [ns(codi_pais=u'ES',
                pais=u'España',
                codi_ccaa=u'09',
                comunitat_autonoma=u'Catalunya',
                codi_provincia=u'08',
                provincia=u'Barcelona',
                codi_ine=u'08217',
                municipi=u'Sant Joan Despí',
                count_2018_02_01=u'201')]
        )
        self.assertNsEqual(ns(data=source._objects['members']), """
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

    def test__set__oneDateWithNewCity(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        source.update('members',
            [ns(codi_pais=u'ES',
                pais=u'España',
                codi_ccaa=u'09',
                comunitat_autonoma=u'Catalunya',
                codi_provincia=u'08',
                provincia=u'Barcelona',
                codi_ine=u'08217',
                municipi=u'Sant Joan Despí',
                count_2018_02_01=u'201'),
            ns(codi_pais=u'ES',
                pais=u'España',
                codi_ccaa=u'09',
                comunitat_autonoma=u'Catalunya',
                codi_provincia=u'17',
                provincia=u'Girona',
                codi_ine=u'17007',
                municipi=u'Amer',
                count_2018_02_01=u'2001')]
        )
        self.assertNsEqual(ns(data=source._objects['members']), """
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
            - municipi: Amer
              codi_ccaa: '09'
              provincia: Girona
              codi_pais: ES
              codi_ine: '17007'
              comunitat_autonoma: Catalunya
              codi_provincia: '17'
              pais: 'España'
              count_2018_02_01: '2001'
              count_2018_01_01: '0'
        """)

    def test__get__readCsvFile(self):
        rows = []
        with open('./b2bdata/som_opendata.api_test.BaseApi_Test.test_contracts_series-expected') as f:
            for line in f:
                rows.append(line.strip('\n'))
        f.close()
        
        source = self.createSource(
            ns(contracts=rows)
        )
        result = source.get('contracts', ['2015-01-01'], ns(codi_ine='17066'))
        self.assertNsEqual(ns(data=result), """
            data:
            - codi_pais: ES
              pais: España
              codi_ccaa: 09
              comunitat_autonoma: Cataluña
              codi_provincia: '17'
              provincia: Girona
              codi_ine: '17066'
              municipi: Figueres
              count_2015_01_01: '31'
            """)
        
