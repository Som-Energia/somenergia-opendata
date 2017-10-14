# -*- encoding: utf-8 -*-

import unittest
from yamlns import namespace as ns
from som_opendata.api import app

class BaseApi_Test(unittest.TestCase):

    @staticmethod
    def setUpClass():
        BaseApi_Test.maxDiff=None
        app.config['TESTING']=True

    def setUp(self):
        self.client = app.test_client()

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    def assertYamlResponse(self, response, expected):
        self.assertMultiLineEqual(
            ns.loads(response.data).dump(),
            ns.loads(expected).dump(),
        )

    def test_version(self):
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '1.0'
            """)



unittest.TestCase.__str__ = unittest.TestCase.id



# vim: et ts=4 sw=4
