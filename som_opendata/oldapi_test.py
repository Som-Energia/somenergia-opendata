# -*- encoding: utf-8 -*-
import unittest
from yamlns import namespace as ns
import b2btest
from flask import Flask
from .api import (
    blueprint,
    )
from .common import (
    register_converters,
    )

app = Flask(__name__)
register_converters(app)
app.register_blueprint(blueprint, url_prefix='')

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

    def test_version(self):
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '1.0'
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


"""
/version
/members/2015-02
/members/2015-02/weeklyuntil/2015-12
/members/2015-02/monthlyuntil/2015-12
/map/members/...
"""



# vim: et ts=4 sw=4
