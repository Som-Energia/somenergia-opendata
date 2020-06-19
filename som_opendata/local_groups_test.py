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

    def test__aliasFilters__getLocalGroups(self):
        localGroups = LocalGroups(gl_list_getLocalGroups)
        expected = [(1, 'La xocolata de Girona')]
        self.assertEqual(localGroups.getLocalGroups(), expected)
