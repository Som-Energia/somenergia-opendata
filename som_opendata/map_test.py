# -*- encoding: utf8 -*-

import b2btest
import unittest
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .map import (
    dataToTemplateDict,
    fillMap,
    renderMap,
    percentRegion,
    lastDateWithData,
    requestedOrLastWithData
    )
from .colorscale import Gradient
from .csvSource import loadCsvSource, CsvSource
from future.utils import iteritems
from pathlib2 import Path

dummyTemplate=u"""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: {title}</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: {subtitle}</text>
  <text y="80" x="170" style="text-anchor:middle">Year: {year}</text>
  <text y="100" x="170" style="text-anchor:middle">Month: {month}</text>
  <circle cy="180" cx="100" r="60" fill="{color_01}"/>
  <text y="180" x="100" style="text-anchor:middle">{number_01}</text>
  <text y="200" x="100" style="text-anchor:middle">{percent_01}</text>
  <circle cy="180" cx="240" r="60" fill="{color_09}"/>
  <text y="180" x="240" style="text-anchor:middle">{number_09}</text>
  <text y="200" x="240" style="text-anchor:middle">{percent_09}</text>
</svg>
"""
headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"


class Map_Test(unittest.TestCase):

    def setUp(self):
        self.b2bdatapath = 'b2bdata'
        Path('maps/mapTemplate_dummy.svg').write_text(dummyTemplate, encoding='utf8')
        population = (u''
                'code\tname\tpopulation\n'
                '01\tAndalucía\t10000\n'
                '09\tCatalunya\t20000\n'
            )
        Path('maps/population_dummy.tsv').write_text(population,encoding='utf8')

    def tearDown(self):
        Path('maps/mapTemplate_dummy.svg').unlink()
        Path('maps/population_dummy.tsv').unlink()

    from somutils.testutils import assertNsEqual

    def test_dataToTemplateDict_noRegion(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas: {}
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
        """)

    def test_dataToTemplateDict_singleRegion(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_01: 123
            percent_01: 100,0%
            color_01: '#384413'
        """)

    def test_percentRegion_totalZero(self):
        self.assertEqual(percentRegion(0,0), '0,0%')

    def test_dataToTemplateDict_manyRegions(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [143]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
                  '09':
                    name: Catalunya
                    values: [20]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_01: 123
            percent_01: 86,0%
            color_01: '#3f4c15'
            number_09: 20
            percent_09: 14,0%
            color_09: '#8eac30'
        """)

    def test_dataToTemplateDict_restWorldHasValue(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [126]
            countries:
              ES:
                name: España
                values: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 3
            percent_00: 2,4%
            color_00: '#c5db7f'
            number_01: 123
            percent_01: 97,6%
            color_01: '#394513'
        """)

    def test_dataToTemplateDict_LinearColorScale(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [143]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
                  '09':
                    name: Catalunya
                    values: [20]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colorScale='Linear', colors=color)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_01: 123
            percent_01: 86,0%
            color_01: '#56691d'
            number_09: 20
            percent_09: 14,0%
            color_09: '#cfe296'
        """)

    def test_fillMap_(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [143]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
                  '09':
                    name: Catalunya
                    values: [20]
            """)
        self.maxDiff = None
        result = fillMap(data=data, template=dummyTemplate,
                title="un títol", subtitle="un subtítol", geolevel='ccaa')
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#3f4c15"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">86,0%</text>
  <circle cy="180" cx="240" r="60" fill="#8eac30"/>
  <text y="180" x="240" style="text-anchor:middle">20</text>
  <text y="200" x="240" style="text-anchor:middle">14,0%</text>
</svg>
""")

    def test_fillMap_withLocationList(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [143]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
            """)
        self.maxDiff = None
        result = fillMap(data=data, template=dummyTemplate,
                title="un títol", subtitle="un subtítol", locations=['01','09'], geolevel='ccaa')
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#3f4c15"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">86,0%</text>
  <circle cy="180" cx="240" r="60" fill="#e0ecbb"/>
  <text y="180" x="240" style="text-anchor:middle">0</text>
  <text y="200" x="240" style="text-anchor:middle">0,0%</text>
