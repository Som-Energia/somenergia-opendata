import b2btest
import unittest
from yamlns import namespace as ns
from .distribution import parse_tsv, tuples2objects
from .tsvRelativeMetricSource import (
    TsvRelativeMetricSource,
    loadTsvRelativeMetric,
    getFieldBy,
)

headers = u"code\tname\tpopulation"
catalunya = u"09\tCatalunya\t7416237"
andalusia = u"01\tAndalucia\t8388875"

ccaaData = '\n'.join([headers, catalunya, andalusia])


class TsvRelativeMetricSource_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test_getFieldBy_nameByCode(self):
        data = tuples2objects(parse_tsv(ccaaData))
        result = getFieldBy(data=data, field='name', by='code')
        self.assertEqual(result, {'01': 'Andalucia', '09': 'Catalunya'})

    def test_getFieldBy_valueByCode(self):
        data = tuples2objects(parse_tsv(ccaaData))
        result = getFieldBy(data=data, field='population', by='code')
        self.assertEqual(result, {'01': '8388875', '09': '7416237'})

    def test_TsvRelativeMetric_metrics(self):
        data = ns(population=ns(ccaa=ccaaData))
        result = TsvRelativeMetricSource(data)
        self.assertEqual(result.metrics, ['population'])

    def test_getValuesByCode(self):
        data = ns(population=ns(ccaa=ccaaData))
        result = TsvRelativeMetricSource(data).getValuesByCode('population', 'ccaa')
        self.assertNsEqual(result, ns({'01': '8388875', '09': '7416237'}))

    def test_getDataObjects(self):
        data = ns(population=ns(ccaa='\n'.join([headers, catalunya])))
        result = TsvRelativeMetricSource(data).getDataObjects('population', 'ccaa')
        self.assertEqual(
            result,
            [ns(code='09', name='Catalunya', population='7416237')]
        )

    def test_validateMetricGeolevel_missingMetric(self):
        src = ns(population=ns(ccaa='\n'.join([headers, catalunya])))
        data = TsvRelativeMetricSource(src)
        with self.assertRaises(ValueError) as context:
            data.validateMetricGeolevel('cows', 'ccaa')
        self.assertEqual("Relative metric cows not found",
            str(context.exception)
        )

    def test_validateMetricGeolevel_missingGeolevel(self):
        src = ns(population=ns(ccaa='\n'.join([headers, catalunya])))
        data = TsvRelativeMetricSource(src)
        with self.assertRaises(ValueError) as context:
            data.validateMetricGeolevel('population', 'jupiter')
        self.assertEqual("Geolevel jupiter not found for population",
            str(context.exception)
        )

    def test_loadTsvRelativeMetric(self):
        result = loadTsvRelativeMetric()
        self.assertTrue(result)
        self.assertEqual(len(result.getDataObjects('population', 'ccaa')), 20)
        self.assertEqual(len(result.getDataObjects('population', 'state')), 53)
