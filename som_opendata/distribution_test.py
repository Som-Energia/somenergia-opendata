# -*- coding: utf-8 -*-
import unittest
from distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    escollirINES,
    state_dates,
    )
from yamlns import namespace as ns
from yamlns.dateutils import Date as isoDate


headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tquants_20180101"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"


class Distribution_Test(unittest.TestCase):
    

    def setUp(self):
        self.maxDiff=None

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
        data = u'\n'.join([
            headers,
            data_Adra,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList)
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            level: countries
            countries:
              ES:
                name: España
                data: 2
                ccaas:
                  '01':
                    name: Andalucía
                    data: 2
                    states:
                      '04':
                        name: Almería
                        data: 2
                        cities:
                          '04003':
                            name: Adra
                            data: 2
            """)


    def _test__aggregate__with_1line_2dates(self):
        data = u'\n'.join([
            headers+'\tquants_20180201',
            data_Adra+'\t3',
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList)
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            level: countries
            countries:
              ES:
                name: España
                data: 2 3
                ccaas:
                  '01':
                    name: Andalucía
                    data: 2 3
                    states:
                      '04':
                        name: Almería
                        data: 2 3
                        cities:
                          '04003':
                            name: Adra
                            data: 2 3
            """)


    def test_state_dates_1date(self):

        data = u'\n'.join([                                                           
            headers,                                                                  
            data_Adra],
        )
        data = tuples2objects(parse_tsv(data))
        r = state_dates(data[0])
        self.assertEqual(
                r,
                [
                    isoDate("20180101"),
                ]
            )




    # def test__aggregate__same_city(self):
    #     with open('./som_opendata/util_test/2rowSameCity') as f:
    #         data = f.read()
    #     li = tuples2objects(parse_tsv(data))
    #     r = aggregate(data)
    #     self.assertNsEqual(r,"""\
    #         - code: ES
    #           name: España
    #           data 3
    #           ccaas:
    #           - code: 01
    #             name: Andalucia
    #             data: 3
    #             states:
    #             - code: 04
    #               name: Almeria
    #               data: 3
    #               cities:
    #               - code: 04003
    #                 name: Adra
    #                 data: 3
    #         """)


    # def test__aggregate__same_state(self):
    #     with open('./som_opendata/util_test/2rowSameState') as f:
    #         data = f.read()
    #     li = tuples2objects(parse_tsv(data))
    #     r = aggregate(data)
    #     self.assertNsEqual(r,"""\
    #         - code: ES
    #           name: España
    #           data 3
    #           ccaas:
    #           - code: 01
    #             name: Andalucia
    #             data: 3
    #             states:
    #             - code: 04
    #               name: Almeria
    #               data: 3
    #               cities:
    #               - code: 04003
    #                 name: Adra
    #                 data: 2
    #               - code: 04006
    #                 name: Albox
    #                 data: 1
    #         """)

    # def _test__aggregate__same_state(self):
    #     with open('./som_opendata/util_test/2rowDifCountry') as f:
    #         data = f.read()
    #     r = aggregate(data)
    #     self.assertEqual(r,"""\
    #         - code: ES
    #           name: España
    #           data 3
    #           ccaas:
    #           - code: 01
    #             name: Andalucia
    #             data: 3
    #             states:
    #             - code: 04
    #               name: Almeria
    #               data: 3
    #               cities:
    #               - code: 04003
    #                 name: Adra
    #                 data: 2
    #               - code: 04006
    #                 name: Albox
    #                 data: 1
    #         """)



# vim: et sw=4 ts=4
