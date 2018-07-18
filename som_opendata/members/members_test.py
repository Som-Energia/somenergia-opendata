# -*- encoding: utf-8 -*-

import unittest
import b2btest
from ..app import app
from members import members_modul

headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"


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

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    from ..testutils import assertNsEqual

    def assertYamlResponse(self, response, expected):
        self.assertNsEqual(response.data, expected)

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    def test_version(self):
        self.setupSource(
            headers,
            data_SantJoan,
            )
        r = self.get('/members/on/2018-01-01')
        self.assertYamlResponse(r, """\
            data: 
                - 1000
            dates:
                - 2018-01-01
            """)


unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
