# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from ..app import app
from printer import printer_module, validateInputDates


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"

class BaseApi_Test(unittest.TestCase):

    @staticmethod
    def setUpClass():
        BaseApi_Test.maxDiff=100000
        app.config['TESTING']=True

    def setUp(self):
        self.client = app.test_client()
        self.b2bdatapath = 'b2bdata'
        self.oldsource = printer_module.source

    def tearDown(self):
        printer_module.source = self.oldsource

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    from ..testutils import assertNsEqual

    def assertYamlResponse(self, response, expected):
        self.assertNsEqual(response.data, expected)

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    def test_version(self):
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '0.2.0'
            compat: '0.2.0'
            """)

    def test__validateInputDates__since_toDate(self):
        r = validateInputDates(since='2018-01-01', todate='2018-01-02')
        self.assertEqual(r, True)

    def test__validateInputDates__since(self):
        r = validateInputDates(since='2018-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__since_toDate_turnedDates(self):
        r = validateInputDates(since='2010-01-01', todate='2018-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__onDate(self):
        r = validateInputDates(ondate='2010-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__onDate_since(self):
        r = validateInputDates(ondate='2010-01-01', since='2018-01-01')
        self.assertEqual(r, False)

    def test__validateInputDates__onDate_toDate(self):
        r = validateInputDates(ondate='2010-01-01', todate='2018-01-01')
        self.assertEqual(r, False)

    def test__onDate__exists(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/on/2018-01-01')
        self.assertYamlResponse(r, """\
            data: [41660]
            dates: [2018-01-01]
            """)

    def test__onDate_aggregateLevel__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/world/on/2018-01-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01]
            data: [41660]
            """)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__aggregateLevel__existToday(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/printer/members/by/cities')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today())+"""]
            data: [123]
            countries:
              ES:
                name: España
                data: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    data: [123]
                    states:
                      '04':
                        name: Almería
                        data: [123]
                        cities:
                          '04003':
                            name: Adra
                            data: [123]
            """)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__basicUrl__exist(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/printer/members')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today())+"""]
            data: [123]
            """)

    def test__aggregateLevel_frequency__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/countries/yearly')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2010-01-01, 2011-01-01, 2012-01-01, 2013-01-01, 2014-01-01, 2015-01-01, 2016-01-01, 2017-01-01, 2018-01-01]
            data: [0, 0, 1067, 4905, 11748, 17703, 23579, 29946, 41660]
            countries:
              CL:
                name: Chile
                data: [0, 0, 1, 1, 1, 1, 1, 1, 1]
              DE:
                name: Germany
                data: [0, 0, 0, 0, 1, 2, 2, 3, 3]
              ES:
                name: España
                data: [0, 0, 1064, 4898, 11738, 17692, 23568, 29931, 41644]
              FR:
                name: France
                data: [0, 0, 1, 1, 2, 2, 2, 4, 4]
              NL:
                name: Netherlands
                data: [0, 0, 1, 3, 3, 3, 3, 3, 3]
              None:
                name: None
                data: [0, 0, 0, 0, 0, 0, 0, 1, 2]
              PT:
                name: Portugal
                data: [0, 0, 0, 1, 1, 1, 1, 1, 1]
              UK:
                name: United Kingdom
                data: [0, 0, 0, 1, 2, 2, 2, 2, 2]
            """)

    def test__aggregateLevel_frequency_fromDate__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/world/yearly/from/2017-01-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2017-01-01, 2018-01-01]
            data: [29946, 41660]
            """)

    def test__aggregateLevel_frequency_fromDate_toDate__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/world/monthly/from/2018-01-01/to/2018-03-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01, 2018-02-01, 2018-03-01]
            data: [41660, 44402, 45810]
            """)

    def test__aggregateLevel_frequency_toDate__exist(self):
        printer_module.firstDate = '2018-02-01'
        r = self.get('/printer/members/by/world/monthly/to/2018-03-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-02-01, 2018-03-01]
            data: [44402, 45810]
            """)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__frequency_formDate__exist(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()-delta(weeks=1)).replace('-','_')+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123\t1234567',
            )
        r = self.get('/printer/members/weekly/from/'+str(Date.today()-delta(weeks=1)))
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today()-delta(weeks=1))+""", """+str(Date.today())+"""]
            data: [123, 1234567]
            """)

    def test__frequency_fromDate_toDate__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/monthly/from/2018-01-01/to/2018-02-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01, 2018-02-01]
            data: [41660, 44402]
            """)

    def test__urlBaseFrequency__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/yearly')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [
                2010-01-01,
                2011-01-01,
                2012-01-01,
                2013-01-01,
                2014-01-01,
                2015-01-01,
                2016-01-01,
                2017-01-01,
                2018-01-01,
            ]
            data: [
                0,
                0,
                1067,
                4905,
                11748,
                17703,
                23579,
                29946,
                41660
            ]
            """)

    def test__onDate_aggregateLevel_queryParams__exist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/cities/on/2018-01-01?city=17007')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01]
            data: [11]
            countries:
              ES:
                name: España
                data: [11]
                ccaas:
                  '09':
                    name: Cataluña
                    data: [11]
                    states:
                      '17':
                        name: Girona
                        data: [11]
                        cities:
                          '17007':
                            name: Amer
                            data: [11]
            """)

    def test__printerError__datesNotExist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/on/1994-09-01')
        self.assertEqual(r.status_code, 500)
        self.assertYamlResponse(r, """\
            errorId: 1001
            message: Missing Dates ['1994-09-01']
            """)

    def test__printerError__URLparamsNotExist_aggregateLevel(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/piolin')
        self.assertEqual(r.status_code, 404)

    def test__printerError__URLparamsNotExist_frequency(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/piolin')
        self.assertEqual(r.status_code, 404)

    @unittest.skip("Not implemented yet | Caldria retocar el converter de Date")
    def test__printerError__URLparamsNotExist_date(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/on/piolin')
        self.assertEqual(r.status_code, 404)

    def test__printerError__queryParamsNotExist(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/cities/on/2018-01-01?city=9999999')
        self.assertYamlResponse(r, ns())

    def test__printerError__incorrectFormatDates(self):
        printer_module.firstDate = '2010-01-01'
        r = self.get('/printer/members/by/cities/on/2018-01-01/from/2018-02-02')
        self.assertEqual(r.status_code, 404)


    def test__printerError_frequency_toDate__exist_NoExactFirstDate(self):
        printer_module.firstDate = '2018-01-15'
        r = self.get('/printer/members/by/cities/monthly/to/2018-03-01')
        self.assertEqual(r.status_code, 500)
        self.assertYamlResponse(r, """\
                errorId: 1001
                message: Missing Dates ['2018-02-15', '2018-01-15']
            """)





unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
