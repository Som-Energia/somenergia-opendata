import b2btest
import unittest
from yamlns import namespace as ns
from .templateSource import TemplateSource, loadMapData

dummyTemplate = u"""\
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
</svg>"""

data = loadMapData()

class TemplateSource_Test(unittest.TestCase):
    maxDiff = None

    def test_getRawTemplate_geolevel(self):
        self.maxDiff = None
        self.assertNotEqual(len(data.getRawTemplate('ccaa')),0)
        self.assertNotEqual(len(data.getRawTemplate('state')),0)
        self.assertMultiLineEqual(data.getRawTemplate('dummy'), dummyTemplate)

    def test_getStyle_geolevel(self):
        self.assertNotEqual(len(data.getStyle('state')),0)
        self.assertEqual(len(data.getStyle('ccaa')),0)

    def test_loadMapData_translations(self):
        translations = data.translations['ca']
        self.assertEqual(len(translations),68)
        self.assertEqual(translations['Catalonia'], 'Catalunya')

    def test_getLegend(self):
        self.assertNotEqual(len(data.getLegend()), '')

    def test_getTemplate_dummyCa(self):
        result = loadMapData()
        self.assertNotEqual(len(result.getTemplate('ccaa')),0)
        self.assertNotEqual(len(result.getTemplate('state')),0)