# -*- encoding: utf-8 -*-
import unittest
from dateutil.relativedelta import relativedelta as delta
from yamlns.dateutils import Date
from yamlns import namespace as ns
import b2btest
from flask import Flask, request
from flask_babel import _, Babel, get_locale
from .api import api, validateInputDates
from . import __version__
from . import common
from .templateSource import loadMapData
from .tsvRelativeMetricSource import loadTsvRelativeMetric
from .local_groups import loadYamlLocalGroups
from .csvSource import loadCsvSource


localgroups = loadYamlLocalGroups(relativeFile='../testData/alias/gl.yaml')
source = loadCsvSource(relativePath='../testData/metrics', aliases=ns(localgroup=localgroups.data))
mapTemplateSource = loadMapData()
relativeMetricSource = loadTsvRelativeMetric()

headers = u"codi_pais\tpais\tcodi_ccaa\tcomunitat_autonoma\tcodi_provincia\tprovincia\tcodi_ine\tmunicipi\tcount_2018_01_01"
data_Adra = u"ES\tEspaña\t01\tAndalucía\t04\tAlmería\t04003\tAdra\t2"
data_Perignan = u"FR\tFrance\t76\tOccità\t66\tPyrénées-Orientales\t66136\tPerpignan\t10"
data_Girona = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17079\tGirona\t20"
data_SantJoan = u"ES\tEspaña\t09\tCatalunya\t08\tBarcelona\t08217\tSant Joan Despí\t1000"
data_Amer = u"ES\tEspaña\t09\tCatalunya\t17\tGirona\t17007\tAmer\t2000"



