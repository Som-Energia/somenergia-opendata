# -*- coding: utf-8 -*-
import unittest
from .timeaggregator import (
    fullYear,
    TimeAggregator,
    TimeAggregatorSum,
)

class TimeAggregator_Test(unittest.TestCase):

    Aggregator = TimeAggregator

    def assertRequestDatesEqual(self, expected, **kwds):
        aggregator=self.Aggregator(**kwds)
        self.assertEqual(
            aggregator.requestDates,
            expected,
        )

    def assertSourceDatesEqual(self, expected, **kwds):
        aggregator=self.Aggregator(**kwds)
        self.assertEqual(
            aggregator.sourceDates,
            expected,
        )

    def assertAggregated(self, expected, input, **kwds):
        aggregator=self.Aggregator(**kwds)
        self.assertEqual(
            aggregator.aggregate(input),
            expected,
        )

    def test__outputDates__last(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            last= '2010-01-01',
            expected = [
                '2010-01-01',
            ])

    def test__outputDates__onDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            on='2018-07-20',
            expected = [
                '2018-07-01',
            ])

    def test__outputDates__weeklySameDate(self):
        self.assertRequestDatesEqual(
            periodicity='weekly',
            first='2000-01-01',
            since='2018-07-20',
            to=   '2018-07-20',
            expected = [
                '2018-07-16',
            ])

    def test__outputDates__weeklyDifferentDate(self):
        self.assertRequestDatesEqual(
            periodicity='weekly',
            first='2000-01-01',
            since='2018-07-10',
            to=   '2018-07-20',
            expected = [
                '2018-07-09',
                '2018-07-16',
            ])

    def test__outputDates__monthlySameDate(self):
        self.assertRequestDatesEqual(
            periodicity='monthly',
            first='2000-01-01',
            since='2018-07-20',
            to=   '2018-07-20',
            expected = [
                '2018-07-01',
            ])

    def test__outputDates__monthlyDifferentDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2018-06-20',
            to='2018-07-20',
            periodicity='monthly',
            expected = [
                '2018-06-01',
                '2018-07-01',
            ])

    def test__outputDates__yearlySameDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2018-07-20',
            to='2018-07-20',
            periodicity='yearly',
            expected = [
                '2018-01-01',
            ])

    def test__outputDates__yearlyDifferentDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            expected = [
                '2017-01-01',
                '2018-01-01',
            ])

    def test__outputDates__toWithoutSince(self):
        self.assertRequestDatesEqual(
            periodicity='weekly',
            first='2011-01-01',
            to=   '2011-01-20',
            expected = [
                '2010-12-27',
                '2011-01-03',
                '2011-01-10',
                '2011-01-17',
            ])

    def test__outputDates__turnedDates(self):
        self.assertRequestDatesEqual(
            periodicity='monthly',
            first='2000-01-01',
            since='2018-02-01',
            to='2018-01-01',
            expected = [
                # empty
            ])

    def test__outputDates__onMidMonth(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            on='2018-01-12',
            expected = [
                '2018-01-01',
            ])

    def test__sourceDates__yearlyDifferentDate(self):
        self.assertSourceDatesEqual(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            expected = [
                '2017-01-01',
                '2018-01-01',
            ])

    def test__aggregated__identity(self):
        self.assertAggregated(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            input = [
                1,
                2,
            ],
            expected = [
                1,
                2,
            ])


class TimeAggregatorSum_Test(TimeAggregator_Test):

    Aggregator = TimeAggregatorSum


    def test_fullYear(self):

        self.assertEqual(
            fullYear('2017-01-01'), [
                '2016-02-01',
                '2016-03-01',
                '2016-04-01',
                '2016-05-01',
                '2016-06-01',
                '2016-07-01',
                '2016-08-01',
                '2016-09-01',
                '2016-10-01',
                '2016-11-01',
                '2016-12-01',
                '2017-01-01',
            ]
        )

    def test__sourceDates__yearlyDifferentDate(self):
        self.assertSourceDatesEqual(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            expected = [
                '2016-02-01',
                '2016-03-01',
                '2016-04-01',
                '2016-05-01',
                '2016-06-01',
                '2016-07-01',
                '2016-08-01',
                '2016-09-01',
                '2016-10-01',
                '2016-11-01',
                '2016-12-01',
                '2017-01-01',
                '2017-02-01',
                '2017-03-01',
                '2017-04-01',
                '2017-05-01',
                '2017-06-01',
                '2017-07-01',
                '2017-08-01',
                '2017-09-01',
                '2017-10-01',
                '2017-11-01',
                '2017-12-01',
                '2018-01-01',
            ])

    def test__sourceDates__sourceDatesBeforeFirst(self):
        self.assertSourceDatesEqual(
            first='2017-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            expected = [
                '2017-01-01',
                '2017-02-01',
                '2017-03-01',
                '2017-04-01',
                '2017-05-01',
                '2017-06-01',
                '2017-07-01',
                '2017-08-01',
                '2017-09-01',
                '2017-10-01',
                '2017-11-01',
                '2017-12-01',
                '2018-01-01',
            ])


    def test__aggregated__identity(self):
        self.assertAggregated(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            input = [
                1,2,3,4,5,6,7,8,9,10,11,12,
                10,20,30,40,50,60,70,80,90,100,110,120,
            ],
            expected = [
                78,
                780,
            ])

    def test__aggregated__sourceDatesBeforeFirst(self):
        self.assertAggregated(
            first='2017-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            input = [
                12,
                10,20,30,40,50,60,70,80,90,100,110,120,
            ],
            expected = [
                12,
                780,
            ])


    def test_Create_sum(self):
        timeDomain = TimeAggregator.Create(
            operator='sum',
            first='2000-01-01',
            last= '2010-01-01',
        )
        self.assertEqual(type(timeDomain), TimeAggregatorSum)

    def test_Create_last(self):
        timeDomain = TimeAggregator.Create(
            operator='last',
            first='2000-01-01',
            last= '2010-01-01',
        )
        self.assertEqual(type(timeDomain), TimeAggregator)



# vim: et sw=4 ts=4
