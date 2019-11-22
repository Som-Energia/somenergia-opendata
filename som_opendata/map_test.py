import unittest
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .map import dataToSvgDict


"""\
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
        states:
          '04':
            name: Almería
            values: [123]
            cities:
              '04003':
                name: Adra
                values: [123]
"""


class Map_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test_dataToSvgDict_withNoRegion(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas: {}
            """)
        result = dataToSvgDict(titol="un títol", subtitol="un subtítol", data=data)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
        """)

    def test_dataToSvgDict_withOneRegion(self):
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
        result = dataToSvgDict(titol="un títol", subtitol="un subtítol", data=data)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
            number_01: 123
            percent_01: 100
            color_01: '#fff'
        """)
