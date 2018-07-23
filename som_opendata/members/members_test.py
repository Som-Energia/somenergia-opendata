# -*- encoding: utf-8 -*-

import unittest
import b2btest
from ..app import app
from members import members_modul
from yamlns.dateutils import Date
from dateutil.relativedelta import relativedelta as delta

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
        self.oldsource = members_modul.source

    def tearDown(self):
        members_modul.source = self.oldsource

    def setupSource(self, *lines):
        members_modul.source = '\n'.join(lines)
        members_modul.firstDate = '2000-01-01'

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    from ..testutils import assertNsEqual

    def assertYamlResponse(self, response, expected):
        self.assertNsEqual(response.data, expected)

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    def test__onDate__exists(self):
        self.setupSource(
            headers,
            data_SantJoan,
            )
        r = self.get('/members/on/2018-01-01')
        self.assertYamlResponse(r, """\
            data: [1000]
            dates: [2018-01-01]
            """)

    def test__onDate__moreCities(self):
        self.setupSource(
            headers,
            data_Adra,
            data_Amer,
            data_SantJoan,
            data_Perignan,
            )
        r = self.get('/members/on/2018-01-01')
        self.assertYamlResponse(r, """\
            data: [3012]
            dates: [2018-01-01]
            """)

    def test__onDate_aggregateLevel__exist(self):
        self.setupSource(
            headers,
            data_Adra,
            )
        r = self.get('/members/by/cities/on/2018-01-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01]
            data: [2]
            countries:
              ES:
                name: España
                data: [2]
                ccaas:
                  '01':
                    name: Andalucía
                    data: [2]
                    states:
                      '04':
                        name: Almería
                        data: [2]
                        cities:
                          '04003':
                            name: Adra
                            data: [2]
            """)

    def test__aggregateLevel__exist(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/members/by/cities')
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

    def test__basicUrl__exist(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/members')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today())+"""]
            data: [123]
            """)

    def test__aggregateLevel_frequency__exist(self):
        self.setupSource(
            headers+'\tcount_2018_05_01',
            data_Adra+'\t123',
            )
        r = self.get('/members/by/countries/monthly')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01, 2018-05-01]
            data: [2, 123]
            countries:
              ES:
                name: España
                data: [2, 123]
            """)

    def test__aggregateLevel_frequency_fromDate__exist(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()-delta(weeks=1)).replace('-','_')+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123\t1234567',
            )
        r = self.get('/members/by/countries/weekly/from/'+str(Date.today()-delta(weeks=1)))
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today()-delta(weeks=1))+""", """+str(Date.today())+"""]
            data: [123, 1234567]
            countries:
              ES:
                name: España
                data: [123, 1234567]
            """)

    def test__aggregateLevel_frequency_fromDate_toDate__exist(self):
        self.setupSource(
            headers+'\tcount_2018_02_01'+'\tcount_2018_03_01',
            data_Adra+'\t123\t1234567',
            )
        r = self.get('/members/by/cities/monthly/from/2018-01-01/to/2018-02-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-01-01, 2018-02-01]
            data: [2, 123]
            countries:
              ES:
                name: España
                data: [2, 123]
                ccaas:
                  '01':
                    name: Andalucía
                    data: [2, 123]
                    states:
                      '04':
                        name: Almería
                        data: [2, 123]
                        cities:
                          '04003':
                            name: Adra
                            data: [2, 123]
            """)

    def test__aggregateLevel_frequency_toDate__exist(self):
        self.setupSource(
            headers+'\tcount_2018_02_01'+'\tcount_2018_03_01',
            data_Adra+'\t123\t1234567',
            )
        members_modul.firstDate = '2018-02-01'
        r = self.get('/members/by/cities/monthly/to/2018-03-01')
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: [2018-02-01, 2018-03-01]
            data: [123, 1234567]
            countries:
              ES:
                name: España
                data: [123, 1234567]
                ccaas:
                  '01':
                    name: Andalucía
                    data: [123, 1234567]
                    states:
                      '04':
                        name: Almería
                        data: [123, 1234567]
                        cities:
                          '04003':
                            name: Adra
                            data: [123, 1234567]
            """)


    @unittest.skip("Not implemented yet")
    def test__on_date__missingDate(self): pass



unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
