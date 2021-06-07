# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from dbutils import csvTable
from werkzeug.routing import ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from .queries import (
    contractsSeries,
    membersSeries,
    newContractsSeries,
    canceledContractsSeries,
    selfConsumptionContractsSeries,
    newSelfConsumptionContractsSeries,
    canceledSelfConsumptionContractsSeries,
    newMembersSeries,
    canceledMembersSeries,
    plantPowerSeries,
    )
import os


#@unittest.skipIf(True, "No database connection")
@unittest.skipIf("TRAVIS" in os.environ, "requires acces to db")
class Queries_Test(unittest.TestCase):

    def setUp(self):
        self.b2bdatapath = 'b2bdata'

    def test_contractsSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = contractsSeries(dates)
        self.assertB2BEqual(result)

    def test_membersSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = membersSeries(dates, csvTable)
        self.assertB2BEqual(result)

    def test_newContractsSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = newContractsSeries(dates)
        self.assertB2BEqual(result)

    def test_canceledContractsSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = canceledContractsSeries(dates)
        self.assertB2BEqual(result)

    def test_newMembersSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = newMembersSeries(dates)
        self.assertB2BEqual(result)

    def test_canceledMembersSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = canceledMembersSeries(dates)
        self.assertB2BEqual(result)

    def test_selfConsumptionContractsSeries_many(self):
        dates = ['2020-10-01','2020-11-01']
        result = selfConsumptionContractsSeries(dates)
        self.assertB2BEqual(result)

    def test_newSelfConsumptionContractsSeries_many(self):
        dates = ['2020-10-01','2020-11-01']
        result = newSelfConsumptionContractsSeries(dates)
        self.assertB2BEqual(result)

    def test_canceledSelfConsumptionContractsSeries_many(self):
        dates = ['2020-10-01','2020-11-01']
        result = canceledSelfConsumptionContractsSeries(dates)
        self.assertB2BEqual(result)

    def test_plantPowerSeries_single(self):
        dates = ['2015-01-01', '2020-10-01']
        result = plantPowerSeries(dates)
        self.assertB2BEqual(result)

# vim: et ts=4 sw=4
