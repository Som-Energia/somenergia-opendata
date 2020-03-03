# -*- encoding: utf-8 -*-
import unittest
from yamlns import namespace as ns
import b2btest
from flask import Flask
from .oldapi import blueprint
from .common import register_converters

app = None

@unittest.skipIf("TRAVIS" in os.environ, "requires acces to db")
class BaseApi_Test(unittest.TestCase):

    @staticmethod
    def setUpClass():
        #BaseApi_Test.maxDiff=None
        global app
        app = Flask(__name__)
        register_converters(app)
        app.register_blueprint(blueprint, url_prefix='')
        app.config['TESTING']=True

    def setUp(self):
        self.client = app.test_client()
        self.b2bdatapath = 'b2bdata'

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    from somutils.testutils import assertNsEqual

    def assertYamlResponse(self, response, expected):
        self.assertNsEqual(response.data, expected)

    def assertTsvResponse(self, response):
        self.assertB2BEqual(response.data)

    def test_version(self):
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '0.1.0'
            compat: '0.1.0'
            """)

    def test_contracts_single(self):
        r = self.get('/contracts/2015-01-01')
        self.assertTsvResponse(r)

    def test_contracts_series(self):
        r = self.get('/contracts/2015-01-01/monthlyto/2015-04-01')
        self.assertTsvResponse(r)

    def test_members_single(self):
        r = self.get('/members/2015-01-01')
        self.assertTsvResponse(r)

    def test_members_series(self):
        r = self.get('/members/2015-01-01/monthlyto/2015-04-01')
        self.assertTsvResponse(r)

    def text_membersAux_series(self):
        r = self.get('/members/2015-01-01/weeklyandmonthlyto/2015-03-01')
        self.assertTsvResponse(r)

    def text_contractssAux_series(self):
        r = self.get('/contracts/2015-01-01/weeklyandmonthlyto/2015-03-01')
        self.assertTsvResponse(r)


# vim: et ts=4 sw=4
