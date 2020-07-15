import unittest
from yamlns import namespace as ns
from .local_groups import LocalGroups, loadYamlLocalGroups

gl_minimal = ns.loads("""\
Alacant:
  name: Alacant
  alias:
    state:
      - '03'
AlmeriaCadiz:
  name: Almería y Cádiz
  alias:
    state:
      - '04'
      - '11'
""")

localGroups = loadYamlLocalGroups('../testData/alias/gl.yaml')
minimalLocalGroups = loadYamlLocalGroups('../testData/alias/minimal_gl.yaml')

class LocalGroups_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test__loadYamlLocalGroups(self):
        expected_localGroups = LocalGroups(gl_minimal)
        self.assertNsEqual(minimalLocalGroups.data, expected_localGroups.data)

    def test__aliasFilters__oneState(self):
        expected = ns(state=('03',))
        self.assertNsEqual(localGroups.aliasFilters('Alacant'), expected)

    def test__aliasFilters__manyStates(self):
        expected = ns(state=['04','11'])
        self.assertEqual(localGroups.aliasFilters('AlmeriaCadiz'), expected)

    def test__aliasFilters__NonExistant(self):

        self.assertEqual(localGroups.aliasFilters('NonExistant'), None)

    def test__aliasFilters__oneCity(self):
        expected = ns(city=['17079'])
        self.assertEqual(localGroups.aliasFilters('GironaCiutat'), expected)

    def test__aliasFilters__manyCities(self):
        expected = ns(city=['17079', '17155'])
        self.assertEqual(localGroups.aliasFilters('GironaSalt'), expected)

    def test__aliasFilters__mixedGeolevels(self):
        expected = ns(ccaa=['09'],city=['28079'])
        self.assertEqual(localGroups.aliasFilters('CatalunyaMadrid'), expected)

    def test__getLocalGroups(self):
        expected = [('Alacant', 'Alacant'), ('AlmeriaCadiz', 'Almería y Cádiz')]
        self.assertEqual(minimalLocalGroups.getLocalGroups(), expected)

    def test__lgComputeValues_oneState(self):
        localGroups = LocalGroups(gl_list_oneState)
        data = ns.loads("""\
          dates: [2019-01-01]
          values: [20]
          countries:
            ES:
              name: España
              values: [20]
              ccaas:
                '01':
                  name: Andalucía
                  values:
                    - 20
                  states:
                    '21':
                      name: Huelva
                      values:
                        - 20
    """)
        expected = ns.loads("""\
        1:
          name: Vitoria-Gasteiz
          values: [20]
        """)

        self.assertNsEqual(localGroups.lgComputeValues([1], data), expected)

    def test__lgComputeValues_manyStates(self):
        localGroups = LocalGroups(gl_list_manyStates)
        data = ns.loads("""\
          dates: [2019-01-01]
          values: [30]
          countries:
            ES:
              name: España
              values: [30]
              ccaas:
                '01':
                  name: Andalucía
                  values:
                    - 30
                  states:
                    '21':
                      name: Huelva
                      values:
                        - 20
                    '22':
                      name: Huelva_2
                      values:
                        - 10
    """)
        expected = ns.loads("""\
        1:
          name: Vitoria-Gasteiz
          values: [30]
        """)

        self.assertNsEqual(localGroups.lgComputeValues([1], data), expected)

    def test__lgComputeValues_oneStateManyDates(self):
        localGroups = LocalGroups(gl_list_oneState)
        data = ns.loads("""\
          dates: [2019-01-01, 2018-01-01]
          values: [20, 30]
          countries:
            ES:
              name: España
              values: [20, 30]
              ccaas:
                '01':
                  name: Andalucía
                  values:
                    - 20
                    - 30
                  states:
                    '21':
                      name: Huelva
                      values:
                        - 20
                        - 30
    """)
        expected = ns.loads("""\
        1:
          name: Vitoria-Gasteiz
          values: [20, 30]
        """)

        self.assertNsEqual(localGroups.lgComputeValues([1], data), expected)

    def test__lgComputeValues_manyCities(self):
        localGroups = LocalGroups(gl_list_manyCities)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 32
        countries:
          ES:
            name: España
            values:
              - 32
            ccaas:
              09:
                name: Cataluña
                values:
                  - 32
                states:
                  '17':
                    name: Girona
                    values:
                      - 32
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 16
                      '170031':
                        name: Aiguaviva
                        values:
                          - 16
        """)
        self.assertNsEqual(
            localGroups.lgComputeValues([1], data),
            ns.loads("""\
              1:
                name: La xocolata de Girona
                values: [32]
    """))

    def test__lgComputeValues_manyLocalGroups(self):
        localGroups = LocalGroups(gl_list_manyLocalGroups)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 32
        countries:
          ES:
            name: España
            values:
              - 32
            ccaas:
              09:
                name: Cataluña
                values:
                  - 32
                states:
                  '17':
                    name: Girona
                    values:
                      - 32
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 16
                      '170031':
                        name: Aiguaviva
                        values:
                          - 16
                      '170046':
                        name: Albons
                        values:
                          - 10
        """)
        self.assertNsEqual(
            localGroups.lgComputeValues([1, 2], data),
            ns.loads("""\
              1:
                name: La xocolata de Girona
                values: [32]
              2:
                name: Grup Local d'Albons
                values: [10]
    """))

    def test__lgComputeValues_manyLocalGroupsDifferentGeolevels(self):
        localGroups = LocalGroups(gl_list_manyLocalGroups)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 32
        countries:
          ES:
            name: España
            values:
              - 32
            ccaas:
              09:
                name: Cataluña
                values:
                  - 32
                states:
                  '17':
                    name: Girona
                    values:
                      - 32
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 16
                      '170031':
                        name: Aiguaviva
                        values:
                          - 16
                      '170046':
                        name: Albons
                        values:
                          - 10
                  '21':
                    name: Girona
                    values:
                      - 500
                    cities:
                      '21001':
                        name: Ciutat 1, The Best Ciutat
                        values:
                          - 499
                      '21002':
                        name: Ciutat 2, The Worst Ciutat
                        values:
                          - 1
        """)
        self.assertNsEqual(
            localGroups.lgComputeValues([1, 3], data),
            ns.loads("""\
              1:
                name: La xocolata de Girona
                values: [32]
              3:
                name: Vitoria-Gasteiz
                values: [500]
    """))

    def test_lgHierarchicalResponse_dataIntegrityTest(self):
        localGroups = LocalGroups(gl_list_oneCity)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 32
        countries:
          ES:
            name: España
            values:
              - 32
            ccaas:
              '09':
                name: Cataluña
                values:
                  - 32
                states:
                  '17':
                    name: Girona
                    values:
                      - 32
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 16
        """)
        expected = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 32
        countries:
          ES:
            name: España
            values:
              - 32
            ccaas:
              '09':
                name: Cataluña
                values:
                  - 32
                states:
                  '17':
                    name: Girona
                    values:
                      - 32
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 16
        """)
        lg = ns.loads("""\
              '1':
                name: La xocolata de Girona
                values: [32]
        """)

        localGroups.lgHierarchicalResponse(lgs=[lg], hierarchicalData=data)
        self.assertNsEqual(data, expected)

    #TODO deprecate this for a better response
    def test_lgHierarchicalResponse(self):
        self.maxDiff = None
        localGroups = LocalGroups(gl_list_oneCity)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 20
        countries:
          ES:
            name: España
            values:
              - 20
            ccaas:
              09:
                name: Cataluña
                values:
                  - 20
                states:
                  '17':
                    name: Girona
                    values:
                      - 20
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 20
        """)

        lgs = ns.loads("""\
              '1':
                name: La xocolata de Girona
                values: [20]
        """)

        expected = ns.loads("""\
              '1':
                name: La xocolata de Girona
                values: [20]
        """)

        result = localGroups.lgHierarchicalResponse(lgs=lgs, hierarchicalData=data)
        self.assertNsEqual(result, expected)

    #TODO lgHierarchicalResponse definition awaiting a proper definition to
    # set its tests accordingly
    def _test_lgHierarchicalResponse_cities(self):
        self.maxDiff = None
        localGroups = LocalGroups(gl_list_oneCity)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 20
        countries:
          ES:
            name: España
            values:
              - 20
            ccaas:
              09:
                name: Cataluña
                values:
                  - 20
                states:
                  '17':
                    name: Girona
                    values:
                      - 20
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 20
        """)

        lgs = ns.loads("""\
              '1':
                name: La xocolata de Girona
                values: [20]
        """)

        expected = ns.loads("""\
          dates: [2020-05-01]
          values: [20]
          countries:
            ES:
              name: España
              values: [20]
              ccaas:
                09:
                  name: Cataluña
                  values:
                    - 20
                  localgroups:
                    '1':
                      name: La xocolata de Girona
                      values:
                        - 20
        """)

        result = localGroups.lgHierarchicalResponse(lgs=lgs, hierarchicalData=data)
        self.assertNsEqual(result, expected)

    def _test_lgHierarchicalResponse_cities(self):
        self.maxDiff = None
        localGroups = LocalGroups(gl_list_oneCity)
        data = ns.loads("""\
        dates: [2020-05-01]
        values:
          - 20
        countries:
          ES:
            name: España
            values:
              - 20
            ccaas:
              09:
                name: Cataluña
                values:
                  - 20
                states:
                  '17':
                    name: Girona
                    values:
                      - 20
                    cities:
                      '170010':
                        name: Agullana
                        values:
                          - 20
        """)

        lgs = ns.loads("""\
              '1':
                name: La xocolata de Girona
                values: [20]
        """)

        expected = ns.loads("""\
          dates: [2020-05-01]
          values: [20]
          countries:
            ES:
              name: España
              values: [20]
              ccaas:
                09:
                  name: Cataluña
                  values:
                    - 20
                  localgroups:
                    '1':
                      name: La xocolata de Girona
                      values:
                        - 20
        """)

        result = localGroups.lgHierarchicalResponse(lgs=lgs, hierarchicalData=data)
        self.assertNsEqual(result, expected)

    def _test__aggregateAlias_(self):
        localGroups = LocalGroups(gl_list_oneState)
        data = ns.loads("""\
          dates: [2019-01-01]
          values: [20]
          countries:
            ES:
              name: España
              values: [20]
              ccaas:
                '01':
                  name: Andalucía
                  values:
                    - 20
                  states:
                    '21':
                      name: Huelva
                      values:
                        - 20
    """)
        expected = ns.loads("""\
          dates: [2019-01-01]
          values: [20]
          countries:
            ES:
              name: España
              values: [20]
              ccaas:
                '01':
                  name: Andalucía
                  values:
                    - 20
                  localgroups:
                    '1':
                      name: Vitoria-Gasteiz
                      values:
                        - 20
    """)
        result = localGroups.aggregateAlias([1], data)
        self.assertNsEqual(result, expected)

    def _test__aggregateAlias_manyStates(self):
        manyStates = ns.loads("""\
            dates: [2019-01-01]
            values: [750]
            countries:
            ES:
                name: España
                values: [750]
                ccaas:
                '01':
                    name: Andalucia
                    values:
                    - 750
                    states:
                    '11':
                        name: Cádiz
                        values:
                        - 500
                    '14':
                        name: Córdoba
                        values:
                        - 250
            """)

        expected = ns.loads("""\
            dates: [2019-01-01]
            values: [750]
            countries:
            ES:
                name: España
                values: [750]
                ccaas:
                '01':
                    name: Andalucia
                    values:
                    - 750
                    localgroups:
                      '2':
                        name: Segon
                        values:
                        - 750
            """)
