import unittest
from flask import current_app
from dbutils import csvTable



class TestSocis(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()


    def test_socis_ok(self):
        res = self.get('htttp://127.0.0.1:5001/socis')

        assert res.status_code == 400


unittest.TestCase.__str__ = unittest.TestCase.id
