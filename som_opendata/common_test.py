# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from datetime import timedelta
from werkzeug.routing import ValidationError
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from .common import (
    caseFrequency,
    dateSequenceYears,
    dateSequenceMonths,
    dateSequenceWeeks,
    IsoDateConverter,
    requestDates,
    validateParams,
    )
from .Errors import ValidateError

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

    # caseFrequency

    def test__caseFrequency__weekly(self):
        r = caseFrequency('weekly')
        self.assertEqual(r, dateSequenceWeeks)

    def test__caseFrequency__monthly(self):
        r = caseFrequency('monthly')
        self.assertEqual(r, dateSequenceMonths)

    def test__caseFrequency__yearly(self):
        r = caseFrequency('yearly')
        self.assertEqual(r, dateSequenceYears)

    # requestDates

    @unittest.skip("Need MockUp?")
    def test__requestDates__toDay(self):
        r = self.requestDates(first='2000-01-01')
        self.assertEqual(r, [str(Date.today()-timedelta(days=Date.today().isoweekday()-1%7))])

    def test__requestDates__onDate(self):
        r = requestDates(first='2000-01-01',
                         on='2018-07-20',
                        )
        self.assertEqual(r, ['2018-07-16'])

    def test__requestDates__weeklySameDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-20',
                         to='2018-07-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2018-07-16'])

    def test__requestDates__weeklyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-10',
                         to='2018-07-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2018-07-09', '2018-07-16'])

    def test__requestDates__monthlySameDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-20',
                         to='2018-07-20',
                         periodicity='monthly',
                        )
        self.assertEqual(r, ['2018-07-01'])

    def test__requestDates__monthlyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-06-20',
                         to='2018-07-20',
                         periodicity='monthly',
                        )
        self.assertEqual(r, ['2018-06-01', '2018-07-01'])

    def test__requestDates__yearlySameDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-20',
                         to='2018-07-20',
                         periodicity='yearly',
                        )
        self.assertEqual(r, ['2018-01-01'])

    def test__requestDates__yearlyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2017-07-20',
                         to='2018-07-20',
                         periodicity='yearly',
                        )
        self.assertEqual(r, ['2017-01-01', '2018-01-01'])

    def test__requestDates__toWithoutSince(self):
        r = requestDates(first='2011-01-01',
                         to='2011-01-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2010-12-27', '2011-01-03', '2011-01-10', '2011-01-17'])

    def test__requestDates__turnedDates(self):
        r = requestDates(first='2000-01-01',
                         since='2018-02-01',
                         to='2018-01-01',
                         periodicity='monthly',
                        )
        self.assertEqual(r, [])


    # Convertes

    def test__DateConverter__valid(self):
        dateConverter = IsoDateConverter({})
        r = dateConverter.to_python('2018-01-01')
        self.assertEqual(r, Date('2018-01-01'))

    def test__DateConverter__invalid(self):
        dateConverter = IsoDateConverter({})
        with self.assertRaises(ValueError) as ctx:
            dateConverter.to_python('PEP 8')
        self.assertEqual(format(ctx.exception), 'Invalid date initializator \'PEP 8\'')


    # validateParams 

    def test__validateParams__valid(self):
        self.assertEqual(validateParams('metric', 'members'), None)

    def test__validateParams__invalidValue(self):
        with self.assertRaises(ValidateError) as ctx:
            validateParams('metric', 'error')
        self.assertEqual(ctx.exception.metric, 'metric')
        self.assertEqual(ctx.exception.value, 'error')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description, 
            'Incorrect metric \'error\' try with [\'members\', \'contracts\']')

    @unittest.skip('TODO BUG')
    def test__validateParams__invalidKey(self):
        with self.assertRaises(ValidateError) as ctx:
            validateParams('error', 'error')
        self.assertEqual(ctx.exception.metric, 'error')
        self.assertEqual(ctx.exception.value, 'error')
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.description, 
            'Incorrect metric \'error\' try with [\'members\', \'contracts\']')



# vim: et ts=4 sw=4
