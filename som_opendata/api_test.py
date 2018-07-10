# -*- encoding: utf-8 -*-

import unittest
import b2btest
from yamlns import namespace as ns
from yamlns.dateutils import Date
from api import (
    dateSequenceMonths,
    contractsSparse,
    contractsSeries,
    membersSparse,
    )
from app import app
from dbutils import csvTable
from common import dateSequenceWeeks, dateSequenceYears


class BaseApi_Test(unittest.TestCase):

    @staticmethod
    def setUpClass():
        #BaseApi_Test.maxDiff=None
        app.config['TESTING']=True

    def setUp(self):
        self.client = app.test_client()
        self.b2bdatapath = 'b2bdata'

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    from .testutils import assertNsEqual

    def assertYamlResponse(self, response, expected):
        self.assertNsEqual(response.data, expected)

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    # dateSequenceMonths

    def test_dateSequence_noStartEnd_today(self):
        self.assertEqual(
            dateSequenceMonths(None, None), [
            Date.today(),
            ])

    def test_dateSequence_singleDate_thatDate(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', None), [
            Date('2015-01-01'),
            ])

    def test_dateSequence_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', '2015-01-08'), [
            Date('2015-01-01'),
            ])

    def test_dateSequence_twoDatesBeyondMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', '2015-02-01'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            ])

    def test_dateSequence_midMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-05', '2015-02-05'), [
            Date('2015-01-05'),
            Date('2015-02-05'),
            ])

    def test_dateSequence_nearlyMidMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-05', '2015-02-04'), [
            Date('2015-01-05'),
            ])

    def test_dateSequence_lateMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-31', '2015-04-30'), [
            Date('2015-01-31'),
            Date('2015-02-28'),
            Date('2015-03-31'),
            Date('2015-04-30'),
            ])

    def test_dateSequence_moreThanAYear(self):
        self.assertEqual(
            dateSequenceMonths('2014-12-01', '2016-02-01'), [
            Date('2014-12-01'),
            Date('2015-01-01'),
            Date('2015-02-01'),
            Date('2015-03-01'),
            Date('2015-04-01'),
            Date('2015-05-01'),
            Date('2015-06-01'),
            Date('2015-07-01'),
            Date('2015-08-01'),
            Date('2015-09-01'),
            Date('2015-10-01'),
            Date('2015-11-01'),
            Date('2015-12-01'),
            Date('2016-01-01'),
            Date('2016-02-01'),
            ])


    # dateSequenceWeeks

    def test_dateSequenceWeeks_noStartEnd_today(self):
        self.assertEqual(
            dateSequenceWeeks(None, None), [
            Date.today(),
            ])

    def test_dateSequenceWeeks_singleDate_thatDate(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', None), [
            Date('2015-01-01'),
            ])

    def test_dateSequenceWeeks_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', '2015-01-08'), [
            Date('2015-01-01'),
            Date('2015-01-08'),
            ])

    def test_dateSequenceWeeks_twoDatesBeyondMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', '2015-02-01'), [
            Date('2015-01-01'),
            Date('2015-01-08'),
            Date('2015-01-15'),
            Date('2015-01-22'),
            Date('2015-01-29'),
            ])

    def test_dateSequenceWeeks_midMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-05', '2015-02-05'), [
            Date('2015-01-05'),
            Date('2015-01-12'),
            Date('2015-01-19'),
            Date('2015-01-26'),
            Date('2015-02-02'),
            ])

    def test_dateSequenceWeeks_nearlyMidMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-05', '2015-02-04'), [
            Date('2015-01-05'),
            Date('2015-01-12'),
            Date('2015-01-19'),
            Date('2015-01-26'),
            Date('2015-02-02'),
            ])

    def test_dateSequenceWeeks_lateMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-31', '2015-04-30'), [
            Date('2015-01-31'),
            Date('2015-02-07'),
            Date('2015-02-14'),
            Date('2015-02-21'),
            Date('2015-02-28'),
            Date('2015-03-07'),
            Date('2015-03-14'),
            Date('2015-03-21'),
            Date('2015-03-28'),
            Date('2015-04-04'),
            Date('2015-04-11'),
            Date('2015-04-18'),
            Date('2015-04-25'),
            ])


    # dateSequenceYears

    def test_dateSequenceYears_noStartEnd_today(self):
        self.assertEqual(
            dateSequenceYears(None, None), [
            Date.today(),
            ])

    def test_dateSequenceYears_singleDate_thatDate(self):
        self.assertEqual(
            dateSequenceYears('2015-01-01', None), [
            Date('2015-01-01'),
            ])

    def test_dateSequenceYears_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequenceYears('2015-01-01', '2015-01-08'), [
            Date('2015-01-01')
            ])

    def test_dateSequenceYears_2years(self):
        self.assertEqual(
            dateSequenceYears('2015-01-31', '2016-04-30'), [
            Date('2015-01-31'),
            Date('2016-01-31'),
            ])

    def test_dateSequenceYears_29february(self):
        self.assertEqual(
            dateSequenceYears('2012-02-29', '2016-04-30'), [
            Date('2012-02-29'),
            Date('2013-02-28'),
            Date('2014-02-28'),
            Date('2015-02-28'),
            Date('2016-02-29'),
            ])


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


    def test_version(self):
        r = self.get('/old/version')
        self.assertYamlResponse(r, """\
            version: '1.0'
            """)

    def test_contracts_single(self):
        r = self.get('/old/contracts/2015-01-01')
        self.assertTsvResponse(r)

    def test_contracts_series(self):
        r = self.get('/old/contracts/2015-01-01/monthlyto/2015-04-01')
        self.assertTsvResponse(r)

    def test_members_single(self):
        r = self.get('/old/members/2015-01-01')
        self.assertTsvResponse(r)

    def test_members_series(self):
        r = self.get('/old/members/2015-01-01/monthlyto/2015-04-01')
        self.assertTsvResponse(r)



"""
/version
/members/2015-02
/members/2015-02/weeklyuntil/2015-12
/members/2015-02/monthlyuntil/2015-12
/map/members/...
"""


unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
