import unittest
from yamlns.dateutils import Date
from yamlns import namespace as ns
from .map import dataToTemplateDict

class Map_Test(unittest.TestCase):

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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
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
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
            number_01: 123
            percent_01: 100,0%
            color_01: '#fff'
        """)

    def test_dataToTemplateDict_manyRegions(self):
        data = ns.loads("""\
            dates: [2019-01-01]
            values: [143]
            countries:
              ES:
                name: España
                values: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
                  '09':
                    name: Catalunya
                    values: [20]
            """)
        result = dataToTemplateDict(titol="un títol", subtitol="un subtítol", data=data)

        self.assertNsEqual(result, """\
            titol: un títol
            subtitol: un subtítol
            year: 2019
            month: 1
            number_01: 123
            percent_01: 86,0%
            color_01: '#fff'
            number_09: 20
            percent_09: 14,0%
            color_09: '#fff'
        """)
