import unittest
from yamlns import namespace as ns
from .local_groups import LocalGroups, loadYamlLocalGroups

gl_list_oneState = ns.loads("""\
1:
    name: Vitoria-Gasteiz
    geolevel: state
    codes: ['21']
""")
gl_list_manyStates = ns.loads("""\
1:
    name: Vitoria-Gasteiz
    geolevel: state
    codes: ['21', '22']
""")

gl_list_manyCities = ns.loads("""\
1:
    name: La xocolata de Girona
    geolevel: city
    codes: ['170010', '170031']
""")

gl_list_oneCity = ns.loads("""\
1:
    name: Pardals de Cabanelles
    geolevel: city
    codes: ['170031']
""")

gl_list_oneCCAA = ns.loads("""\
1:
    name: Asturias
    geolevel: ccaa
    codes: ['33']
""")

gl_list_manyCCAA = ns.loads("""\
1:
    name: Provincies agermanades Girona-Asturias
    geolevel: ccaa
    codes: ['17', '33']
""")

gl_list_getLocalGroups = ns.loads("""\
1:
    name: La xocolata de Girona
    geolevel: city
    codes: ['170010', '170031']
""")

gl_list_manyLocalGroups= ns.loads("""\
1:
    name: La xocolata de Girona
    geolevel: city
    codes: ['170010', '170031']
2:
    name: Grup Local d'Albons
    geolevel: city
    codes: ['170046']
3:
    name: Vitoria-Gasteiz
    geolevel: state
    codes: ['21']
""")

class LocalGroups_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test__loadYamlLocalGroups(self):
        expected_localGroups = LocalGroups(gl_list_oneState)
        localGroups = loadYamlLocalGroups('../testData/alias/minimal_gl.yaml')
        self.assertNsEqual(localGroups.data, expected_localGroups.data)

    def test__aliasFilters__oneState(self):
        localGroups = LocalGroups(gl_list_oneState)
        expected = [('state', '21')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__manyStates(self):
        localGroups = LocalGroups(gl_list_manyStates)
        expected = [('state', '21'), ('state', '22')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__NonExistant(self):
        localGroups = LocalGroups(gl_list_manyStates)
        expected = None
        self.assertEqual(localGroups.aliasFilters(2), expected)

    def test__aliasFilters__oneCity(self):
        localGroups = LocalGroups(gl_list_oneCity)
        expected = [('city', '170031')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__manyCities(self):
        localGroups = LocalGroups(gl_list_manyCities)
        expected = [('city', '170010'), ('city', '170031')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__oneCCAA(self):
        localGroups = LocalGroups(gl_list_oneCCAA)
        expected = [('ccaa', '33')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__manyCCAA(self):
        localGroups = LocalGroups(gl_list_manyCCAA)
        expected = [('ccaa', '17'), ('ccaa', '33')]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__getLocalGroups(self):
        localGroups = LocalGroups(gl_list_getLocalGroups)
        expected = [(1, 'La xocolata de Girona')]
        self.assertEqual(localGroups.getLocalGroups(), expected)

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