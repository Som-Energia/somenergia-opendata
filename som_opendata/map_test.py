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
    maxValue,
    toPopulationRelative,
    fillLegend,
    )
from .colorscale import Gradient
from .scale import LogScale, LinearScale
from .csvSource import loadCsvSource, CsvSource
from future.utils import iteritems
from pathlib2 import Path
from .distribution import parse_tsv, tuples2objects


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

fullData = ns.loads("""\
    dates:
    - 2019-11-01
    values:
    - 3208
    countries:
      ES:
        name: España
        values:
        - 3208
        ccaas:
          '01':
            name: Andalucia
            values:
            - 48
          '02':
            name: Aragón
            values:
            - 124
          '03':
            name: Asturias, Principado de
            values:
            - 13
          '04':
            name: Baleares, Islas
            values:
            - 235
          '05':
            name: Canarias
            values:
            - 0
          '06':
            name: Cantabria
            values:
            - 12
          08:
            name: Castilla - La Mancha
            values:
            - 28
          '07':
            name: Castilla y León
            values:
            - 24
          09:
            name: Cataluña
            values:
            - 2054
          '10':
            name: Comunidad Valenciana
            values:
            - 224
          '11':
            name: Extremadura
            values:
            - 14
          '12':
            name: Galicia
            values:
            - 24
          '13':
            name: Madrid, Comunidad de
            values:
            - 145
          '14':
            name: Murcia, Región de
            values:
            - 11
          '15':
            name: Navarra, Comunidad Foral de
            values:
            - 151
          '16':
            name: País Vasco
            values:
            - 53
          '17':
            name: Rioja, La
            values:
            - 37
          '18':
            name: Ceuta
            values:
            - 5
          '19':
            name: Melilla
            values:
            - 5
""")
headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"

noRegion = ns.loads("""\
    dates: [2019-01-01]
    values: [123]
    countries:
      ES:
        name: España
        values: [123]
        ccaas: {}
    """)

singleRegion = ns.loads("""\
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

manyRegions = ns.loads("""\
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
singleState = ns.loads("""\
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
noState = ns.loads("""\
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
manyStates = ns.loads("""\
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
manyStatesDifferentCCAA = ns.loads("""\
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

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=noRegion, colors=color,maxVal=123)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 123
            legendNumber_25: 3
            legendNumber_50: 11
            legendNumber_75: 36
        """)

    def test_dataToTemplateDict_singleRegion(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=singleRegion, colors=color,maxVal=123)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 123
            legendNumber_25: 3
            legendNumber_50: 11
            legendNumber_75: 36
        """)

    def test_percentRegion_totalZero(self):
        self.assertEqual(percentRegion(0,0), '0,0%')

    def test_dataToTemplateDict_manyRegions(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colors=color, maxVal=143)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 143
            legendNumber_25: 3
            legendNumber_50: 11
            legendNumber_75: 41
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
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, maxVal=126)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 126
            legendNumber_25: 3
            legendNumber_50: 11
            legendNumber_75: 37

        """)

    def test_dataToTemplateDict_LinearColorScale(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colorScale='Linear', colors=color, maxVal=143)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 0
            legendNumber_100: 143
            legendNumber_25: 35
            legendNumber_50: 71
            legendNumber_75: 107
        """)

    def test_fillMap_manyRegions(self):

        self.maxDiff = None
        result = fillMap(data=manyRegions, template=dummyTemplate,
                title="un títol", subtitle="un subtítol", geolevel='ccaa', maxVal=143)
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

        self.maxDiff = None
        result = fillMap(data=singleRegion, template=dummyTemplate,
                title="un títol", subtitle="un subtítol", locations=['01','09'], geolevel='ccaa', maxVal=143)
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#3f4c15"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">100,0%</text>
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


    def test_renderMap_dummyAllLocations(self):
        self.maxDiff = None
        source = self.createSource(
            ns(members=[
                headers,
                data_Girona,
                data_Adra,
                ])
            )

        result = renderMap(source, 'members', ['2018-01-01'], geolevel='dummy')

        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: </text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#c4db7e"/>
  <text y="180" x="100" style="text-anchor:middle">2</text>
  <text y="200" x="100" style="text-anchor:middle">9,1%</text>
  <circle cy="180" cx="240" r="60" fill="#384413"/>
  <text y="180" x="240" style="text-anchor:middle">20</text>
  <text y="200" x="240" style="text-anchor:middle">90,9%</text>
