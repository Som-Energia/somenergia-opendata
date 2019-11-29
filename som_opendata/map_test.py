import b2btest
import unittest
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .map import dataToTemplateDict, renderMap
from .colorscale import Gradient

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

    def test_dataToTemplateDict_restWorld(self):
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

    unittest.skip("Not implemented yet")
    def test_renderMap_singleRegion(self):
        color = Gradient('#e0ecbb','#384413')

        self.assertB2BEqual(
            renderMap(data=fullData, template='MapaSocios-template.svg',
                colors=color, title="un títol", subtitle="un subtítol")
        )
