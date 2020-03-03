import b2btest
import unittest
from yamlns import namespace as ns
from .templateSource import TemplateSource, loadMapData

class TemplateSource_Test(unittest.TestCase):

    def test_getTemplate_geolevel(self):
        result = loadMapData()
        self.assertNotEqual(len(result.getTemplate('ccaa')),0)
        self.assertNotEqual(len(result.getTemplate('state')),0)

    def test_getStyle_geolevel(self):
        result = loadMapData()
        self.assertNotEqual(len(result.getStyle('state')),0)
        self.assertEqual(len(result.getStyle('ccaa')),0)
