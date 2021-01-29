# -*- encoding: utf-8 -*-
import unittest
from datetime import timedelta
from werkzeug.routing import ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from .common import (
    previousFirstOfMonth,
    dateSequenceYears,
    dateSequenceMonths,
    dateSequenceWeeks,
    IsoDateConverter,
    requestDates,
    validateParams,
    ValidateError,
    validateMapParams,
    )

class DateSequence_Test(unittest.TestCase):

    # dateSequenceMonths

    def test_dateSequenceMonths_noStartEnd_today(self):
        self.assertEqual(
            dateSequenceMonths(None, None), [
            Date.today().replace(day=1),
            ])

    def test_dateSequenceMonth_singleDate_thatDate(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', None), [
            Date('2015-01-01'),
            ])

    def test_dateSequenceMonths_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', '2015-01-08'), [
            Date('2015-01-01'),
            ])

    def test_dateSequenceMonths_twoDatesBeyondMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-01', '2015-02-01'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            ])

    def test_dateSequenceMonths_midMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-05', '2015-02-05'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            ])

    def test_dateSequenceMonths_nearlyMidMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-05', '2015-02-04'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            ])

    def test_dateSequenceMonths_lateMonth(self):
        self.assertEqual(
            dateSequenceMonths('2015-01-31', '2015-04-30'), [
            Date('2015-01-01'),
            Date('2015-02-01'),
            Date('2015-03-01'),
            Date('2015-04-01'),
            ])

    def test_dateSequenceMonths_moreThanAYear(self):
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
            Date.today()-timedelta(days=Date.today().isoweekday()-1%7),
            ])

    def test_dateSequenceWeeks_singleDate_thatDate(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', None), [
            Date('2014-12-29'),
            ])

    def test_dateSequenceWeeks_twoDatesUnderAMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', '2015-01-08'), [
            Date('2014-12-29'),
            Date('2015-01-05'),
            ])

    def test_dateSequenceWeeks_twoDatesBeyondMonth(self):
        self.assertEqual(
            dateSequenceWeeks('2015-01-01', '2015-02-01'), [
            Date('2014-12-29'),
            Date('2015-01-05'),
            Date('2015-01-12'),
            Date('2015-01-19'),
            Date('2015-01-26'),
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
            Date('2015-01-26'),
            Date('2015-02-02'),
            Date('2015-02-09'),
            Date('2015-02-16'),
            Date('2015-02-23'),
            Date('2015-03-02'),
            Date('2015-03-09'),
            Date('2015-03-16'),
            Date('2015-03-23'),
            Date('2015-03-30'),
            Date('2015-04-06'),
            Date('2015-04-13'),
            Date('2015-04-20'),
            Date('2015-04-27'),
            ])


    # dateSequenceYears

    def test_dateSequenceYears_noStartEnd_today(self):
        self.assertEqual(
            dateSequenceYears(None, None), [
            Date.today().replace(day=1, month=1),
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
            Date('2015-01-01'),
            Date('2016-01-01'),
            ])

    def test_dateSequenceYears_29february(self):
        self.assertEqual(
            dateSequenceYears('2012-02-29', '2016-04-30'), [
            Date('2012-01-01'),
            Date('2013-01-01'),
            Date('2014-01-01'),
            Date('2015-01-01'),
            Date('2016-01-01'),
            ])

