import unittest
from yamlns import namespace as ns
from .localGroups import LocalGroups, loadYamlLocalGroups

gl_list_oneState = ns.loads("""\
1:
    name: Vitoria-Gasteiz
    geolevel: state
    codes: [21]
""")
gl_list_manyStates = ns.loads("""\
1:
    name: Vitoria-Gasteiz
    geolevel: state
    codes: [21, 22] 
""")
class LocalGroups_Test(unittest.TestCase):

    from somutils.testutils import assertNsEqual

    def test__loadYamlLocalGroups(self):
        expected_localGroups = LocalGroups(gl_list_oneState)
        localGroups = loadYamlLocalGroups('../testData/alias/minimal_gl.yaml')
        self.assertNsEqual(localGroups.data, expected_localGroups.data)

    def test__aliasFilters__oneState(self):
        localGroups = LocalGroups(gl_list_oneState)
        expected = [('state', 21)]
        self.assertEqual(localGroups.aliasFilters(1), expected)

    def test__aliasFilters__manyStates(self):
        localGroups = LocalGroups(gl_list_manyStates)
        expected = [('state', 21),('state', 22)]
        self.assertEqual(localGroups.aliasFilters(1), expected)

