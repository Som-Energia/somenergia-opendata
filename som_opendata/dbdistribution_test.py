# -*- coding: utf-8 -*-
import unittest
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate
from dbdistribution import (
    extractObjects,
    )

class Dbdistribution_Test(unittest.TestCase):

    def test__extractObjects__membersWorldOneDate(self):
        self.assertEqual(extractObjects('members', ['2018_07_01']),
            [])

    def test__extractObjects__membersWorldOneDateExist(self):
        self.assertEqual(extractObjects('members', ['2015_01_01']),
            [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2015_01_01'],
            ['ES', u'España', '01', 'Andalucia', '04', u'Almería', '04003', 'Adra', '2'],
            ['ES', u'España', '01', 'Andalucia', '04', u'Almería', '04013', u'Almería', '26']
            ])