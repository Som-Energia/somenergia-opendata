# -*- coding: utf-8 -*-
import io
import unittest
from yamlns.dateutils import Date as isoDate
from yamlns import namespace as ns
import b2btest
from .distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    headerDates,
    locationFilter,
    validateStringDate,
    includedDates,
    field2date,
    date2field,
    isField,
    missingDates,
    includedDatesObject,
    findObject,
    addObjects,
    getAggregated,
    distributionKey,
    aggregated2table,
    )
from .csvSource import loadCsvSource
from functools import lru_cache
from .timeaggregator import TimeAggregator, TimeAggregatorSum

headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"


skipSlow = False

class Distribution_Test(unittest.TestCase):
    

    def setUp(self):
        self.maxDiff=None
        self.b2bdatapath = 'b2bdata'
        self.singleDate = TimeAggregator(on='2018-01-01')
        self.manyDates = TimeAggregator(periodicity='monthly', since='2018-01-01', to='2018-02-01')

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


    from somutils.testutils import assertNsEqual

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

    def test__aggregated2table_global_singleDate(self):
        data=ns.loads("""\
            dates: 
            - 2018-01-01
            values: [2]
        """)

        self.assertEqual(
            list(aggregated2table(data)),
            [
                [isoDate('2018-01-01')],
                [2],
            ])

    def test__aggregated2table_countries_oneCountry(self):
        data=ns.loads("""\
            dates: 
            - 2018-01-01
            values: [2]
            countries:
              ES: 
                 name: España
                 values: [2]
        """)

        self.assertEqual(
            list(aggregated2table(data)),
            [
                ['country_code', 'country', isoDate('2018-01-01')],
                ['ES', 'España', 2],
            ])

    def test__aggregated2table_countries_manyCountries(self):
        data=ns.loads("""\
            dates: 
            - 2018-01-01
            values: [7]
            countries:
              ES: 
                 name: España
                 values: [2]
              FR: 
                 name: Francia
                 values: [5]
        """)

        self.assertEqual(
            list(aggregated2table(data)),
            [
                ['country_code', 'country', isoDate('2018-01-01')],
                ['ES', 'España', 2],
                ['FR', 'Francia', 5],
            ])


    def test__aggregate__1line(self):
        data = u'\n'.join([
            headers,
            data_Adra,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [2]
            countries:
              ES:
                name: España
                values: [2]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [2]
                    states:
                      '04':
                        name: Almería
                        values: [2]
                        cities:
                          '04003':
                            name: Adra
                            values: [2]
            """)


    def test__aggregate__1line_2dates(self):
        data = u'\n'.join([
            headers+'\tcount_2018_02_01',
            data_Adra+'\t3',
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            - 2018-02-01
            values: [2, 3]
            countries:
              ES:
                name: España
                values: [2, 3]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [2, 3]
                    states:
                      '04':
                        name: Almería
                        values: [2, 3]
                        cities:
                          '04003':
                            name: Adra
                            values: [2, 3]
            """)


    def test__aggregate__2lines_differentCountry(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [12]
            countries:
              ES:
                name: España
                values: [2]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [2]
                    states:
                      '04':
                        name: Almería
                        values: [2]
                        cities:
                          '04003':
                            name: Adra
                            values: [2]
              FR:
                name: France
                values: [10]
                ccaas:
                  '76':
                    name: Occità
                    values: [10]
                    states:
                      '66':
                        name: Pyrénées-Orientales
                        values: [10]
                        cities:
                          '66136':
                            name: Perpignan
                            values: [10]
            """)


    def test__aggregate__2lines_differentCcaa(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Girona,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [22]
            countries:
              ES:
                name: España
                values: [22]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [2]
                    states:
                      '04':
                        name: Almería
                        values: [2]
                        cities:
                          '04003':
                            name: Adra
                            values: [2]
                  '09':
                    name: Catalunya
                    values: [20]
                    states:
                      '17':
                        name: Girona
                        values: [20]
                        cities:
                          '17079':
                            name: Girona
                            values: [20]
            """)


    def test__aggregate__2lines_differentState(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_SantJoan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [1020]
            countries:
              ES:
                name: España
                values: [1020]
                ccaas:
                  '09':
                    name: Catalunya
                    values: [1020]
                    states:
                      '17':
                        name: Girona
                        values: [20]
                        cities:
                          '17079':
                            name: Girona
                            values: [20]
                      '08':
                        name: Barcelona
                        values: [1000]
                        cities:
                          '08217':
                            name: Sant Joan Despí
                            values: [1000]
            """)

    def test__aggregate__2lines_differentCities(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_Amer,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [2020]
            countries:
              ES:
                name: España
                values: [2020]
                ccaas:
                  '09':
                    name: Catalunya
                    values: [2020]
                    states:
                      '17':
                        name: Girona
                        values: [2020]
                        cities:
                          '17079':
                            name: Girona
                            values: [20]
                          '17007':
                            name: Amer
                            values: [2000]
            """)


    def test__aggregate__1line_dates(self):
        data = u'\n'.join([
            headers+'\tcount_2018_02_01',
            data_Adra+'\t3',
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city', timeDomain=self.singleDate)
        self.assertNsEqual(r,"""\
            dates:
            - 2018-01-01
            values: [2]
            countries:
              ES:
                name: España
                values: [2]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [2]
                    states:
                      '04':
                        name: Almería
                        values: [2]
                        cities:
                          '04003':
                            name: Adra
                            values: [2]
            """)


    def test_headerDates_severalDates(self):
        data = u'\n'.join([
            headers+'\tcount_2018_02_01',
            data_Adra+'\t3',
        ])
        data = tuples2objects(parse_tsv(data))
        r = headerDates(data[0])
        self.assertEqual(r, [
            "2018-01-01",
            "2018-02-01",
        ])

    def test__aggregate__1line_timeAggregationSum(self):
        data = u'\n'.join([
            headers+
                '\tcount_2018_02_01'
                '\tcount_2018_03_01'
                '\tcount_2018_04_01'
                '\tcount_2018_05_01'
                '\tcount_2018_06_01'
                '\tcount_2018_07_01'
                '\tcount_2018_08_01'
                '\tcount_2018_09_01'
                '\tcount_2018_10_01'
                '\tcount_2018_11_01'
                '\tcount_2018_12_01'
                '\tcount_2019_01_01'
                ,
            data_Adra+
                '\t1'
                '\t2'
                '\t3'
                '\t4'
                '\t5'
                '\t6'
                '\t7'
                '\t8'
                '\t9'
                '\t10'
                '\t11'
                '\t12'
                ,
        ])
        timeDomain = TimeAggregatorSum(
            since = '2019-01-01',
            to = '2019-03-01',
            periodicity = 'yearly',
        )
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city', timeDomain=timeDomain)
        self.assertNsEqual(r,"""\
            dates:
            - 2019-01-01
            values: [78]
            countries:
              ES:
                name: España
                values: [78]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [78]
                    states:
                      '04':
                        name: Almería
                        values: [78]
                        cities:
                          '04003':
                            name: Adra
                            values: [78]
            """)



    @unittest.skipIf(skipSlow, 'test lent')
    def test__aggregate__backToBack(self):
        with io.open('./b2bdata/som_opendata.contractSeries_many-input.tsv') as f:
            data = f.read()

        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList, 'city')
        self.assertB2BEqual(r.dump())


    @unittest.skip("TODO")  # Tant facil com if objectList == [] no crida aggregate i mostra un missatge explicatiu
    def test__aggregate__withNoRows(self):
        data = u'\n'.join([
            headers,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList)
        self.assertNsEqual(r,"")


    def test__filter__noFilter(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns())
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '01'
              comunitat_autonoma: Andalucía
              codi_provincia: '04'
              provincia: Almería
              codi_ine: '04003'
              municipi: Adra
              count_2018_01_01: '2'

            - codi_pais: FR
              pais: France
              codi_ccaa: '76'
              comunitat_autonoma: Occità
              codi_provincia: '66'
              provincia: Pyrénées-Orientales
              codi_ine: '66136'
              municipi: Perpignan
              count_2018_01_01: '10'
        """)



    def test__filter__1country(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns(codi_pais=['ES']))
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '01'
              comunitat_autonoma: Andalucía
              codi_provincia: '04'
              provincia: Almería
              codi_ine: '04003'
              municipi: Adra
              count_2018_01_01: '2'
        """)


    def test__filter__France(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns(codi_pais=['FR']))
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: FR
              pais: France
              codi_ccaa: '76'
              comunitat_autonoma: Occità
              codi_provincia: '66'
              provincia: Pyrénées-Orientales
              codi_ine: '66136'
              municipi: Perpignan
              count_2018_01_01: '10'
        """)


    def test__filter__1state(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns(codi_ccaa=['01']))
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '01'
              comunitat_autonoma: Andalucía
              codi_provincia: '04'
              provincia: Almería
              codi_ine: '04003'
              municipi: Adra
              count_2018_01_01: '2'
        """)


    def test__filter__2countries(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns(codi_pais=['ES','FR']))
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '01'
              comunitat_autonoma: Andalucía
              codi_provincia: '04'
              provincia: Almería
              codi_ine: '04003'
              municipi: Adra
              count_2018_01_01: '2'

            - codi_pais: FR
              pais: France
              codi_ccaa: '76'
              comunitat_autonoma: Occità
              codi_provincia: '66'
              provincia: Pyrénées-Orientales
              codi_ine: '66136'
              municipi: Perpignan
              count_2018_01_01: '10'
        """)

    def test__filter__differentLevels(self):
        data = u'\n'.join([
            headers,
            data_Adra,
            data_Perignan,
        ])
        objectList = tuples2objects(parse_tsv(data))
        result = locationFilter(objectList,ns(
            codi_pais=['FR'],
            codi_ccaa=['01']),
        )
        self.assertNsEqual(ns(data=result), """\
            data:
            - codi_pais: ES
              pais: 'España'
              codi_ccaa: '01'
              comunitat_autonoma: Andalucía
              codi_provincia: '04'
              provincia: Almería
              codi_ine: '04003'
              municipi: Adra
              count_2018_01_01: '2'

            - codi_pais: FR
              pais: France
              codi_ccaa: '76'
              comunitat_autonoma: Occità
              codi_provincia: '66'
              provincia: Pyrénées-Orientales
              codi_ine: '66136'
              municipi: Perpignan
              count_2018_01_01: '10'
        """)

    @unittest.skipIf(skipSlow, 'test lent')
    def test__filter_aggregate__backToBack(self):
        with io.open('./b2bdata/som_opendata.contractSeries_many-input.tsv') as f:
            data = f.read()

        objectList = tuples2objects(parse_tsv(data))
        objectList = locationFilter(objectList,
                ns(codi_pais=['ES'],codi_ccaa=['01','09'])
            )
        r = aggregate(objectList, 'city')
        self.assertB2BEqual(r.dump())


    def test__aggregate__detailCountry_2lines_differentCities(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_Amer,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList,'country')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [2020]
            countries:
              ES:
                name: España
                values: [2020]
            """)

    def test__aggregate__detailState_2lines_differentCities(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_Amer,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList,'state')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [2020]
            countries:
              ES:
                name: España
                values: [2020]
                ccaas:
                  '09':
                    name: Catalunya
                    values: [2020]
                    states:
                      '17':
                        name: Girona
                        values: [2020]
            """)

    def test__aggregate__detailWorld_2lines_differentCities(self):
        data = u'\n'.join([
            headers,
            data_Girona,
            data_Amer,
        ])
        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList,'world')
        self.assertNsEqual(r,"""\
            dates: 
            - 2018-01-01
            values: [2020]
            """)

    @unittest.skipIf(skipSlow, 'test lent')
    def test__filter_aggregate__withDetail_backToBack(self):
        with io.open('./b2bdata/som_opendata.contractSeries_many-input.tsv') as f:
            data = f.read()

        objectList = tuples2objects(parse_tsv(data))
        r = aggregate(objectList,'ccaa')
        self.assertB2BEqual(r.dump())
        

    # validateStringDate

    def test__validateStringDate__existDate(self):
        result = validateStringDate('2018-01-01')
        self.assertEqual(result, True)

    def test__validateStringDate__noExistDate(self):
        result = validateStringDate('2018-21-01')
        self.assertEqual(result, False)


    # includedDates

    def test__includedDates__empty(self):
        result = includedDates([])
        self.assertEqual(result, [])

    def test__includedDates__emptyHeaders(self):
        result = includedDates([[],[]])
        self.assertEqual(result, [])

    def test__includedDates__correctDates(self):
        result = includedDates([['blah', 'blah', 'count_2018_01_01']])
        self.assertEqual(result, ['2018-01-01'])

    def test__includedDates__incorrectDates(self):
        result = includedDates([['blah', 'count_2018_20_54', 'count_2018_01_01']])
        self.assertEqual(result, ['2018-01-01'])


    # includedDatesObjects

    def test__includedDatesObject__empty(self):
        result = includedDatesObject([])
        self.assertEqual(result, [])

    def test__includedDatesObject__emptyHeaders(self):
        result = includedDatesObject([ns(),ns()])
        self.assertEqual(result, [])

    def test__includedDatesObject__correctDates(self):
        result = includedDatesObject([ns(codi_pais='ES', count_2018_01_01='1000')])
        self.assertEqual(result, ['2018-01-01'])

    def test__includedDatesObject__incorrectDates(self):
        result = includedDatesObject([ns(codi_pais='ES', count_2018_41_01='1000', count_2018_01_01='1000')])
        self.assertEqual(result, ['2018-01-01'])


    # field2date

    def test__field2date__correctDate(self):
        result = field2date('count_2018_01_01')
        self.assertEqual(result, '2018-01-01')


    # date2field

    def test__date2field__correctDate(self):
        result = date2field('2018-01-01')
        self.assertEqual(result, 'count_2018_01_01')


    # isField

    def test__isField__correctField(self):
        result = isField('count_2018_01_01')
        self.assertEqual(result, True)

    def test__isField__incorrectField(self):
        result = isField('codi_pais')
        self.assertEqual(result, False)


    # missingDates

    def test__missingDates__existAllDates(self):
        result = missingDates(['2018-01-01'], ['2018-01-01'])
        self.assertEqual(result, [])

    def test__missingDates__moreRequestThatExist(self):
        result = missingDates(['2018-01-01'], ['2018-01-01', '2018-02-01'])
        self.assertEqual(result, ['2018-02-01'])

    def test__missingDates__moreExistThatRequest(self):
        result = missingDates(['2018-01-01','2018-02-01'], ['2018-01-01'])
        self.assertEqual(result, [])


    # findObject

    def test__findObject__NotFound(self):
        objectList = [
            ns(key1='value1', key2='value2'),
            ns(key1='value3', key2='value4')
        ]
        result = findObject(objectList, 'key1', 'value5')
        self.assertEqual(result, None)

    def test__findObject__existObject(self):
        objectList = [
            ns(key1='value1', key2='value2'),
            ns(key1='value3', key2='value4')
        ]
        result = findObject(objectList, 'key1', 'value3')
        self.assertEqual(result, ns(key1='value3', key2='value4'))


    # addObjects

    def test__addObjects__Equals(self):
        data = [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'17',
                    provincia=u'Girona',
                    codi_ine=u'17007',
                    municipi=u'Amer',
                    count_2018_02_01=u'2001',
                )
            ]
        addObjects(data, data)
        self.assertEqual(data, [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'17',
                    provincia=u'Girona',
                    codi_ine=u'17007',
                    municipi=u'Amer',
                    count_2018_02_01=u'2001',
                )
            ])

    def test__addObjects__sameCounts(self):
        data = [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
            ]
        content = [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'17',
                    provincia=u'Girona',
                    codi_ine=u'17007',
                    municipi=u'Amer',
                    count_2018_02_01=u'100',
                ),
            ]
        addObjects(data, content)
        self.assertEqual(data, [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'17',
                    provincia=u'Girona',
                    codi_ine=u'17007',
                    municipi=u'Amer',
                    count_2018_02_01=u'100',
                ),
            ])

    def test__addObjects__diferentCounts(self):
        data = [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_02_01=u'201',
                ),
            ]
        content = [
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'08',
                    provincia=u'Barcelona',
                    codi_ine=u'08217',
                    municipi=u'Sant Joan Despí',
                    count_2018_03_01=u'2010',
                ),
                ns(
                    codi_pais=u'ES',
                    pais=u'España',
                    codi_ccaa=u'09',
                    comunitat_autonoma=u'Catalunya',
                    codi_provincia=u'17',
                    provincia=u'Girona',
                    codi_ine=u'17007',
                    municipi=u'Amer',
                    count_2018_03_01=u'1000',
                ),
            ]
        addObjects(data, content)
        self.assertNsEqual(ns(data=data), """\
            data:
            - municipi: Sant Joan Despí
              codi_ccaa: '09'
              provincia: Barcelona
              codi_pais: ES
              codi_ine: '08217'
              comunitat_autonoma: Catalunya
              codi_provincia: '08'
              pais: 'España'
              count_2018_02_01: '201'
              count_2018_03_01: '2010'
            - municipi: Amer
              count_2018_03_01: '1000'
              provincia: Girona
              codi_pais: ES
              codi_ine: '17007'
              comunitat_autonoma: Catalunya
              codi_ccaa: '09'
              codi_provincia: '17'
              pais: 'España'
              count_2018_02_01: '0'
        """)

    def test__getAggregated_cached(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [1,1])

    def test__getAggregated_notCachedMetric(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        getAggregated(source, 'contracts', self.singleDate, {}, 'ccaa', mutable=False)
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [0,2])

    def test__getAggregated_notCachedGeolevel(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        getAggregated(source, 'members', self.singleDate, {}, 'state', mutable=False)
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [0,2])

    def test__getAggregated_notCachedDates(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        getAggregated(source, 'members', self.manyDates, {}, 'ccaa', mutable=False)
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [0,2])

    def test__getAggregated_updatingSource(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)

        #source.update clears cache
        source.update('members',
            [ns(codi_pais=u'NC',
                pais=u'New Country',
                codi_ccaa=u'09',
                comunitat_autonoma=u'Catalunya',
                codi_provincia=u'08',
                provincia=u'Barcelona',
                codi_ine=u'08217',
                municipi=u'Sant Joan Despí',
                count_2018_02_01=u'201')]
        )
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [0,0])
        getAggregated(source, 'members', self.singleDate, {}, 'ccaa', mutable=False)
        self.assertEqual([getAggregated.cache_hits, getAggregated.cache_misses], [0,1])

    def test_getAggregated_cachedAfterChangedValues(self):
        getAggregated.cache_clear()
        source = loadCsvSource(relativePath='../testData/metrics')
        resultBefore = getAggregated(source, 'members', self.singleDate, {}, 'state', mutable=True)
        resultBefore['dates']=10
        resultAfter = getAggregated(source, 'members', self.singleDate, {}, 'state', mutable=True)
        self.assertNotEqual(resultBefore['dates'], resultAfter['dates'])

    def assertKeyEqual(self, result, expected):
        self.assertEqual(result, expected)
        self.assertEqual(hash(result), hash(expected))

    def test_distributionKey(self):
        source = loadCsvSource(relativePath='../testData/metrics')
        result = distributionKey(
            source=source,
            metric='members',
            timeDomain = self.singleDate,
            location_filter={'city': ['08232']},
            geolevel='state',
        )
        self.assertKeyEqual(result, (
            source,
            'members',
            tuple(self.singleDate.requestDates),
            (
                ('city',tuple(['08232'])),
            ),
            'state',
        ))

    def test_distributionKey_multipleFilterKeys_ordered(self):
        source = loadCsvSource(relativePath='../testData/metrics')
        result = distributionKey(
            source=source,
            metric='members',
            timeDomain = self.singleDate,
            location_filter=ns([
                ('city', ['08232']),
                ('ccaa', ['02']),
            ]),
            geolevel='state',
        )
        self.assertKeyEqual(result, (
            source,
            'members',
            tuple(self.singleDate.requestDates),
            (
                ('ccaa',tuple(['02'])),
                ('city',tuple(['08232'])),
            ),
            'state',
        ))

    def test_distributionKey_multipleFilterValues_ordered(self):
        source = loadCsvSource(relativePath='../testData/metrics')
        result = distributionKey(
            source=source,
            metric='members',
            timeDomain = self.singleDate,
            location_filter=ns([
                ('city', ['08232','02324']),
            ]),
            geolevel='state',
        )
        self.assertKeyEqual(result, (
            source,
            'members',
            tuple(self.singleDate.requestDates),
            (
                ('city',tuple(['02324','08232'])),
            ),
            'state',
        ))


# vim: et sw=4 ts=4
