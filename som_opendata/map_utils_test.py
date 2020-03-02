import unittest
from .map_utils import (
    validateImplementation,
    ValidateImplementationMap,
    loadMapData,
)
from yamlns import namespace as ns

class MapUtils_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test__validateImplementation__notImplementedValue(self):
        params = [['geolevel','bad']]
        with self.assertRaises(ValidateImplementationMap) as ctx:
            validateImplementation(params)
        self.assertEqual(ctx.exception.parameter, 'geolevel')
        self.assertEqual(ctx.exception.value, 'bad')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description,
            'Not implemented geolevel \'bad\' try with [\'ccaa\', \'state\']')

    def test__validateImplementation__valid(self):
        params = [['metric','members'],['geolevel','ccaa'], ['relativemetric','population']]
        self.assertEqual(validateImplementation(params), None)

    def test__validateImplementation__notImplementedIndicator(self):
        params = [['relativemetric', 'dogs']]
        with self.assertRaises(ValidateImplementationMap) as ctx:
            validateImplementation(params)
        self.assertEqual(ctx.exception.parameter, 'relativemetric')
        self.assertEqual(ctx.exception.value, 'dogs')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description,
            'Not implemented relativemetric \'dogs\' try with [\'population\', None]')


    def test_loadMapData(self):
        result = loadMapData()
        self.assertTrue(result.ccaa.template)
        self.assertTrue(result.state.template)
        self.assertTrue(result.legend)
        self.assertTrue(result.state.style)
        self.assertFalse(result.ccaa.style)
        self.assertEqual(len(result.translations), 5)
        self.assertTrue(result.translations.ca)
