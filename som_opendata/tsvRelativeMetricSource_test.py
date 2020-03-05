import b2btest
import unittest
from yamlns import namespace as ns
from .distribution import parse_tsv, tuples2objects
from .tsvRelativeMetricSource import (
        TsvRelativeMetricSource,
        loadTsvRelativeMetric,
        getFieldBy,
    )

headers = u"code\tname\tvalue"
catalunya = u"09\tCatalunya\t7416237"
andalusia = u"01\tAndalucia\t8388875"


class TsvRelativeMetricSource_Test(unittest.TestCase):

    def test_getFieldBy_nameByCode(self):
        rawData = '\n'.join([headers,catalunya,andalusia])
        data= tuples2objects(parse_tsv(rawData))
        result = getFieldBy(data=data, field='name', by='code')
        self.assertEqual(result, {'01': 'Andalucia', '09': 'Catalunya'})

    def test_getFieldBy_valueByCode(self):
        rawData = '\n'.join([headers,catalunya,andalusia])
        data= tuples2objects(parse_tsv(rawData))
        result = getFieldBy(data=data, field='value', by='code')
        self.assertEqual(result, {'01': '8388875', '09': '7416237'})
