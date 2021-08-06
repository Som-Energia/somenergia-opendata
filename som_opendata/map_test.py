# -*- coding: utf8 -*-
from __future__ import unicode_literals

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
    getNiceDivisor,
    toPopulationRelative,
    fillLegend,
    frameCssAnimation,
    createAnimatedSvg,
    )
from .colorscale import Gradient
from .scale import LogScale, LinearScale
from .csvSource import loadCsvSource, CsvSource
from future.utils import iteritems
from pathlib2 import Path
from .distribution import parse_tsv, tuples2objects
from .templateSource import loadMapData
from .timeaggregator import TimeAggregator
from .tsvRelativeMetricSource import loadTsvRelativeMetric


source = loadCsvSource(relativePath='../testData/metrics')
mapTemplateSource = loadMapData()
relativeData = loadTsvRelativeMetric()

dummyTemplate="""\
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

dummyTemplateNamesLegend="""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: {title}</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: {subtitle}</text>
  <text y="80" x="170" style="text-anchor:middle">Year: {year}</text>
  <text y="100" x="170" style="text-anchor:middle">Month: {month}</text>
  <text y="110" x="50" style="text-anchor:middle">{Andalusia}</text>
  <text y="110" x="320" style="text-anchor:middle">{Catalonia}</text>
  <circle cy="180" cx="100" r="60" fill="{color_01}"/>
  <text y="180" x="100" style="text-anchor:middle">{number_01}</text>
  <text y="200" x="100" style="text-anchor:middle">{percent_01}</text>
  <circle cy="180" cx="240" r="60" fill="{color_09}"/>
  <text y="180" x="240" style="text-anchor:middle">{number_09}</text>
  <text y="200" x="240" style="text-anchor:middle">{percent_09}</text>
  <text y="280" x="260" style="text-anchor:middle">{legend}</text>
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
headers = "codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = "ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = "FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = "ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = "ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = "ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"

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

legendTemplate = Path('data/maps/legend.svg').read_text(encoding='utf8')

