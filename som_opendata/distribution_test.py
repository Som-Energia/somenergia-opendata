# -*- coding: utf-8 -*-
import unittest
from distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    escollirINES,
    )
from yamlns import namespace as ns
from app import app


class Distribution_Test(unittest.TestCase):
    
    @staticmethod
    def setUpClass():
        #BaseApi_Test.maxDiff=None
        app.config['TESTING']=True

    def setUp(self):
        self.client = app.test_client()

    def get(self, *args, **kwds):
        return self.client.get(*args,**kwds)


    def test__parse_tsv__1col_1row(self):
        fixture = 'item'
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__2col_1row(self):
        fixture = 'item1\titem2'
        self.assertEqual(parse_tsv(fixture), [['item1', 'item2']])


    def test__parse_tsv__1col_2row(self):
        fixture = 'item1\nitem2'
        self.assertEqual(parse_tsv(fixture), [['item1'],['item2']])


    def test__parse_tsv__empty_line_ignored(self):
        fixture = 'item\n'
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__line_with_spaces_ignored(self):
        fixture = 'item\n  '
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__fields_are_stripped(self):
        fixture = '  item  '
        self.assertEqual(parse_tsv(fixture), [['item']])


    def test__parse_tsv__fields_are_really_stripped(self):
        fixture = '  item1  \t item2  '
        self.assertEqual(parse_tsv(fixture), [['item1', 'item2']])


    from testutils import assertNsEqual 

    def assertTupleToObjectEquals(self, csv_input, yaml_output):
        fixture = parse_tsv(csv_input)
        self.assertNsEqual(ns(data=tuples2objects(fixture)), yaml_output)


    def test__tuple2object__1value_1attribute(self):
        self.assertTupleToObjectEquals(
            'name\n'
            'value\n'
            ,
            """\
            data:
            - name: value
            """
            )


    def test__tuple2object__2value_1attribute(self):
        self.assertTupleToObjectEquals(
            'name\n'
            'value1\n'
            'value2\n'
            ,
            """\
            data:
            - name: value1
            - name: value2
            """
            )

    def test__tuple2object__1value_2attribute(self):
        self.assertTupleToObjectEquals(
            'name1\tname2\n'
            'value1\tvalue2\n'
            ,
            """\
            data:
            - name1: value1
              name2: value2
            """
            )


    def test__aggregate__with_1line(self):
        with open('./util_test/1row') as f:
            data = f.read()
        li = tuples2objects(parse_tsv(data))
        #r = escollirINES(li)
        r = aggregate(data)
        self.assertNsEqual(r,"""\
            - code: ES
              name: España
              data 2
              ccaas:
              - code: 01
                name: Andalucia
                data: 2
                states:
                - code: 04
                  name: Almeria
                  data: 2
                  cities:
                  - code: 04003
                    name: Adra
                    data: 2
            """)


    def test__aggregate__same_city(self):
        with open('./util_test/2rowSameCity') as f:
            data = f.read()
        li = tuples2objects(parse_tsv(data))
        r = aggregate(data)
        self.assertNsEqual(r,"""\
            - code: ES
              name: España
              data 3
              ccaas:
              - code: 01
                name: Andalucia
                data: 3
                states:
                - code: 04
                  name: Almeria
                  data: 3
                  cities:
                  - code: 04003
                    name: Adra
                    data: 3
            """)


    def test__aggregate__same_state(self):
        with open('./util_test/2rowSameState') as f:
            data = f.read()
        li = tuples2objects(parse_tsv(data))
        r = aggregate(data)
        self.assertNsEqual(r,"""\
            - code: ES
              name: España
              data 3
              ccaas:
              - code: 01
                name: Andalucia
                data: 3
                states:
                - code: 04
                  name: Almeria
                  data: 3
                  cities:
                  - code: 04003
                    name: Adra
                    data: 2
                  - code: 04006
                    name: Albox
                    data: 1
            """)

    def _test__aggregate__same_state(self):
        with open('./util_test/2rowDifCountry') as f:
            data = f.read()
        r = aggregate(data)
        self.assertEqual(r,"""\
            - code: ES
              name: España
              data 3
              ccaas:
              - code: 01
                name: Andalucia
                data: 3
                states:
                - code: 04
                  name: Almeria
                  data: 3
                  cities:
                  - code: 04003
                    name: Adra
                    data: 2
                  - code: 04006
                    name: Albox
                    data: 1
            """)


    @unittest.skip("És massa complex per fer-ho a la primera, cal partir-ho")
    def test__set_top__city_1date_1city(self):
        response = self.get('/old/members/2015-01-01')
        r = tuples2objects(parse_tsv(response))
        self.assertNsEqual(
            ns(dates=['2015-01-01'],
               level='city',
               data=
                    [ns(codi='17155',
                        name='Salt',
                        data=[176])
                    ]
                ), r)



# vim: et sw=4 ts=4