# -*- coding: utf-8 -*-
import b2btest
import unittest
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns
from .csvSource import CsvSource
from .errors import MissingDateError
from future.utils import iteritems


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"

data_Andalucia = (
    'Andalucia', ns(
        name = "Andalucía",
        alias = ns(
            ccaa = [
                '01', # Andalucía
            ],
        ),
    )
)
data_BaixMontseny = (
    'BaixMontseny', ns(
        name = "Baix Montseny",
        alias = ns(
            city = [
                '08097', # Gualba
                '17027', # Breda
            ],
        ),
    )
)
data_BaixLlobregat = (
    'BaixLlobregat', ns(
        name = "Baix Llobregat",
        alias = ns(
            city = [
                '08217', # Sant Joan Despi
            ],
        ),
    )
)


class CsvSource_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def setUp(self):
        self.maxDiff=None
        self.b2bdatapath = 'b2bdata'

    def createSource(self, datums, aliases=ns()):

        content = ns()
        for datum, lines in iteritems(datums):
            content[datum] = '\n'.join(lines)
        return CsvSource(content, aliases)

    def raisesAssertion(self, source, datum, dates, missingDates):
        with self.assertRaises(MissingDateError) as ctx:
            source.get(datum=datum, dates=dates, filters=ns())

        self. assertEqual(ctx.exception.missingDates, missingDates)


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
        self.assertEqual(source.getLastDay('members'), '2018-02-01')

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
        self.assertEqual(source.getLastDay('members'), '2018-02-01')

    def test_update_unmodifiedLastDay(self):
        source = self.createSource(
            ns(members=[headers,
            data_SantJoan])
            )
        source.update('members',
            [ns(codi_pais=u'ES',
                pais=u'España',
                codi_ccaa=u'09',
                comunitat_autonoma=u'Catalunya',
                codi_provincia=u'17',
                provincia=u'Girona',
                codi_ine=u'17007',
                municipi=u'Amer')]
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
            - municipi: Amer
              codi_ccaa: '09'
              provincia: Girona
              codi_pais: ES
              codi_ine: '17007'
              comunitat_autonoma: Catalunya
              codi_provincia: '17'
              pais: 'España'
              count_2018_01_01: '0'
        """)
        self.assertEqual(source.getLastDay('members'), '2018-01-01')


    def test__get__readCsvFile(self):
        rows = []
        with open('./b2bdata/som_opendata.oldapi_test.BaseApi_Test.test_contracts_series-expected') as f:
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
              count_2015_02_01: '30'
              count_2015_03_01: '32'
              count_2015_04_01: '32'
            """)


    def test__getLastDay(self):
        source = self.createSource(
            ns(members=[headers+'\tcount_2018_02_01',
            data_SantJoan+'\t10'])
            )
        r = source.getLastDay('members')
        self.assertEqual(r, '2018-02-01')

    def test__geolevelOptions_single(self):
        source = self.createSource(
            ns(contracts=[headers,
                data_SantJoan])
            )
        self.assertNsEqual(source.geolevelOptions('ccaa'),"""
            '09': Catalunya
        """)

    def test__geolevelOptions_many(self):
        source = self.createSource(
            ns(contracts=[headers,
                data_SantJoan,
                data_Adra,
                ])
            )
        self.assertNsEqual(source.geolevelOptions('ccaa'),"""
            '01': Andalucía
            '09': Catalunya
        """)

    def test__geolevelOptions_repeated(self):
        source = self.createSource(
            ns(contracts=[headers,
                data_SantJoan,
                data_Girona,
                ])
            )
        self.assertNsEqual(source.geolevelOptions('ccaa'),"""
            '09': Catalunya
        """)

    def test__geolevelOptions_mergesSources(self):
        source = self.createSource(ns(
            contracts=[headers,
                data_SantJoan,
            ],
            members=[headers,
                data_Adra,
            ],
        ))
        self.assertNsEqual(source.geolevelOptions('ccaa'),"""
            '01': Andalucía
            '09': Catalunya
        """)


    def test__geolevelOptions_differentGeolevel(self):
        source = self.createSource(ns(
            contracts=[headers,
                data_SantJoan,
                data_Adra,
            ],
        ))
        self.assertNsEqual(source.geolevelOptions('state'),"""
            '04': Almería
            '08': Barcelona
        """)

    # TODO: launch error
    def test__geolevelOptions_badLevel(self):
        source = self.createSource(ns(
            contracts=[headers,
                data_SantJoan,
                data_Adra,
            ],
        ))
        self.assertNsEqual(source.geolevelOptions('bad_geolevel_name'),"""
            {}
        """)

    def test__geolevelOptions_withFilter(self):
        source = self.createSource(ns(
            contracts=[headers,
                data_SantJoan,
                data_Adra,
            ],
        ))
        self.assertNsEqual(source.geolevelOptions('state', codi_ccaa=['09']),"""
            '08': Barcelona
        """)


    def test__geolevelOptions_alias(self):
        source = self.createSource(
            ns(
                contracts=[headers,
                    data_SantJoan,
                    data_Adra,
            ]),
            aliases=ns(localgroup=ns([
                data_BaixLlobregat,
                data_BaixMontseny,
            ])),
        )
        self.assertNsEqual(source.geolevelOptions('localgroup'),"""
            BaixLlobregat: Baix Llobregat
            BaixMontseny: Baix Montseny
        """)


    def test_translateFilter_whenEmpty(self):
        source = self.createSource(
            ns(
                contracts=[headers,
                    data_SantJoan,
                    data_Adra,
            ]),
        )
        translated = source.translateFilter()
        self.assertNsEqual(translated, """
            {}
        """)

    # TODO: Should it fail?
    def test_translateFilter_unknownGeolevel(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            notageolevel=[
                'value',
                ]
            )
        self.assertNsEqual(translated, """
            {}
        """)

    def test_translateFilter_oneGeoLevel(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            city=[
                'city1',
                'city2',
                ],
            )
        self.assertNsEqual(translated, """
            codi_ine:
            - city1
            - city2
        """)

    def test_translateFilter_state(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            state=[
                'state1',
                'state2',
                ],
            )
        self.assertNsEqual(translated, """
            codi_provincia:
            - state1
            - state2
        """)

    def test_translateFilter_manyGeoLevel(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            city=[
                'city1',
                'city2',
                ],
            state=[
                'state1',
                'state2',
                ],
            )
        self.assertNsEqual(translated, """
            codi_ine:
            - city1
            - city2
            codi_provincia:
            - state1
            - state2
        """)

    def test_translateFilter_ccaa(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            ccaa=[
                'ccaa1',
                'ccaa2',
                ],
            )
        self.assertNsEqual(translated, """
            codi_ccaa:
            - ccaa1
            - ccaa2
        """)

    def test_translateFilter_country(self):
        source = self.createSource(ns())
        translated = source.translateFilter(
            country=[
                'AA',
                'BB',
                ],
            )
        self.assertNsEqual(translated, """
            codi_pais:
            - AA
            - BB
        """)


# vim: et sw=4 ts=4
