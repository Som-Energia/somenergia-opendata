import unittest
from flask import current_app
from dbutils import csvTable
import requests


class TestSocis(unittest.TestCase):

    # def setUp(self):
    #     self.client = app.test_client()


    def test_socis_ok(self):
        #res = self.get('htttp://127.0.0.1:5001/socis')
        res = requests.get('http://localhost:5001/socis')

        assert res.status_code == 200


    def test_socis_response(self):
        res = requests.get('http://localhost:5001/socis')

        assert res.content.split()[0] == 'socis:'


    def test_socis_pais_ok(self):
        res  = requests.get('http://localhost:5001/socis/ES')

        assert res.status_code == 200


    def test_socis_pais_response(self):
        res  = requests.get('http://localhost:5001/socis/ES')

        assert res.content.split()[0] == 'socis:'


    def test_socis_pais_ccaa_ok(self):
        res  = requests.get('http://localhost:5001/socis/ES/9')

        assert res.status_code == 200


    def test_socis_pais_ccaa_response(self):
        res  = requests.get('http://localhost:5001/socis/ES/9')

        assert res.content.split()[0] == 'socis:'


    def test_socis_pais_ccaa_prov_ok(self):
        res  = requests.get('http://localhost:5001/socis/ES/9/17')

        assert res.status_code == 200


    def test_socis_pais_ccaa_prov_response(self):
        res  = requests.get('http://localhost:5001/socis/ES/9/17')

        assert res.content.split()[0] == 'socis:'


    def test_socis_pais_ccaa_prov_municipi_ok(self):
        res  = requests.get('http://localhost:5001/socis/ES/9/17/17079')

        assert res.status_code == 200


    def test_socis_pais_ccaa_prov_municipi_response(self):
        res  = requests.get('http://localhost:5001/socis/ES/9/17/17079')

        assert res.content.split()[0] == 'socis:'


unittest.TestCase.__str__ = unittest.TestCase.id


if __name__ == '__main__':
    unittest.main()
