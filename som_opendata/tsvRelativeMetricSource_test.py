import b2btest
import unittest
from yamlns import namespace as ns
from .tsvRelativeMetricSource import (
        TsvRelativeMetricSource,
        loadTsvRelativeMetric,
        getFieldBy,
    )


class TsvRelativeMetricSource_Test(unittest.TestCase):

    def test_getFieldBy_nameByCode(self):
        data= [
                {'code':'01', 'name': 'Andalucia', 'value': '50000'},
                {'code':'09', 'name': 'Catalunya', 'value': '70000'},
            ]
        result = getFieldBy(data=data, field='name', by='code')
        self.assertEqual(result, {'01': 'Andalucia', '09': 'Catalunya'})

    def test_getFieldBy_valueByCode(self):
        data= [
                {'code':'01', 'name': 'Andalucia', 'value': '50000'},
                {'code':'09', 'name': 'Catalunya', 'value': '70000'},
            ]
        result = getFieldBy(data=data, field='value', by='code')
        self.assertEqual(result, {'01': '50000', '09': '70000'})