</svg>
""")

    def test_renderMap_dummyMissingLocation(self):
        self.maxDiff = None
        source = self.createSource(
            ns(members=[
                headers,
                data_Adra,
                ])
            )

        result = renderMap(source, 'members', ['2018-01-01'], geolevel='dummy')

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
        result = renderMap(source, 'members', ['2019-01-01'], geolevel='ccaa')
        self.assertB2BEqual(result)

    def test_renderMap_contracts(self):
        source = loadCsvSource()
        result = renderMap(source, 'contracts', ['2019-01-01'], geolevel='ccaa')
        self.assertB2BEqual(result)

    def test_dataToTemplateDict_singleState(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=singleState, colors=color, geolevel='state', maxVal=1969)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 1969
            legendNumber_25: 6
            legendNumber_50: 44
            legendNumber_75: 295
        """)

    def test_dataToTemplateDict_noState(self):
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=noState, colors=color, geolevel='state',maxVal=1969)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 1969
            legendNumber_25: 6
            legendNumber_50: 44
            legendNumber_75: 295
        """)

    def test_dataToTemplateDict_manyStates(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyStates, colors=color, geolevel='state',maxVal=750)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 750
            legendNumber_25: 5
            legendNumber_50: 27
            legendNumber_75: 143
        """)

    def test_dataToTemplateDict_twoStatesDifCCAA(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyStatesDifferentCCAA, colors=color, geolevel='state', maxVal=750)

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
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 750
            legendNumber_25: 5
            legendNumber_50: 27
            legendNumber_75: 143
        """)

    def test_renderMap_members_byState(self):
        source = loadCsvSource()
        result = renderMap(source, 'members', ['2019-11-01'], geolevel='state')
        self.assertB2BEqual(result)

    def test_dataToTemplateDict_manyRegionsGivenWithoutMaxValue(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colors=color)

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
            color_01: '#384413'
            number_09: 20
            percent_09: 14,0%
            color_09: '#8aa72f'
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 123
            legendNumber_25: 3
            legendNumber_50: 11
            legendNumber_75: 36
        """)

    def test_maxValue_oneCCAA(self):

        self.assertEqual(maxValue(singleRegion, 'ccaa', frame=0), 123)

    def test_maxValue_manyCCAA(self):

        self.assertEqual(maxValue(manyRegions, 'ccaa', frame=0), 123)

    def test_maxValue_noCCAA(self):

        self.assertEqual(maxValue(noRegion, 'ccaa', frame=0), 0)

    def test_maxValue_singleState(self):

        self.assertEqual(maxValue(singleState, 'state', frame=0), 1969)

    def test_maxValue_manyStates(self):

        self.assertEqual(maxValue(manyStates, 'state', frame=0), 500)

    def test_maxValue_manyStatesDifferentCCAA(self):

        self.assertEqual(maxValue(manyStatesDifferentCCAA, 'state', frame=0), 500)

    def test__dataToTemplateDict_frameSet(self):
        data = ns.loads("""\
            dates: [2019-01-01, 2018-01-01]
            values: [143, 500]
            countries:
              ES:
                name: España
                values: [143, 500]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123, 500]
                  '09':
                    name: Catalunya
                    values: [20, 0]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, frame=1)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2018
            month: Enero
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_01: 500
            percent_01: 100,0%
            color_01: '#384413'
            number_09: 0
            percent_09: 0,0%
            color_09: '#e0ecbb'
            legendColor_0: '#e0ecbb'
            legendColor_100: '#384413'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendNumber_0: 1
            legendNumber_100: 500
            legendNumber_25: 4
            legendNumber_50: 22
            legendNumber_75: 105
        """)


    def test__toPopulationRelative_singleRegion(self):

        data = ns.loads(singleRegion.dump())

        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
            dates: [2019-01-01]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [0.14662275930920415]
        """))


    def test__toPopulationRelative_manyRegions(self):

        data = ns.loads(manyRegions.dump())

        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [143]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [0.14662275930920415]
                  '09':
                    name: Catalunya
                    values: [0.02696785445233209]
        """))

    def test__toPopulationRelative_noRegion(self):

        data = ns.loads(noRegion.dump())

        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
            dates: [2019-01-01]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas: {}
        """))

    def test__toPopulationRelative_singleState(self):

        data = ns.loads(singleState.dump())

        populationContent = Path('maps/population_state.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='state', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
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
                          - 15.769346280909
        """))

    def test__toPopulationRelative_manyStatesDifferentCCAA(self):

        data = ns.loads(manyStatesDifferentCCAA.dump())

        populationContent = Path('maps/population_state.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='state', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
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
                          - 4.004404845329863
                    '09':
                      name: Catalunya
                      values: [250]
                      states:
                        '43':
                          name: Tarragona
                          values:
                            - 3.1541005199219296
        """))

    def test__toPopulationRelative_singleRegionManyFrames(self):

        data = ns.loads("""\
            dates: [2019-01-01, 2018-01-01]
            values: [143, 500]
            countries:
              ES:
                name: España
                values: [143, 500]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123, 500]
                  '09':
                    name: Catalunya
                    values: [20, 0]
            """)

        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        self.assertNsEqual(data, ns.loads("""\
            dates: [2019-01-01, 2018-01-01]
            values: [143, 500]
            countries:
              ES:
                name: España
                values: [143, 500]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [0.14662275930920415, 0.5960274768666836]
                  '09':
                    name: Catalunya
                    values: [0.02696785445233209, 0.0]
        """))

    def test_dataToTemplateDict_relativeData(self):
        data = ns.loads(singleRegion.dump())
        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        result = dataToTemplateDict(data=data, colors=Gradient('#e0ecbb', '#384413'),
            title="relative", subtitle='subtitle', colorScale='Linear', isRelative=True)
        self.assertNsEqual(result, """\
                    title: relative
                    subtitle: subtitle
                    year: 2019
                    month: Enero
                    number_00: 0,0
                    percent_00: ''
                    color_00: '#e0ecbb'
                    number_01: 0,1
                    percent_01: ''
                    color_01: '#384413'
                    legendColor_0: '#e0ecbb'
                    legendColor_100: '#384413'
                    legendColor_25: '#c2da79'
                    legendColor_50: '#a4c738'
                    legendColor_75: '#6e8625'
                    legendNumber_0: 0
                    legendNumber_100: 0
                    legendNumber_25: 0
                    legendNumber_50: 0
                    legendNumber_75: 0
                """)


    def test_fillMap_relativeDataLinearColors(self):

        self.maxDiff = None
        data = ns.loads(manyRegions.dump())
        populationContent = Path('maps/population_ccaa.tsv').read_text(encoding='utf8')
        populationData = tuples2objects(parse_tsv(populationContent))
        toPopulationRelative(data=data, geolevel='ccaa', population=populationData)

        result = fillMap(data=data, template=dummyTemplate,
                title="un títol", subtitle="un subtítol", geolevel='ccaa', scale='Linear', isRelative=True)
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#384413"/>
  <text y="180" x="100" style="text-anchor:middle">0,1</text>
  <text y="200" x="100" style="text-anchor:middle"></text>
  <circle cy="180" cx="240" r="60" fill="#cadf8b"/>
  <text y="180" x="240" style="text-anchor:middle">0,0</text>
  <text y="200" x="240" style="text-anchor:middle"></text>
</svg>
""")


    def test_renderMap_dummyAllLocationsRelativePopulation(self):
        self.maxDiff = None
        source = self.createSource(
            ns(members=[
                headers,
                data_Girona,
                data_Adra,
                ])
            )

        result = renderMap(source, 'members', ['2018-01-01'], geolevel='dummy', isRelative=True)

        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: /10.000 hab</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: Enero</text>
  <circle cy="180" cx="100" r="60" fill="#bcd66c"/>
  <text y="180" x="100" style="text-anchor:middle">2,0</text>
  <text y="200" x="100" style="text-anchor:middle"></text>
  <circle cy="180" cx="240" r="60" fill="#384413"/>
  <text y="180" x="240" style="text-anchor:middle">10,0</text>
  <text y="200" x="240" style="text-anchor:middle"></text>
</svg>
""")

    def test_fillLegend_(self):
        scale = LogScale(higher=1000)
        gradient = Gradient('#e0ecbb', '#384413')
        result = dict()
        fillLegend(result=result, scale=scale, colors=gradient)
        self.assertNsEqual(result, """\
            legendNumber_0: 1
            legendNumber_25: 5
            legendNumber_50: 31
            legendNumber_75: 177
            legendNumber_100: 1000
            legendColor_0: '#e0ecbb'
            legendColor_25: '#c2da79'
            legendColor_50: '#a4c738'
            legendColor_75: '#6e8625'
            legendColor_100: '#384413'
        """)