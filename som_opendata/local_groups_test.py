import unittest
from yamlns import namespace as ns
from .local_groups import LocalGroups, loadYamlLocalGroups
from .errors import AliasNotFoundError

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

        self.assertNsEqual(result, expected)

        self.assertNsEqual(result, expected)

    def test__get__ensureImmutable(self):
        before = localGroups.get('Alacant')
        before.update({'temp':'temp'})
        self.assertEqual(
            localGroups.get('Alacant'),
            ns(name='Alacant', alias=ns(state=['03']))
        )
