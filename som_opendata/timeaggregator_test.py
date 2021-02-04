# -*- coding: utf-8 -*-
import unittest
from .timeaggregator import TimeAggregator

class TimeAggregator_Test(unittest.TestCase):

    def assertRequestDatesEqual(self, expected, **kwds):
        aggregator=TimeAggregator(**kwds)
        self.assertEqual(
            aggregator.requestDates,
            expected,
        )

    def assertSourceDatesEqual(self, expected, **kwds):
        aggregator=TimeAggregator(**kwds)
        self.assertEqual(
            aggregator.sourceDates,
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



# vim: et sw=4 ts=4
