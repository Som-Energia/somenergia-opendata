# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from dbutils import csvTable
from werkzeug.routing import ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from .oldapi import (
    contractsSparse,
    contractsSeries,
    membersSparse,
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


# vim: et ts=4 sw=4