class Common_Test(unittest.TestCase):

    # requestDates

    def assertRequestDatesEqual(self, expected, **kwds):
        r=requestDates(**kwds)
        self.assertEqual(r,expected)

    def test__requestDates__last(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            last= '2010-01-01',
            expected = [
                '2010-01-01',
            ])

    def test__requestDates__onDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            on='2018-07-20',
            expected = [
                '2018-07-01',
            ])

    def test__requestDates__weeklySameDate(self):
        self.assertRequestDatesEqual(
            periodicity='weekly',
            first='2000-01-01',
            since='2018-07-20',
            to=   '2018-07-20',
            expected = [
                '2018-07-16',
            ])

    def test__requestDates__weeklyDifferentDate(self):
        self.assertRequestDatesEqual(
            periodicity='weekly',
            first='2000-01-01',
            since='2018-07-10',
            to=   '2018-07-20',
            expected = [
                '2018-07-09',
                '2018-07-16',
            ])

    def test__requestDates__monthlySameDate(self):
        self.assertRequestDatesEqual(
            periodicity='monthly',
            first='2000-01-01',
            since='2018-07-20',
            to=   '2018-07-20',
            expected = [
                '2018-07-01',
            ])

    def test__requestDates__monthlyDifferentDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2018-06-20',
            to='2018-07-20',
            periodicity='monthly',
            expected = [
                '2018-06-01',
                '2018-07-01',
            ])

    def test__requestDates__yearlySameDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2018-07-20',
            to='2018-07-20',
            periodicity='yearly',
            expected = [
                '2018-01-01',
            ])

    def test__requestDates__yearlyDifferentDate(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            since='2017-07-20',
            to=   '2018-07-20',
            periodicity='yearly',
            expected = [
                '2017-01-01',
                '2018-01-01',
            ])

    def test__requestDates__toWithoutSince(self):
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

    def test__requestDates__turnedDates(self):
        self.assertRequestDatesEqual(
            periodicity='monthly',
            first='2000-01-01',
            since='2018-02-01',
            to='2018-01-01',
            expected = [
                # empty
            ])

    def test__requestDates__onMidMonth(self):
        self.assertRequestDatesEqual(
            first='2000-01-01',
            on='2018-01-12',
            expected = [
                '2018-01-01',
            ])

    def test_previousFirstOfMonth_withAFirst(self):
        self.assertEqual(
            previousFirstOfMonth('2018-02-01'),
            '2018-02-01'
            )

    def test_previousFirstOfMonth_whenWithin(self):
        self.assertEqual(
            previousFirstOfMonth('2018-02-12'),
            '2018-02-01'
            )


    # Convertes

    def test__DateConverter__valid(self):
        dateConverter = IsoDateConverter({})
        r = dateConverter.to_python('2018-01-01')
        self.assertEqual(r, Date('2018-01-01'))

    def test__DateConverter__invalid(self):
        dateConverter = IsoDateConverter({})
        with self.assertRaises(ValidationError) as ctx:
            dateConverter.to_python('Thisisnotadate')
        self.assertEqual(format(ctx.exception), 'Thisisnotadate')


    # validateParams 

    def test__validateParams_valid(self):
        # not raises
        validateParams(
            metric='members',
            geolevel='ccaa',
            relativemetric=None,
            frequency=None,
        )

    def test__validateParams_badMetric(self):
        with self.assertRaises(ValidateError) as ctx:
            validateParams(
                metric='badvalue', # fail
                geolevel='ccaa',
                relativemetric=None,
                frequency=None,
            )
        self.assertEqual(ctx.exception.parameter, 'metric')
        self.assertEqual(ctx.exception.value, 'badvalue')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description, 
            "Invalid metric 'badvalue'. Accepted ones are 'members', 'newmembers', 'canceledmembers', 'contracts', 'newcontracts', 'canceledcontracts'.")

    # validateMapParams

    def test__validateMapParams__valid(self):
        validateMapParams(
            metric='members',
            geolevel='ccaa',
            relativemetric = 'population',
        )

    def test__validateMapParams__wrongRelativeMetricValue(self):
        with self.assertRaises(ValidateError) as ctx:
            validateMapParams(relativemetric='dogs')

        self.assertEqual(ctx.exception.parameter, 'relativemetric')
        self.assertEqual(ctx.exception.value, 'dogs')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description,
            "Invalid relativemetric 'dogs'. Accepted ones are 'population', None.")

    def test__validateMapParams__notImplementedValue(self):
        with self.assertRaises(ValidateError) as ctx:
            validateMapParams(geolevel='city') # not implemented
        self.assertEqual(ctx.exception.parameter, 'geolevel')
        self.assertEqual(ctx.exception.value, 'city')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description,
            "Invalid geolevel 'city'. Accepted ones are 'ccaa', 'state'.")

# vim: et ts=4 sw=4