class Map_Test(unittest.TestCase):

    def setUp(self):
        self.b2bdatapath = 'b2bdata'
        Path('data/maps/mapTemplates/mapTemplate_dummy.svg').write_text(dummyTemplate, encoding='utf8')

        self.maxDiff = None

    def tearDown(self):
        Path('data/maps/mapTemplates/mapTemplate_dummy.svg').unlink()

    from somutils.testutils import assertNsEqual

    def test_dataToTemplateDict_noRegion(self):
        scale = LogScale(higher=123)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=noRegion, colors=color,scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
        """)

    def test_dataToTemplateDict_singleRegion(self):

        color = Gradient('#e0ecbb','#384413')
        scale = LogScale(higher=123)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=singleRegion, colors=color,scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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
        scale = LogScale(higher=143)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colors=color, scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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

    def test_dataToTemplateDict_manyRegionsGivenScale(self):

        color = Gradient('#e0ecbb','#384413')
        scale = LogScale(higher=143)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colors=color, scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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
        scale = LogScale(higher=126)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
            number_00: 3
            percent_00: 2,4%
            color_00: '#c5db7f'
            number_01: 123
            percent_01: 97,6%
            color_01: '#394513'
        """)

    def test_dataToTemplateDict_LinearColorScale(self):

        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyRegions, colors=color, scale= LinearScale(higher=143))

        self.assertNsEqual(result, u"""\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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

    def test_fillMap_manyRegions(self):

        self.maxDiff = None
        result = fillMap(data=manyRegions, template=dummyTemplate, legendTemplate="",
                title=u"un títol", subtitle=u"un subtítol", geolevel='ccaa', maxVal=143)
        self.assertMultiLineEqual(result, u"""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#4c5c1a"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">86,0%</text>
  <circle cy="180" cx="240" r="60" fill="#96b633"/>
  <text y="180" x="240" style="text-anchor:middle">20</text>
  <text y="200" x="240" style="text-anchor:middle">14,0%</text>
</svg>
""")


    def test_fillMap_manyRegionsWithoutMaxVal(self):

        self.maxDiff = None
        result = fillMap(data=manyRegions, template=dummyTemplate , legendTemplate="",
                title=u"un títol", subtitle=u"un subtítol", geolevel='ccaa')
        self.assertMultiLineEqual(result, u"""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#4c5c1a"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">86,0%</text>
  <circle cy="180" cx="240" r="60" fill="#96b633"/>
  <text y="180" x="240" style="text-anchor:middle">20</text>
  <text y="200" x="240" style="text-anchor:middle">14,0%</text>
</svg>
""")

    def test_fillMap_withLocationList(self):

        self.maxDiff = None
        result = fillMap(data=singleRegion, template=dummyTemplate, legendTemplate="",
                title=u"un títol", subtitle=u"un subtítol", locations=['01','09'], geolevel='ccaa', maxVal=143)
        self.assertMultiLineEqual(result, u"""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#4c5c1a"/>
  <text y="180" x="100" style="text-anchor:middle">123</text>
  <text y="200" x="100" style="text-anchor:middle">100,0%</text>
  <circle cy="180" cx="240" r="60" fill="#e0ecbb"/>
  <text y="180" x="240" style="text-anchor:middle">0</text>
  <text y="200" x="240" style="text-anchor:middle">0,0%</text>
</svg>
""")


    def createSource(self, metrics):

        content = ns()
        for metric, lines in iteritems(metrics):
            content[metric] = '\n'.join(lines)

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
        result = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2018-01-01'),
            template=dummyTemplate,
            geolevel='dummy',
            locationsCodes=['01','09']
        )

        # TODO: Review why at some point changed from calculated #c4db7e to #cee193
        # TODO: Review why at some point changed from calculated #384413 to #84a02d
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: </text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#cee193"/>
  <text y="180" x="100" style="text-anchor:middle">2</text>
  <text y="200" x="100" style="text-anchor:middle">9,1%</text>
  <circle cy="180" cx="240" r="60" fill="#84a02d"/>
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
        result = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2018-01-01'),
            template=dummyTemplate,
            geolevel='dummy',
            locationsCodes=['01','09']
        )

        # TODO: Review why at some point changed from calculated #384413 to #cee193
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: </text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#cee193"/>
  <text y="180" x="100" style="text-anchor:middle">2</text>
  <text y="200" x="100" style="text-anchor:middle">100,0%</text>
  <circle cy="180" cx="240" r="60" fill="#e0ecbb"/>
  <text y="180" x="240" style="text-anchor:middle">0</text>
  <text y="200" x="240" style="text-anchor:middle">0,0%</text>
</svg>
""")

    def test_renderMap_members(self):
        locations = relativeData.getCodesByGeolevel('ccaa')
        template = mapTemplateSource.getTemplate(geolevel='ccaa', lang='en')
        result = renderMap(
            source,
            'members', 
            timeDomain=TimeAggregator(on='2019-01-01'),
            template=template,
            geolevel='ccaa',
            locationsCodes=locations,
            legendTemplate=legendTemplate,
        )
        self.assertB2BEqual(result)

    def test_renderMap_contracts(self):
        locations = relativeData.getCodesByGeolevel('ccaa')
        template = mapTemplateSource.getTemplate(geolevel='ccaa', lang='en')
        result = renderMap(
            source,
            'contracts',
            timeDomain=TimeAggregator(on='2019-01-01'),
            geolevel='ccaa',
            template=template,
            locationsCodes=locations,
            legendTemplate=legendTemplate,
        )
        self.assertB2BEqual(result)

    def test_dataToTemplateDict_singleState(self):

        color = Gradient('#e0ecbb','#384413')
        scale = LogScale(higher=1969)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=singleState, colors=color, geolevel='state', scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_11: 1969
            percent_11: 100,0%
            color_11: '#384413'
        """)

    def test_dataToTemplateDict_noState(self):
        color = Gradient('#e0ecbb','#384413')
        scale = LogScale(higher=1969)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=noState, colors=color, geolevel='state', scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
        """)

    def test_dataToTemplateDict_manyStates(self):

        color = Gradient('#e0ecbb','#384413')
        scale = LogScale(higher=750)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyStates, colors=color, geolevel='state', scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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

    def test_dataToTemplateDict_twoStatesDifCCAA(self):

        scale = LogScale(higher=750)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=manyStatesDifferentCCAA, colors=color, geolevel='state', scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2019
            month: January
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
        locations = relativeData.getCodesByGeolevel('state')
        template = mapTemplateSource.getTemplate(geolevel='state', lang='en')
        result = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2019-11-01'),
            geolevel='state',
            template=template,
            locationsCodes=locations,
            legendTemplate=legendTemplate,
        )
        self.assertB2BEqual(result)

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
        color = Gradient('#e0ecbb', '#384413')
        scale = LogScale(higher=500)
        result = dataToTemplateDict(title="un títol", subtitle="un subtítol", data=data, colors=color, frame=1, scale=scale)

        self.assertNsEqual(result, """\
            title: un títol
            subtitle: un subtítol
            year: 2018
            month: January
            number_00: 0
            percent_00: 0,0%
            color_00: '#e0ecbb'
            number_01: 500
            percent_01: 100,0%
            color_01: '#384413'
            number_09: 0
            percent_09: 0,0%
            color_09: '#e0ecbb'
        """)


    def test__toPopulationRelative_singleRegion(self):

        data = ns.loads(singleRegion.dump())

        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)

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

    def test__toPopulationRelative_givenPerValue(self):

        data = ns.loads(singleRegion.dump())
        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues, perValue=100000)

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
                    values: [1.4662275930920416]
        """))

    def test__toPopulationRelative_manyRegions(self):

        data = ns.loads(manyRegions.dump())
        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)

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

        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)

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

        populationValues = relativeData.getValuesByCode(metric='population', geolevel='state')
        toPopulationRelative(data=data, geolevel='state', values=populationValues)


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

        populationValues = relativeData.getValuesByCode(metric='population', geolevel='state')
        toPopulationRelative(data=data, geolevel='state', values=populationValues)


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

        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)

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
        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)
        scale = LinearScale(higher=1)

        result = dataToTemplateDict(data=data, colors=Gradient('#e0ecbb', '#384413'),
            title="relative", subtitle='subtitle', isRelative=True, scale=scale)
        self.assertNsEqual(result, """\
                    title: relative
                    subtitle: subtitle
                    year: 2019
                    month: January
                    number_00: 0,0
                    percent_00: ''
                    color_00: '#e0ecbb'
                    number_01: 0,1
                    percent_01: ''
                    color_01: '#cee194'
                """)


    def test_fillMap_relativeDataLinearColors(self):

        self.maxDiff = None
        data = ns.loads(manyRegions.dump())
        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        toPopulationRelative(data=data, geolevel='ccaa', values=populationValues)

        result = fillMap(data=data, template=dummyTemplate, legendTemplate="",
                title=u"un títol", subtitle=u"un subtítol", geolevel='ccaa', scale='Linear', isRelative=True)


        # TODO: Review why it changed from #384413 to #e0ecbb
        self.assertMultiLineEqual(result, u"""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: un títol</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: un subtítol</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2019</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#e0ecbb"/>
  <text y="180" x="100" style="text-anchor:middle">0,1</text>
  <text y="200" x="100" style="text-anchor:middle"></text>
  <circle cy="180" cx="240" r="60" fill="#e0ecbb"/>
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
        populationValues = {'01': 8388875, '09': 7416237}
        result = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2018-01-01'),
            template=dummyTemplate,
            geolevel='dummy',
            locationsCodes=['01','09'],
            relativeMetricValues=populationValues,
        )

        # TODO: Review why it changed from #d9e8ac to #dbe9b1
        # TODO: Review why it changed from #54671d to #96b633
        self.assertMultiLineEqual(result, """\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: Members</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: per 5.000.000 population</text>
  <text y="80" x="170" style="text-anchor:middle">Year: 2018</text>
  <text y="100" x="170" style="text-anchor:middle">Month: January</text>
  <circle cy="180" cx="100" r="60" fill="#dbe9b1"/>
  <text y="180" x="100" style="text-anchor:middle">1,2</text>
  <text y="200" x="100" style="text-anchor:middle"></text>
  <circle cy="180" cx="240" r="60" fill="#96b633"/>
  <text y="180" x="240" style="text-anchor:middle">13,5</text>
  <text y="200" x="240" style="text-anchor:middle"></text>
</svg>
""")

    def test_fillLegend_default(self):
        scale = LogScale(higher=1000)
        gradient = Gradient('#e0ecbb', '#384413')
        result = dict()
        result = fillLegend(legendTemplate=legendTemplate,scale=scale, colors=gradient, isRelative=None)
        self.assertEqual(result, legendTemplate.format(
            legendNumber_0= 0,
            legendNumber_25= 0,
            legendNumber_50= 30,
            legendNumber_75= 180,
            legendNumber_100= 1000,
            legendColor_0= '#e0ecbb',
            legendColor_25= '#c2da79',
            legendColor_50='#a4c738',
            legendColor_75= '#6e8625',
            legendColor_100= '#384413'
        ))

    def test_fillLegend_relativeData(self):
        scale = LogScale(higher=1000)
        gradient = Gradient('#e0ecbb', '#384413')
        result = fillLegend(legendTemplate=legendTemplate,scale=scale, colors=gradient, isRelative='population')
        self.assertEqual(result, legendTemplate.format(
            legendNumber_0=1,
            legendNumber_25='',
            legendNumber_50=31,
            legendNumber_75='',
            legendNumber_100=1000,
            legendColor_0='#e0ecbb',
            legendColor_25='#c2da79',
            legendColor_50='#a4c738',
            legendColor_75='#6e8625',
            legendColor_100='#384413',
        ))

    def test_renderMap_members_givenTemplate(self):
        template = Path('data/maps/mapTemplates/mapTemplate_dummy.svg').read_text(encoding='utf8')
        result = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2019-11-01'),
            geolevel='state',
            template=template,
            locationsCodes=['01','09']
        )
        self.assertB2BEqual(result)

    def test_renderMap_membersRangeDates(self):
        template = mapTemplateSource.getTemplate(geolevel='ccaa', lang='en')
        locations = relativeData.getCodesByGeolevel('ccaa')
        svg = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(periodicity='monthly', since='2019-01-01', to='2019-02-01'),
            geolevel='ccaa',
            template=template,
            locationsCodes=locations
        )
        self.assertB2BEqual(svg)

    def test_getNiceDivisor_(self):
        relativeValues = relativeData.getValuesByCode(geolevel='ccaa')
        result = getNiceDivisor(relativeValues)

        self.assertEqual(result, 50000)

    def test_renderMap_members_cachedAfterChangedValues(self):
        locations = relativeData.getCodesByGeolevel('ccaa')
        template = mapTemplateSource.getTemplate(geolevel='ccaa', lang='en')
        resultBefore = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2019-01-01'),
            template=template,
            geolevel='ccaa',
            locationsCodes=locations,
            legendTemplate=""
          )
        populationValues = relativeData.getValuesByCode(metric='population', geolevel='ccaa')
        renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2019-01-01'),
            template=template,
            geolevel='ccaa',
            relativeMetricValues=populationValues,
            locationsCodes=locations,
            legendTemplate="",
        )
        resultAfter = renderMap(
            source,
            'members',
            timeDomain=TimeAggregator(on='2019-01-01'),
            template=template,
            geolevel='ccaa',
            locationsCodes=locations,
            legendTemplate=""
          )
        self.assertEqual(resultBefore, resultAfter)

    def test_frameCssAnimation(self):
        result = frameCssAnimation(
            frames=2,
            seconds=10,
            classtemplate='frame{:03d}',
        )
        self.assertEqual(result,
            """@keyframes frame000 { 0% { visibility: hidden; } 0.00% { visibility: visible; } 50.00% { visibility: hidden; } } .frame000 { animation: frame000 10s step-end infinite; }\n"""
            """@keyframes frame001 { 0% { visibility: hidden; } 50.00% { visibility: visible; } 100.00% { visibility: hidden; } } .frame001 { animation: frame001 10s step-end infinite; }\n"""
        )

    def test_createAnimatedSvg_manyFrames(self):
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
        template = Path('data/maps/mapTemplates/mapTemplate_dummy.svg').read_text(encoding='utf8')
        gradient = Gradient('#e0ecbb', '#384413')
        scale = LogScale(higher=500).nice()
        img = createAnimatedSvg(
            frameQuantity=2,
            data=data,
            template=template,
            legend='',
            colors=gradient,
            scale=scale,
            geolevel='ccaa',
            title='One',
        )
        self.assertB2BEqual(img)


# vim: et sw=4 ts=4
