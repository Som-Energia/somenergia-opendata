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
from common import (
    dateSequenceWeeks,
    dateSequenceYears,
    requestDates,
    caseFrequency,
    pickDates,
    IsoFrequencyConverte,
    IsoAggregateLevelConverter,
    IsoDateConverter,
    )
from distribution import parse_tsv
from dateutil.relativedelta import relativedelta as delta
from werkzeug.routing import ValidationError

headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"

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
        self.assertEqual(r, ['2018-07-20'])

    def test__requestDates__monthlyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-06-20',
                         to='2018-07-20',
                         periodicity='monthly',
                        )
        self.assertEqual(r, ['2018-06-20', '2018-07-20'])

    def test__requestDates__yearlySameDate(self):
        r = requestDates(first='2000-01-01',
                         since='2018-07-20',
                         to='2018-07-20',
                         periodicity='yearly',
                        )
        self.assertEqual(r, ['2018-07-20'])

    def test__requestDates__yearlyDifferentDate(self):
        r = requestDates(first='2000-01-01',
                         since='2017-07-20',
                         to='2018-07-20',
                         periodicity='yearly',
                        )
        self.assertEqual(r, ['2017-07-20', '2018-07-20'])

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

    def createTuples(self, *lines):
        source = '\n'.join(lines)
        return parse_tsv(source)

    def test__pickDates__oneDateColumn_oneDateRequest(self):
        tuples = self.createTuples(headers, data_Amer)
        r = pickDates(tuples, ['2018-01-01'])
        self.assertEqual(r, [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2018_01_01'],
            ['ES', u'España', '09', 'Catalunya', '17', 'Girona', '17007', 'Amer', '2000']
            ])

    def test__pickDates__twoDateColumn_twoDateRequest(self):
        tuples = self.createTuples(
            headers+'\tcount_2018_02_01',
            data_Amer+'\t20',
            )
        r = pickDates(tuples, ['2018-01-01', '2018-02-01'])
        self.assertEqual(r, [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2018_01_01', 'count_2018_02_01'],
            ['ES', u'España', '09', 'Catalunya', '17', 'Girona', '17007', 'Amer', '2000', '20']
            ])

    def test__pickDates__twoDateColumn_oneDateRequest(self):
        tuples = self.createTuples(
            headers+'\tcount_2018_02_01',
            data_Amer+'\t20',
            )
        r = pickDates(tuples, ['2018-01-01'])
        self.assertEqual(r, [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2018_01_01'],
            ['ES', u'España', '09', 'Catalunya', '17', 'Girona', '17007', 'Amer', '2000']
            ])


    def test__pickDates__moreDateColumn_twoDateRequest(self):
        tuples = self.createTuples(
            headers+'\tcount_2018_01_08'+'\tcount_2018_01_15'+'\tcount_2018_01_22'+'\tcount_2018_01_29'+'\tcount_2018_02_01'+'\tcount_2018_02_05',
            data_Amer+'\t20'+'\t200'+'\t10'+'\t150'+'\t3'+'\t300',
            )
        r = pickDates(tuples, ['2018-01-01', '2018-02-01'])
        self.assertEqual(r, [
            ['codi_pais', 'pais', 'codi_ccaa', 'comunitat_autonoma', 'codi_provincia', 'provincia', 'codi_ine', 'municipi', 'count_2018_01_01', 'count_2018_02_01'],
            ['ES', u'España', '09', 'Catalunya', '17', 'Girona', '17007', 'Amer', '2000', '3']
            ])

    # Convertes
    frequencyConverter = IsoFrequencyConverte({})
    aggregateLevelConverter = IsoAggregateLevelConverter({})
    dateConverter = IsoDateConverter({})

    def test__FrequencyConverter__valid(self):
        r = self.frequencyConverter.to_python('weekly')
        self.assertEqual(r, 'weekly')

    def test__FrequencyConvertes__invalid(self):
        with self.assertRaises(ValidationError) as ctx:
            self.frequencyConverter.to_python('caracola')
        self.assertEquals(format(ctx.exception), 'Incorrect Frequency')

    def test__AggregateLevelConverter__valid(self):
        r = self.aggregateLevelConverter.to_python('countries')
        self.assertEqual(r, 'countries')

    def test__AggregateLevelConverter__invalid(self):
        with self.assertRaises(ValidationError) as ctx:
            self.aggregateLevelConverter.to_python('caracola')
        self.assertEquals(format(ctx.exception), 'Incorrect Aggregate Level')

    def test__DateConverter__valid(self):
        r = self.dateConverter.to_python('2018-01-01')
        self.assertEqual(r, Date('2018-01-01'))

    def test__DateConverter__invalid(self):
        with self.assertRaises(ValueError) as ctx:
            self.dateConverter.to_python('PEP 8')
        self.assertEquals(format(ctx.exception), 'Invalid date initializator \'PEP 8\'')

"""
/version
/members/2015-02
/members/2015-02/weeklyuntil/2015-12
/members/2015-02/monthlyuntil/2015-12
/map/members/...
"""


unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