</svg>
""")


    def createSource(self, datums):

        content = ns()
        for datum, lines in iteritems(datums):
            content[datum] = '\n'.join(lines)

        return CsvSource(content)


    def test_lastDateWithData_(self):
        result = lastDateWithData()
        self.assertEqual(result, '2019-11-01')

    def test_requestedOrLastWithData_requested(self):
        requested = Date('2018-01-01')
        self.assertEqual(requestedOrLastWithData(requested), '2018-01-01')

    def test_requestedOrLastWithData_noDataYet(self):
        requested = Date('2020-01-01')
        self.assertEqual(requestedOrLastWithData(requested), '2019-11-01')

    def test_requestedOrLastWithData_equals(self):
        requested = Date('2019-11-01')
        self.assertEqual(requestedOrLastWithData(requested), '2019-11-01')

    def test_requestedOrLastWithData_None(self):
        self.assertEqual(requestedOrLastWithData(None), lastDateWithData())
    def test_renderMap_(self):
        self.maxDiff = None
        source = self.createSource(
            ns(members=[
                headers,
                data_Girona,
                data_Adra,
                ])
            )

        result = renderMap(source, 'members', '2018-01-01', geolevel='dummy')

        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: </text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#c5dc80"/>
  <text y="180" x="100" style="text-anchor:middle">2</text>
  <text y="200" x="100" style="text-anchor:middle">9,1%</text>
  <circle cy="180" cx="240" r="60" fill="#3f4c15"/>
  <text y="180" x="240" style="text-anchor:middle">20</text>
  <text y="200" x="240" style="text-anchor:middle">90,9%</text>
</svg>
""")

    def test_renderMap_missingLocation(self):
        self.maxDiff = None
        source = self.createSource(
            ns(members=[
                headers,
                data_Adra,
                ])
            )

        result = renderMap(source, 'members', '2018-01-01', geolevel='dummy')

        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: </text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#384413"/>
  <text y="180" x="100" style="text-anchor:middle">2</text>
  <text y="200" x="100" style="text-anchor:middle">100,0%</text>
  <circle cy="180" cx="240" r="60" fill="#e0ecbb"/>
  <text y="180" x="240" style="text-anchor:middle">0</text>
  <text y="200" x="240" style="text-anchor:middle">0,0%</text>
</svg>
""")

    def test_renderMap_members(self):
        source = loadCsvSource()
        result = renderMap(source, 'members', '2019-01-01', geolevel='ccaa')
        self.assertB2BEqual(result)

    def test_renderMap_members_defaultDate(self):
        source = loadCsvSource()
        result = renderMap(source, 'members', None, geolevel='ccaa')
        expected = renderMap(source, 'members', '2019-11-01', 'ccaa')
        self.assertMultiLineEqual(result, expected)

    def test_renderMap_contracts(self):
        source = loadCsvSource()
        result = renderMap(source, 'contracts', '2019-01-01', geolevel='ccaa')
        self.assertB2BEqual(result)

    def test_dataToTemplateDict_singleCounty(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [1969]
            countries:
              ES:
                name: España
                values: [1969]
                ccaas:
                  '01':
                    name: Andalucia
                    values:
                      - 1969
                    states:
                      '11':
                        name: Cádiz
                        values:
                          - 1969
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, geolevel='state')

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_11: 1969
            percent_11: 100,0%
            color_11: '#384413'
        """)

    def test_dataToTemplateDict_noCounty(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [1969]
            countries:
              ES:
                name: España
                values: [1969]
                ccaas:
                  '01':
                    name: Andalucia
                    values:
                      - 1969
                    states: {}
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, geolevel='state')

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
        """)

    def test_dataToTemplateDict_twoCounties(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [750]
            countries:
              ES:
                name: España
                values: [750]
                ccaas:
                  '01':
                    name: Andalucia
                    values:
                      - 750
                    states:
                      '11':
                        name: Cádiz
                        values:
                          - 500
                      '14':
                        name: Córdoba
                        values:
                          - 250
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, geolevel='state')

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_11: 500
            percent_11: 66,7%
            color_11: '#455417'
            number_14: 250
            percent_14: 33,3%
            color_14: '#5c701f'
        """)

    def test_dataToTemplateDict_twoCountiesDifCCAA(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [750]
            countries:
                ES:
                  name: España
                  values:
                  - 750
                  ccaas:
                    '01':
                      name: Andalucia
                      values: [500]
                      states:
                        '11':
                          name: Cádiz
                          values:
                          - 500
                    '09':
                      name: Catalunya
                      values: [250]
                      states:
                        '43':
                          name: Tarragona
                          values:
                            - 250
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, geolevel='state')

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_11: 500
            percent_11: 66,7%
            color_11: '#455417'
            number_43: 250
            percent_43: 33,3%
            color_43: '#5c701f'
        """)

    def test_renderMap_members_byState(self):
        source = loadCsvSource()
        result = renderMap(source, 'members', '2019-11-01', geolevel='state')
        self.assertB2BEqual(result)
