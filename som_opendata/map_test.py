# -*- encoding: utf8 -*-

import b2btest
import unittest
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .map import dataToTemplateDict, fillMap, renderMap
from .colorscale import Gradient
from .csvSource import loadCsvSource


dummyTemplate="""\
<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: {titol}</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: {subtitol}</text>
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


class Map_Test(unittest.TestCase):

    def setUp(self):
        self.b2bdatapath = 'b2bdataMap'

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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            number_01: 123
            percent_01: 100,0%
            color_01: '#384413'
        """)

    def test_percentRegion_totalZero(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [0]
            countries:
              ES:
                name: España
                values: [0]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [0]
            """)
        color = Gradient('#e0ecbb','#384413')
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            number_01: 0
            percent_01: 0,0%
            color_01: '#e0ecbb'
        """)

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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 3
            percent_00: 2,4%
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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data, colorScale='Linear', colors=color)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: Enero
            number_00: 0
            percent_00: 0,0%
            number_01: 123
            percent_01: 86,0%
            color_01: '#56691d'
            number_09: 20
            percent_09: 14,0%
            color_09: '#cfe296'
        """)

    def test_fillMap_(self):
        color = Gradient('#e0ecbb','#384413')
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
                gradient=color, title="un títol", subtitle="un subtítol")
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
        color = Gradient('#e0ecbb','#384413')
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
                gradient=color, title="un títol", subtitle="un subtítol", locations=['01','09'])
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

    @unittest.skip("Not yet")
    def test_renderMap_byDefault(self):
        source = loadCsvSource()
        result = renderMap(source, 'members', '2019-01-01')
        self.assertB2BEqual(result)

    @unittest.skip("Rewrite")
    def test_fillMap_singleRegion(self):
        color = Gradient('#e0ecbb','#384413')

        self.assertB2BEqual(
            fillMap(data=fullData, template='MapaSocios-template.svg',
                colors=color, title="un títol", subtitle="un subtítol")
        )


    @unittest.skip("Rewrite")
    def test_fillMap_missingCCAA(self):
        data = ns.loads("""\
    dates: [2019-01-01]
    values: [3208]
    countries:
      ES:
        name: España
        values: [3208]
        ccaas:
          '01':
            name: Andalucia
            values:
            - 48
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
        color = Gradient('#e0ecbb','#384413')

        self.assertB2BEqual(
            fillMap(data=data, template='MapaSocios-template.svg',
                colors=color, title="un títol", subtitle="un subtítol")
        )


    @unittest.skip("Rewrite")
    def test_fillMap_missingCCAAs(self):
        data = ns.loads("""\
        dates: [2019-01-01]
        values: [3208]
        countries:
          ES:
            name: España
            values: [3208]
            ccaas:
              '01':
                name: Andalucia
                values:
                - 48
        """)
        color = Gradient('#e0ecbb','#384413')
        self.assertB2BEqual(
            fillMap(data=data, template='MapaSocios-template.svg',
                colors=color, title="un títol", subtitle="un subtítol")
        )

