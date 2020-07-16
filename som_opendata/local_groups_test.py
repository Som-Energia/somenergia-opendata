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
        self.assertNsEqual(localGroups.aliasFilters(['Alacant']), ns(state=['03']))

    def test__aliasFilters__manyStates(self):
        expected = ns(state=['04','11'])
        self.assertEqual(localGroups.aliasFilters(['AlmeriaCadiz']), expected)

    def test__aliasFilters__NonExistant(self):
        with self.assertRaises(AliasNotFoundError) as ctx:
            localGroups.aliasFilters(['NonExistant'])

    def test__aliasFilters__noCodes(self):
        self.assertEqual(localGroups.aliasFilters([]), ns())

    def test__aliasFilters__manyGeolevels(self):
        expected = ns(ccaa=['09'],city=['28079'])
        self.assertEqual(localGroups.aliasFilters(['CatalunyaMadrid']), expected)

    def test__getLocalGroups(self):
        expected = [('Alacant', 'Alacant'), ('AlmeriaCadiz', 'Almería y Cádiz')]
        self.assertEqual(minimalLocalGroups.getLocalGroups(), expected)

    def test__aliasFilters__manyAliasDifferentGeolevel(self):
        expected = ns(state=['03'], city=['17079', '17155'])
        result = localGroups.aliasFilters(['Alacant', 'GironaSalt'])
        self.assertNsEqual(result, expected)

    def test__aliasFilters__manyAliasSharedGeolevel(self):
        expected = ns(ccaa=['09'],city=['28079','17079','17155'])
        result = localGroups.aliasFilters(['CatalunyaMadrid', 'GironaSalt'])
        self.assertNsEqual(result, expected)

    def test__get__ensureImmutable(self):
        before = localGroups.get('Alacant')
        before.update({'temp':'temp'})
        self.assertEqual(
            localGroups.get('Alacant'),
            ns(name='Alacant', alias=ns(state=['03']))
        )
