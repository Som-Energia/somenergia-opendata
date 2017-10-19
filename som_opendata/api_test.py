# -*- encoding: utf-8 -*-

import unittest
import b2btest
from yamlns import namespace as ns
from yamlns.dateutils import Date
from som_opendata.api import (
    app,
    dateSequence,
    contractsSparse,
    contractsSeries,
    membersSparse,
    )
from dbutils import csvTable


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

    def assertYamlResponse(self, response, expected):
        self.assertMultiLineEqual(
            ns.loads(response.data).dump(),
            ns.loads(expected).dump(),
        )

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    # dateSequence

    def test_dateSequence_noStartEnd_today(self):
        self.assertEqual(
            dateSequence(None, None), [
            Date.today(),
            ])

    def test_dateSequence_singleDate_thatDate(self):
        self.assertEqual(
            dateSequence('2015-01-01', None), [
            Date('2015-01-01'),
            ])

    def test_dateSequence_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequence('2015-01-01', '2015-01-08'), [
            Date('2015-01-01'),
            ])

    def test_dateSequence_twoDatesBeyondMonth(self):
        self.assertEqual(
            dateSequence('2015-01-01', '2015-02-01'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            ])

    def test_dateSequence_midMonth(self):
        self.assertEqual(
            dateSequence('2015-01-05', '2015-02-05'), [
            Date('2015-01-05'),
            Date('2015-02-05'),
            ])

    def test_dateSequence_nearlyMidMonth(self):
        self.assertEqual(
            dateSequence('2015-01-05', '2015-02-04'), [
            Date('2015-01-05'),
            ])

    def test_dateSequence_lateMonth(self):
        self.assertEqual(
            dateSequence('2015-01-31', '2015-04-30'), [
            Date('2015-01-31'),
            Date('2015-02-28'),
            Date('2015-03-31'),
            Date('2015-04-30'),
            ])

    def test_dateSequence_moreThanAYear(self):
        self.assertEqual(
            dateSequence('2014-12-01', '2016-02-01'), [
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
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '1.0'
            """)

    def test_contracts_single(self):
        r = self.get('/contracts/2015-01-01')
        self.assertTsvResponse(r)

    def test_contracts_series(self):
        r = self.get('/contracts/2015-01-01/monthlyto/2015-04-01')
        self.assertTsvResponse(r)

    def _test_members(self):
        r = self.get('/members/2015-01-01')
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
