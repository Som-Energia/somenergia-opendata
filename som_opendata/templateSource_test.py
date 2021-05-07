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
  {style}
</svg>"""

data = loadMapData()

class TemplateSource_Test(unittest.TestCase):
    maxDiff = None

    def test_getLegend(self):
        self.assertNotEqual(len(data.getLegend()), '')

    def test_getTemplate_dummyEn(self):
        self.maxDiff = None
        result = data.getTemplate('dummy', lang='en')
        self.assertMultiLineEqual(result,
u"""<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: {title}</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: {subtitle}</text>
  <text y="80" x="170" style="text-anchor:middle">Year: {year}</text>
  <text y="100" x="170" style="text-anchor:middle">Month: {month}</text>
  <text y="110" x="50" style="text-anchor:middle">Andalusia</text>
  <text y="110" x="320" style="text-anchor:middle">Catalonia</text>
  <circle cy="180" cx="100" r="60" fill="{color_01}"/>
  <text y="180" x="100" style="text-anchor:middle">{number_01}</text>
  <text y="200" x="100" style="text-anchor:middle">{percent_01}</text>
  <circle cy="180" cx="240" r="60" fill="{color_09}"/>
  <text y="180" x="240" style="text-anchor:middle">{number_09}</text>
  <text y="200" x="240" style="text-anchor:middle">{percent_09}</text>
  <text y="280" x="260" style="text-anchor:middle">{legend}</text>
</svg>""")

    def test_getTemplate_fake(self):
        self.maxDiff = None
        result = data.getTemplate('', fake=True)
        self.assertMultiLineEqual(result,
u"""<svg xmlns="http://www.w3.org/2000/svg" width="480" version="1.1" height="300">
  <text y="40" x="170" style="text-anchor:middle">Title: {title}</text>
  <text y="60" x="170" style="text-anchor:middle">Subtitle: {subtitle}</text>
  <text y="80" x="170" style="text-anchor:middle">Year: {year}</text>
  <text y="100" x="170" style="text-anchor:middle">Month: {month}</text>
  <text y="110" x="50" style="text-anchor:middle">Andalusia</text>
  <text y="110" x="320" style="text-anchor:middle">Catalonia</text>
  <circle cy="180" cx="100" r="60" fill="{color_01}"/>
  <text y="180" x="100" style="text-anchor:middle">{number_01}</text>
  <text y="200" x="100" style="text-anchor:middle">{percent_01}</text>
  <circle cy="180" cx="240" r="60" fill="{color_09}"/>
  <text y="180" x="240" style="text-anchor:middle">{number_09}</text>
  <text y="200" x="240" style="text-anchor:middle">{percent_09}</text>
  <text y="280" x="260" style="text-anchor:middle">{legend}</text>
</svg>""")

    def test_getTemplate_ccaa_compareDifferentLang(self):
        self.maxDiff = None
        en = data.getTemplate('ccaa', lang='en')
        ca = data.getTemplate('ccaa', lang='ca')
        self.assertTrue(en)
        self.assertTrue(ca)
        self.assertNotEqual(en, ca)

    def test_getTemplate_missingGeolevel(self):
        with self.assertRaises(ValueError) as context:
            data.getTemplate('satrapy')
        self.assertEqual("No map template found for country=es detailed by satrapy in language 'en'",
            str(context.exception)
        )

    def test_getTemplate_missingLanguage(self):
        with self.assertRaises(ValueError) as context:
            data.getTemplate('ccaa', 'fr')
        self.assertEqual("No map template found for country=es detailed by ccaa in language 'fr'",
            str(context.exception)
        )
