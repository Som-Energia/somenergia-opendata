# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from dbutils import csvTable
from werkzeug.routing import ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from .queries import (
    contractsSparse,
    contractsSeries,
    membersSparse,
    newContractsSeries,
    canceledContractsSeries,
    newMembersSeries,
    canceledMembersSeries,
    )
import os


#@unittest.skipIf(True, "No database connection")
@unittest.skipIf("TRAVIS" in os.environ, "requires acces to db")
class Queries_Test(unittest.TestCase):

    def setUp(self):
        self.b2bdatapath = 'b2bdata'

    def test_contractsSparse_single(self):
        dates = ['2015-01-01']
        result = contractsSparse(dates)
        self.assertB2BEqual(result)

    def test_contractsSparse_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = contractsSparse(dates)
        self.assertB2BEqual(result)

    def test_contractsSeries_single(self):
        dates = ['2015-01-01']
        result = contractsSeries(dates)
        self.assertB2BEqual(result)

    def test_contractsSeries_many(self):
        dates = ['2015-01-01','2015-02-01']
        result = contractsSeries(dates)
        self.assertB2BEqual(result)


    def test_membersSparse_single(self):
        dates = ['2015-01-01']
        result = membersSparse(dates, csvTable)
        self.assertB2BEqual(result)

    def test_membersSparse_many(self):
        # TODO: Not implemented (b2b expects same as single)
        dates = ['2015-01-01','2015-02-01']
        result = membersSparse(dates, csvTable)
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


# vim: et ts=4 sw=4
