import b2btest
import unittest
from yamlns import namespace as ns
from .templateSource import TemplateSource, loadMapData

class TemplateSource_Test(unittest.TestCase):

    def test_getTemplate_geolevel(self):
        result = loadMapData()
        self.assertNotEqual(len(result.getTemplate('ccaa')),0)
