import unittest
from flask import current_app
from dbutils import csvTable
import requests
from ..app import app
from yamlns import namespace as ns



class TestSocis(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)

    def test_socis_ok(self):
        res = self.get('htttp://127.0.0.1:5001/socis')
        #res = requests.get('http://localhost:5001/socis')

        assert res.status_code == 200

    from ..testutils import assertNsEqual

    def test_socis_response(self):
        res = self.get('http://localhost:5001/socis')
        assert res.data == ns(socis=88588).dump()


    def test_socis_pais_ok(self):
        res  = self.get('http://localhost:5001/socis/ES')

        assert res.status_code == 200


    def test_socis_pais_response(self):
        res  = self.get('http://localhost:5001/socis/ES')

        assert res.data == ns(socis=87481).dump()


    def test_socis_pais_ccaa_ok(self):
        res  = self.get('http://localhost:5001/socis/ES/9')

        assert res.status_code == 200


    def test_socis_pais_ccaa_response(self):
        res  = self.get('http://localhost:5001/socis/ES/9')

        assert res.data == ns(socis=55454).dump()


    def test_socis_pais_ccaa_prov_ok(self):
        res  = self.get('http://localhost:5001/socis/ES/9/17')

        assert res.status_code == 200


    def test_socis_pais_ccaa_prov_response(self):
        res  = self.get('http://localhost:5001/socis/ES/9/17')

        assert res.data == ns(socis=6735).dump()


    def test_socis_pais_ccaa_prov_municipi_ok(self):
        res  = self.get('http://localhost:5001/socis/ES/9/17/17079')

        assert res.status_code == 200


    def test_socis_pais_ccaa_prov_municipi_response(self):
        res  = self.get('http://localhost:5001/socis/ES/9/17/17079')

        assert res.data == ns(socis=1821).dump()


unittest.TestCase.__str__ = unittest.TestCase.id


if __name__ == '__main__':
    unittest.main()
