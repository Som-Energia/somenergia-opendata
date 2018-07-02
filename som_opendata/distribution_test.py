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
import io
import b2btest

headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t09090\tSantJoan\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"


class Distribution_Test(unittest.TestCase):
    

    def setUp(self):
        self.maxDiff=None
        self.b2bdatapath = 'b2bdata'

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


    def test__aggregate__with_1line_2dates(self):
        data = u'\n'.join([
            headers+'\tcount_2018_02_01',
            data_Adra+'\t3',
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList)
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            - 2018-02-01
            level: countries
            countries:
              ES:
                name: España
                data: [2, 3]
                ccaas:
                  '01':
                    name: Andalucía
                    data: [2, 3]
                    states:
                      '04':
                        name: Almería
                        data: [2, 3]
                        cities:
                          '04003':
                            name: Adra
                            data: [2, 3]
            """)


    def test__aggregate__with_2line(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
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
              FR:
                name: France
                data: [10]
                ccaas:
                  '76':
                    name: Occità
                    data: [10]
                    states:
                      '66':
                        name: Pyrénées-Orientales
                        data: [10]
                        cities:
                          '66136':
                            name: Perpignan
                            data: [10]
            """)


    def test__aggregate__with_2line_sameCountry(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Girona,
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
                data: [22]
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
                  '09':
                    name: Catalunya
                    data: [20]
                    states:
                      '17':
                        name: Girona
                        data: [20]
                        cities:
                          '17079':
                            name: Girona
                            data: [20]
            """)


    def test__aggregate__with_2line_sameCCAA(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_SantJoan,
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
                data: [1020]
                ccaas:
                  '09':
                    name: Catalunya
                    data: [1020]
                    states:
                      '17':
                        name: Girona
                        data: [20]
                        cities:
                          '17079':
                            name: Girona
                            data: [20]
                      '08':
                        name: Barcelona
                        data: [1000]
                        cities:
                          '09090':
                            name: SantJoan
                            data: [1000]
            """)


    def test__aggregate__with_2line_sameState(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_Amer,
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
                data: [2020]
                ccaas:
                  '09':
                    name: Catalunya
                    data: [2020]
                    states:
                      '17':
                        name: Girona
                        data: [2020]
                        cities:
                          '17079':
                            name: Girona
                            data: [20]
                          '17007':
                            name: Amer
                            data: [2000]
            """)




    def test_state_dates_1date(self):

        data = u'\n'.join([
            headers+'\tcount_2018_02_01',
            data_Adra+'\t3',
        ])
        data = tuples2objects(parse_tsv(data))
        r = state_dates(data[0])
        self.assertEqual(
                r,
                [
                    isoDate("20180101"),
                    isoDate("20180201"),
                ]
            )


    def test__aggregate__backToBack(self):
        with io.open('./b2bdata/som_opendata.api_test.BaseApi_Test.test_contractsSeries_many-expected') as f:
            data = f.read()

        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList)
        self.assertB2BEqual(r.dump())






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
