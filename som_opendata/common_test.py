# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
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
    GeoLevelConverter,
    FrequencyConverter,
    MetricConverter,
    requestDates,
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

    def test__requestDates__toDay(self):
        r = requestDates(first='2000-01-01',
                        )
        self.assertEqual(r, [str(Date.today())])

    def test__requestDates__onDate(self):
        r = requestDates(first='2000-01-01',
                         on='2018-07-20',
                        )
        self.assertEqual(r, ['2018-07-20'])

    def test__requestDates__weeklySameDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-20',
                         to='2018-07-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2018-07-20'])

    def test__requestDates__weeklyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-10',
                         to='2018-07-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2018-07-10', '2018-07-17'])

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
        r = requestDates(first='2000-01-01',
                         to='2000-01-20',
                         periodicity='weekly',
                        )
        self.assertEqual(r, ['2000-01-01', '2000-01-08', '2000-01-15'])

    def test__requestDates__sinceWithoutTo(self):
        r = requestDates(first='2000-01-01',
                         since=str(Date.today()-delta(weeks=1)),
                         periodicity='weekly',
                        )
        self.assertEqual(r, [str(Date.today()-delta(weeks=1)), str(Date.today())])

    def test__requestDates__turnedDates(self):
        r = requestDates(first='2000-01-01',
                         since='2018-02-01',
                         to='2018-01-01',
                         periodicity='monthly',
                        )
        self.assertEqual(r, [])


    # Convertes

    def test__FrequencyConverter__valid(self):
        frequencyConverter = FrequencyConverter({})
        r = frequencyConverter.to_python('monthly')
        self.assertEqual(r, 'monthly')

    def test__FrequencyConvertes__invalid(self):
        frequencyConverter = FrequencyConverter({})
        with self.assertRaises(ValidationError) as ctx:
            frequencyConverter.to_python('badfrequency')
        self.assertEqual(format(ctx.exception),
            "Incorrect frequency 'badfrequency'. "
            "Try with: 'monthly', 'yearly'")

    def test__MetricConverter__valid(self):
        metricConverter = MetricConverter({})
        r = metricConverter.to_python('members')
        self.assertEqual(r, 'members')

    def test__MetricConverter__invalid(self):
        metricConverter = MetricConverter({})
        with self.assertRaises(ValidationError) as ctx:
            metricConverter.to_python('badmetric')
        self.assertEqual(format(ctx.exception),
            "Incorrect metric 'badmetric'. "
            "Try with: 'members', 'contracts'"
        )

    def test__AggregateLevelConverter__valid(self):
        aggregateLevelConverter = GeoLevelConverter({})
        r = aggregateLevelConverter.to_python('country')
        self.assertEqual(r, 'country')

    def test__AggregateLevelConverter__invalid(self):
        aggregateLevelConverter = GeoLevelConverter({})
        with self.assertRaises(ValidationError) as ctx:
            aggregateLevelConverter.to_python('badlevel')
        self.assertEqual(format(ctx.exception),
            "Incorrect geographical level 'badlevel'. "
            "Try with: 'world', 'country', 'ccaa', 'state', 'city'")

    def test__DateConverter__valid(self):
        dateConverter = IsoDateConverter({})
        r = dateConverter.to_python('2018-01-01')
        self.assertEqual(r, Date('2018-01-01'))

    def test__DateConverter__invalid(self):
        dateConverter = IsoDateConverter({})
        with self.assertRaises(ValueError) as ctx:
            dateConverter.to_python('PEP 8')
        self.assertEqual(format(ctx.exception), 'Invalid date initializator \'PEP 8\'')


# vim: et ts=4 sw=4