class ApiHelpers_Test(unittest.TestCase):

    def test__validateInputDates__since_toDate(self):
        r = validateInputDates(since='2018-01-01', todate='2018-01-02')
        self.assertEqual(r, True)

    def test__validateInputDates__since(self):
        r = validateInputDates(since='2018-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__since_toDate_turnedDates(self):
        r = validateInputDates(since='2010-01-01', todate='2018-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__onDate(self):
        r = validateInputDates(ondate='2010-01-01')
        self.assertEqual(r, True)

    def test__validateInputDates__onDate_since(self):
        r = validateInputDates(ondate='2010-01-01', since='2018-01-01')
        self.assertEqual(r, False)

    def test__validateInputDates__onDate_toDate(self):
        r = validateInputDates(ondate='2010-01-01', todate='2018-01-01')
        self.assertEqual(r, False)


class Api_Test(unittest.TestCase):

    @staticmethod
    def setUpClass():
        Api_Test.maxDiff=100000
        Api_Test.app = app = Flask(__name__)
        common.register_converters(app)
        common.register_handlers(app)
        app.register_blueprint(api, url_prefix='')
        app.config['TESTING']=True
        app.config['LANGUAGES'] = ['en', 'es', 'ca', 'eu', 'gl']

    def setUp(self):
        self.client = self.app.test_client()
        self.b2bdatapath = 'b2bdata'
        self.oldsource = api.source
        self.oldMapSource = api.mapTemplateSource
        self.oldFirstDate = api.firstDate
        self.oldRelativeData = api.relativeMetricSource
        self.oldLocalGroups = api.localGroups
        api.source = source
        api.localGroups = localgroups
        api.mapTemplateSource = mapTemplateSource
        api.relativeMetricSource = relativeMetricSource
        api.firstDate = '2010-01-01'
        self.babel = Babel()
        self.babel.init_app(self.app)

        @self.babel.localeselector
        def get_locale():
            lang = request.args.get('lang')
            if lang in self.app.config['LANGUAGES']:
                return lang
            return request.accept_languages.best_match(self.app.config['LANGUAGES'])

    def tearDown(self):
        api.source = self.oldsource
        api.mapTemplateSource = self.oldMapSource
        api.relativeMetricSource = self.oldRelativeData
        api.firstDate = self.oldFirstDate
        api.localgroups = self.oldLocalGroups

    def get(self, uri, *args, **kwds):
        return self.client.get(uri,*args,**kwds)

    from somutils.testutils import assertNsEqual

    def assertYamlResponse(self, response, expected, status=200):
        self.assertNsEqual(response.data, expected)
        self.assertEqual(response.status_code, status)

    def assertTsvResponse(self, response, status=200):
        self.assertB2BEqual(response.data)
        self.assertEqual(response.status_code, status)


    def test__version(self):
        r = self.get('/version')
        self.assertYamlResponse(r, """\
            version: '{}'
            compat: '0.2.1'
            """.format(__version__))


    def test__metrics(self):
        r = self.get('/discover/metrics')
        self.assertYamlResponse(r, """\
            metrics:
            - id: members
              text: 'Members'
              description: 'Current cooperative members at the start of a given date.


                Members are taken from our current ERP data, so the following considerations apply:

                - Membership during the first months of the cooperative was stored in spreadsheets and is not included yet.

                - There is no historical record of member addresses.
                So, if a member has changed her home from Vigo to Cartagena,
                it counts as she has been been living all the time in Cartagena.

                - Only a single start date can be stored so, canceled and later renewed memberships are not properly recorded.

                '
            - id: newmembers
              text: 'New members'
              description: 'New cooperative members during the month before a given date.


                Considerations for "Members" metric also apply in this one.

                '
            - id: canceledmembers
              text: 'Canceled members'
              description: 'Members leaving the cooperative during in the month before a given date.


                Considerations for "Members" metric also apply in this one.

                '
            - id: contracts
              text: 'Contracts'
              description: 'Current active contracts at the start of a given date.


                Contract data is taken from activation and deactivation dates from ATR system.

                Old contracts were copied by hand from ATR files and may be less reliable.

                '
            - id: newcontracts
              text: 'New contracts'
              description: 'Contracts starting during in the month before a given date.


                Considerations for "Contracts" metric also apply in this one.

                '
            - id: canceledcontracts
              text: 'Canceled contracts'
              description: 'Contracts ending during in the month before a given date.


                Considerations for "Contracts" metric also apply in this one.

                '
            """)

    def test__metrics_translated(self):
        r = self.get('/discover/metrics?lang=ca')
        # text and description should be in catalan
        self.assertB2BEqual(r.data)

    def test_geolevel(self):
        r = self.get('/discover/geolevel')
        self.assertYamlResponse(r, """\
            geolevels:
            - id: world
              text: 'World'
              mapable: False
            - id: country
              text: 'Country'
              parent: world
              plural: countries
              mapable: False
            - id: ccaa
              text: 'CCAA'
              parent: country
              plural: ccaas
            - id: state
              text: 'State'
              parent: ccaa
              plural: states
            - id: city
              text: 'City'
              parent: state
              plural: cities
              mapable: False
            - id: localgroup
              text: 'Local Group'
              parent: world
              plural: localgroups
              detailed: False
              mapable: False
            """)

    def test_geolevel_translated(self):
        r = self.get('/discover/geolevel?lang=ca')
        self.assertYamlResponse(r, """\
            geolevels:
            - id: world
              text: 'Món'
              mapable: False
            - id: country
              text: 'País'
              parent: world
              plural: countries
              mapable: False
            - id: ccaa
              text: 'Comunitat Autònoma'
              parent: country
              plural: ccaas
            - id: state
              text: 'Província'
              parent: ccaa
              plural: states
            - id: city
              text: 'Municipi'
              parent: state
              plural: cities
              mapable: False
            - id: localgroup
              text: 'Grup Local'
              parent: world
              plural: localgroups
              detailed: False
              mapable: False
            """)


    def test_geolevelOptions_unfiltered(self):
        r = self.get('/discover/geolevel/ccaa')
        self.assertYamlResponse(r, """\
            options:
              '01': Andalucia
              '02': Aragón
              '03': Asturias, Principado de
              '04': Baleares, Islas
              '05': Canarias
              '06': Cantabria
              '07': Castilla y León
              '08': Castilla - La Mancha
              '09': Cataluña
              '10': Comunidad Valenciana
              '11': Extremadura
              '12': Galicia
              '13': Madrid, Comunidad de
              '14': Murcia, Región de
              '15': Navarra, Comunidad Foral de
              '16': País Vasco
              '17': Rioja, La
              '19': Melilla
              None: None
            """)

    def test_geolevelOptions_alias(self):
        r = self.get('/discover/geolevel/localgroup')
        self.assertYamlResponse(r, """\
            options:
                Alacant: Alacant
                AlmeriaCadiz: Almería y Cádiz
                CatalunyaMadrid: Gl de Catalunya i Madrid ciutat
                GironaCiutat: Gl de Girona
                GironaSalt: Gl de Girona i Salt
            """)

    def test_geolevelOptions_filtered(self):
        r = self.get('/discover/geolevel/state?ccaa=09')
        self.assertYamlResponse(r, """\
            options:
                '08': Barcelona
                '17': Girona
                '25': Lleida
                '43': Tarragona
            """)

    def test_geolevelOptions_alias_filtered(self):
        r = self.get('/discover/geolevel/localgroup?ccaa=01')
        self.assertYamlResponse(r, """\
            options:
                AlmeriaCadiz: Almería y Cádiz
            """)

    def test__metric_onDate(self):
        r = self.get('/members/on/2018-01-01')
        self.assertTsvResponse(r)

    def test__metric_level_onDate(self):
        r = self.get('/members/by/world/on/2018-01-01')
        self.assertTsvResponse(r)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__metric_today(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/members')
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today())+"""]
            values: [123]
            """)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__metric_level__today(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123',
            )
        r = self.get('/members/by/city')
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today())+"""]
            values: [123]
            countries:
              ES:
                name: España
                values: [123]
                ccaas:
                  '01':
                    name: Andalucía
                    values: [123]
                    states:
                      '04':
                        name: Almería
                        values: [123]
                        cities:
                          '04003':
                            name: Adra
                            values: [123]
            """)

    def test__metric_level_frequency(self):
        r = self.get('/members/by/country/yearly')
        self.assertTsvResponse(r)

    def test__metric_level_frequency_fromDate(self):
        r = self.get('/members/by/world/yearly/from/2017-01-01')
        self.assertTsvResponse(r)

    def test__metric_level_frequency_fromDate_toDate(self):
        r = self.get('/members/by/world/monthly/from/2018-01-01/to/2018-03-01')
        self.assertTsvResponse(r)

    def test__metric_level_frequency_fromDate_sumAggregatedMonth(self):
        r = self.get('/newmembers/by/world/yearly/from/2017-01-01')
        self.assertTsvResponse(r)

    def test__metric_level_frequency_toDate(self):
        api.firstDate = '2018-02-01'
        r = self.get('/members/by/world/monthly/to/2018-03-01')
        self.assertTsvResponse(r)

    @unittest.skip('NOT IMPLEMENTED YET')
    def test__metric_frequency_formDate(self):
        self.setupSource(
            headers+'\tcount_'+str(Date.today()-delta(weeks=1)).replace('-','_')+'\tcount_'+str(Date.today()).replace('-','_'),
            data_Adra+'\t123\t1234567',
            )
        r = self.get('/members/weekly/from/'+str(Date.today()-delta(weeks=1)))
        self.assertEqual(r.status, '200 OK')    # En cas de ser NO OK petaria en el següent assert
        self.assertYamlResponse(r, """\
            dates: ["""+str(Date.today()-delta(weeks=1))+""", """+str(Date.today())+"""]
            values: [123, 1234567]
            """)

    def test__metric_frequency_fromDate_toDate(self):
        r = self.get('/members/monthly/from/2018-01-01/to/2018-02-01')
        self.assertTsvResponse(r)

    def test__metric_frequency(self):
        r = self.get('/members/yearly')
        self.assertTsvResponse(r)

    def test__metric_level_onDate_filter(self):
        r = self.get('/members/by/city/on/2018-01-01?city=17007')
        self.assertTsvResponse(r)

    def test__metric(self):
        r = self.get('/members')
        self.assertTsvResponse(r)

    def test__metric_onDate__oldDate(self):
        r = self.get('/members/on/1994-09-01')
        self.assertYamlResponse(r, """\
            message: Missing Dates ['1994-09-01']
            """, 500)

    def test__metric_level__badGeolevel(self):
        r = self.get('/members/by/badgeolevel')
        self.assertYamlResponse(r, """\
            parameter: geolevel
            valueRequest: badgeolevel
            possibleValues: ['world', 'country', 'ccaa', 'state', 'city']
            message: Invalid geolevel 'badgeolevel'. Accepted ones are 'world', 'country', 'ccaa', 'state', 'city'.
            """, 400)

    def test__metric_frequency__doesNotExist(self):
        r = self.get('/members/badly')
        self.assertYamlResponse(r, """\
            parameter: frequency
            valueRequest: badly
            possibleValues: ['monthly', 'yearly', null]
            message: Invalid frequency 'badly'. Accepted ones are 'monthly', 'yearly', None.
            """, 400)

    # TODO: turn 404 in yaml messages
    def test__metric_onDate__badDate(self):
        r = self.get('/members/on/baddate')
        self.assertEqual(r.data, b"Request not found!")
        self.assertEqual(r.status_code, 404)

    # TODO: Should it be an error
    def test__metric_level_onDate_filter__filterValueNotFound(self):
        r = self.get('/members/by/city/on/2018-01-01?city=9999999')
        self.assertYamlResponse(r, """\
            {}
        """, 200)


    # TODO: turn 404 in yaml messages
    def test__metric_level_onDate_fromDate__onAndFromIncompatible(self):
        r = self.get('/members/by/city/on/2018-01-01/from/2018-02-02')
        self.assertEqual(r.data, b"Request not found!")
        self.assertEqual(r.status_code, 404)


    def test__metric_level_onDate_filter__badLocalGroup(self):
        r = self.get('/members/by/city/on/2018-01-01?localgroup=Unknown')
        self.assertYamlResponse(r, """\
            message: localgroup 'Unknown' not found\n
        """, 400)

    def test__metric_level_onDate_filter__oneLocalGroup_equivalence(self):
        expected = self.get('/members/by/state/on/2018-01-01?state=03')
        r = self.get('/members/by/state/on/2018-01-01?localgroup=Alacant')
        self.assertEqual(r.data, expected.data)

    def test__metric_level_onDate_filter__manyLocalGroups_equivalence(self):
        expected = self.get('/members/by/state/on/2018-01-01?state=03&ccaa=09&city=28079')
        r = self.get('/members/by/state/on/2018-01-01?localgroup=Alacant&localgroup=CatalunyaMadrid')
        self.assertEqual(r.data, expected.data)

    def test__metric_frequency_fromDate_toDate__noExactFirstDate(self):
        r = self.get('/members/monthly/from/2018-03-15/to/2018-04-15')
        self.assertTsvResponse(r, 200)

    def test__metric__badMetric(self):
        r = self.get('/incorrectMetric')
        self.assertYamlResponse(r, """\
            parameter: metric
            valueRequest: incorrectMetric
            possibleValues: ['members', 'newmembers', 'canceledmembers', 'contracts', 'newcontracts', 'canceledcontracts']
            message: Invalid metric 'incorrectMetric'. Accepted ones are 'members', 'newmembers', 'canceledmembers', 'contracts', 'newcontracts', 'canceledcontracts'.
            """, 400)


    def test__map__ccaaMembers(self):
        r = self.get('/map/members')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__ccaaMembersDateSet(self):
        r = self.get('/map/members/on/2018-01-01')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__statesMembers(self):
        r = self.get('/map/members/by/state/on/2018-01-01')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__onDateMissing(self):
        r = self.get('/map/members/on/2038-01-01')
        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.mimetype, 'application/json')

    def test__map__wrongMetric(self):
        r = self.get('/map/badmetric')
        self.assertYamlResponse(r, """\
            parameter: metric
            valueRequest: badmetric
            possibleValues: ['members', 'newmembers', 'canceledmembers', 'contracts', 'newcontracts', 'canceledcontracts']
            message: Invalid metric 'badmetric'. Accepted ones are 'members', 'newmembers', 'canceledmembers', 'contracts', 'newcontracts', 'canceledcontracts'.
            """,400)
        self.assertEqual(r.mimetype, 'application/json')

    def test__map__cityLevelNotYetImplemented(self):
        r = self.get('/map/members/by/city')
        self.assertYamlResponse(r, """\
            parameter: geolevel
            valueRequest: city
            possibleValues: ['ccaa', 'state']
            message: Invalid geolevel 'city'. Accepted ones are 'ccaa', 'state'.
            """, 400)
        self.assertEqual(r.mimetype, 'application/json')

    def test__map__ccaaMembersPerPopulation(self):
        r = self.get('/map/members/per/population/on/2018-01-01')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__ccaaMembersRangeDates__animated(self):
        r = self.get('/map/members/by/ccaa/monthly/from/2018-10-01/to/2019-01-01')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__ccaaMembersCaLanguage(self):
        r = self.get('/map/members/on/2015-01-01', headers=[("Accept-Language", "ca")])
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    def test__map__ccaaState_CaLanguageByParam(self):
        r = self.get('/map/members/by/state/on/2015-01-01?lang=ca')
        self.assertEqual(r.status, '200 OK')
        self.assertEqual(r.mimetype, 'image/svg+xml')
        self.assertB2BEqual(r.data)

    @unittest.skip("Activated just for profiling, not regular testing")
    def test__profiling(self):
        for a in range(5):
            r = self.get('/members/by/city/monthly')


# vim: et ts=4 sw=4
