# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, make_response, send_file
from yamlns import namespace as ns
from .common import (
    yaml_response,
    validateParams,
    validateMapParams,
)
from .timeaggregator import TimeAggregator
from . import common
from .distribution import getAggregated
from .errors import MissingDateError
from . import __version__
from .map import renderMap
from flask_babel import Babel, get_locale


api = Blueprint(name=__name__, import_name=__name__, template_folder='../')
api.firstDate = '2010-01-01'

@api.route('/version')
@yaml_response
def version():
    """
    @api {get} /v0.2/version Version information
    @apiVersion 0.2.17
    @apiName Version
    @apiGroup About
    @apiDescription Returns current and oldest backward compatible versions

    @apiSuccessResponse 200
    @apiSuccess version Current api version
    @apiSuccess compat Oldest backward compatible version

    @apiSampleRequest /v0.2/version
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        version: 0.2.17
        compat: 0.2.1
    """
    return ns(
        version = __version__,
        compat = '0.2.1',
        )

@api.route('/spec')
@yaml_response
def spec():
    """
    @api {get} /v0.2/spec API specification
    @apiVersion 0.2.17
    @apiName API specification
    @apiGroup About
    @apiDescription OpenData API specification as OpenAPI 3.0 YAML

    @apiSuccessResponse 200

    @apiSampleRequest /v0.2/spec
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
    """
    return ns(
        version = __version__,
        compat = '0.2.1',
        )
    return send_file(
        '../openapi.yaml',
        as_attachment = True,
        attachment_filename = "somenergia-opendata-{}.yaml".format(__version__),
    )


@api.route('/discover/metrics')
@yaml_response
def discoverMetrics():
    """
    @api {get} /v0.2/discover/metrics Available metrics
    @apiVersion 0.2.17
    @apiName GetMetrics
    @apiGroup Discover
    @apiDescription Returns the metrics that can be queried.
    @apiUse QueryLang

    @apiSuccessResponse 200
    @apiSuccess {Object[]} metrics List of metrics
    @apiSuccess {String} metrics.id The id to refer the metric
    @apiSuccess {String} metrics.text Translated text to show users
    @apiSuccess {String} metrics.description Translated Markdown text explaining the metric

    @apiSampleRequest /v0.2/discover/metrics
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        metrics:
        - id: members
          text: 'Members'
          description: "Members of the cooperative at the end of the day."
        - id: contracts
          text: 'Contracts'
          description: "Active contracts at the end of the day."
    """
    return ns(metrics=[
        ns(
            id = key,
            text = format(value.text), # Translates
            description = format(value.description), # Translates
        )
        for key,value in common.metrics.items()
    ])


@api.route('/discover/geolevel')
@yaml_response
def discoverGeoLevel():
    """
    @api {get} /v0.2/discover/geolevel Available Geolevels
    @apiVersion 0.2.17
    @apiName GetGeolevels lala
    @apiGroup Discover
    @apiDescription Returns the geolevels (geographical levels) that can be used in queries, such as countries, states, cities
    @apiUse QueryLang

    @apiSuccessResponse 200
    @apiSuccess {Object[]} geolevels List of geolevels
    @apiSuccess {String} geolevels.id The id to refer the geolevel
    @apiSuccess {String} geolevels.text Translated text to show users
    @apiSuccess {String} [geolevels.plural=id+"s"] Plural tag to use in structures
    @apiSuccess {String} [geolevels.parent=null] The parent geolevel
    @apiSuccess {Boolean} [geolevels.detailed=true] Set to false if it is not supported as level of detail for distributions
    @apiSuccess {Boolean} [geolevels.mapable=true] Set to false if it is not supported as level of detail for map

    @apiSampleRequest /v0.2/discover/geolevel
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
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
    """
    return ns(
        geolevels = [
        ns(data,
            id=key,
            text=format(data.text), # overwrite lazy translated
        )
        for key, data in common.geolevels.items()
    ])

@api.route('/discover/geolevel/<geolevel>')
@yaml_response
def discoverGeoLevelOptions(geolevel):
    """
    @api {get} /v0.2/discover/geolevel/:geolevel Available Geolevel values
    @apiVersion 0.2.17
    @apiName Geolevels values
    @apiGroup Discover
    @apiDescription Returns the available values for a given geografical division
    @apiUse PathGeolevelAndAlias
    @apiUse QueryGeolevelAndAlias
    @apiUse QueryLang

    @apiSuccessResponse 200
    @apiSuccess options {Object) Mapping of level codes to its translated display text


    @apiSuccessExample {yaml} All Autonomous Comunities
        /v0.2/discover/geolevel/ccaa
        HTTP/1.1 200OK
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

    @apiSuccessExample {yaml} All local grups in Catalonia
        /v0.2/discover/geolevel/localgroups?ccaa=09
        HTTP/1.1 200OK
        options:
          AltPenedes: Alt Penedès
          Anoia: Anoia
          Badalona: Badalona
          Bages: Bages
          BaixLlobregat: Baix Llobregat
          BaixMontseny: Baix Montseny
          BaixValles: Baix Vallès
          Barcelona: Barcelona
          CastellarValles: Castellar del Vallès
          CerdanyolaValles: Cerdanyola del Vallès
          Maresme: Maresme
          Osona: Osona
          Rubi: Rubí
          Sabadell: Sabadell
          SantCugatValles: Sant Cugat del Vallès
          SelvaMaritima: Selva Marítima
          Terrassa: Terrassa
    """
    filters = locationFiltersFromQuery()
    return ns(options=api.source.geolevelOptions(geolevel, **filters))

def locationFiltersFromQuery():
    """Extracts any relevant query parameter to build a filter.
    """
    return ns(
        (key, request.args.getlist(key))
        for key in [
            # TODO: take list from source
            'country',
            'ccaa',
            'state',
            'city',
            'localgroup',
        ]
        if key in request.args
    )

def validateInputDates(ondate = None, since = None, todate = None):
    return ondate is None or (
        since is None and todate is None
    )


"""
@api {get} /v0.2/:metric/by/:geolevel/on/:ondate Metric Data on a Given Date

@apiVersion 0.2.17
@apiGroup Distribution
@apiName Distribution
@apiDescription Returns the geographical distribution of a metric at a given date.

Use the filters in the query string to restrict to a group of geographical entities.
The filters are additive. That means that any city matching any of the specified values will be counted.

@apiExample Current number of contracts
    /v0.2/contracts
@apiExample Current members at every state
    /v0.2/members/by/state
@apiExample Members at every CCAA on 2018-02-01
    /v0.2/members/by/ccaa/on/2018-02-01
@apiExample Members by city on Araba and Gipuzcoa provinces
    /v0.2/members/by/city?state=01&state=20

@apiParam {String="contracts","members"} metric Quantity to aggregate.
@apiUse PathMetric
@apiUse PathGeolevel
@apiUse PathOnDate
@apiUse QueryGeolevelAndAlias

@apiUse ResponseNumbers

@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    dates:
    - 2013-01-01
    values:
    - 3197
    countries:
      ES:
        name: España
        values:
        - 3197
        ccaas:
          '01':
            name: Andalucia
            values:
            - 48
          '02':
            name: Aragón
            values:
            - 124
          '03':
            name: Asturias, Principado de
            values:
            - 13
          '04':
            name: Baleares, Islas
            values:
            - 235
          '05':
            name: Canarias
            values:
            - 0
          '06':
            name: Cantabria
            values:
            - 12
          08:
            name: Castilla - La Mancha
            values:
            - 28
          '07':
            name: Castilla y León
            values:
            - 24
          09:
            name: Cataluña
            values:
            - 2054
          '10':
            name: Comunidad Valenciana
            values:
            - 224
          '11':
            name: Extremadura
            values:
            - 14
          '12':
            name: Galicia
            values:
            - 24
          '13':
            name: Madrid, Comunidad de
            values:
            - 145
          '14':
            name: Murcia, Región de
            values:
            - 11
          '15':
            name: Navarra, Comunidad Foral de
            values:
            - 151
          '16':
            name: País Vasco
            values:
            - 53
          '17':
            name: Rioja, La
            values:
            - 37
"""

"""
@api {get} /v0.2/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate Metric Data on a Temporal Serie

@apiVersion 0.2.17
@apiGroup Distribution
@apiName DistributionSeries
@apiDescription Returns the geographical distribution and temporal evolution of a quantity.

Use the geolevel to get more geographical detail (country, ccaa, state, city).

Use the filters in the query string to restrict to a group of geographical entities.
The filters are additive. That means that any city matching any of the specified values will be counted.

@apiExample Evolution of all contracts every year
    /v0.2/contracts/yearly
@apiExample Monthly evolution of members on 2018
    /v0.2/members/monthly/from/2018-01-01/to/2019-01-01
@apiExample 2018 monthly evolution of members
    /v0.2/members/monthly/from/2018-01-01/to/2019-01-01
@apiExample Members by city on Araba and Gipuzcoa provinces every year
    /v0.2/members/by/city/yearly?state=01&state=20


@apiUse PathMetric
@apiUse PathGeolevel
@apiUse QueryGeolevelAndAlias
@apiUse PathFromToDate

@apiUse ResponseNumbers

@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    dates:
    - 2010-01-01
    - 2011-01-01
    - 2012-01-01
    - 2013-01-01
    values:
    - 0
    - 0
    - 277
    - 3197
    countries:
      ES:
        name: España
        values:
        - 0
        - 0
        - 277
        - 3197
        ccaas:
          '01':
            name: Andalucia
            values:
            - 0
            - 0
            - 0
            - 48
          '02':
            name: Aragón
            values:
            - 0
            - 0
            - 0
            - 124
          '03':
            name: Asturias, Principado de
            values:
            - 0
            - 0
            - 0
            - 13
          '04':
            name: Baleares, Islas
            values:
            - 0
            - 0
            - 1
            - 235
          '05':
            name: Canarias
            values:
            - 0
            - 0
            - 0
            - 0
          '06':
            name: Cantabria
            values:
            - 0
            - 0
            - 0
            - 12
          08:
            name: Castilla - La Mancha
            values:
            - 0
            - 0
            - 0
            - 28
          '07':
            name: Castilla y León
            values:
            - 0
            - 0
            - 0
            - 24
          09:
            name: Cataluña
            values:
            - 0
            - 0
            - 256
            - 2054
          '10':
            name: Comunidad Valenciana
            values:
            - 0
            - 0
            - 11
            - 224
          '11':
            name: Extremadura
            values:
            - 0
            - 0
            - 0
            - 14
          '12':
            name: Galicia
            values:
            - 0
            - 0
            - 0
            - 24
          '13':
            name: Madrid, Comunidad de
            values:
            - 0
            - 0
            - 3
            - 145
          '14':
            name: Murcia, Región de
            values:
            - 0
            - 0
            - 0
            - 11
          '15':
            name: Navarra, Comunidad Foral de
            values:
            - 0
            - 0
            - 6
            - 151
          '16':
            name: País Vasco
            values:
            - 0
            - 0
            - 0
            - 53
          '17':
            name: Rioja, La
            values:
            - 0
            - 0
            - 0
            - 37
"""

@api.route('/<string:metric>') # TODO: UNTESTED
@api.route('/<string:metric>/on/<isodate:ondate>')
@api.route('/<string:metric>/<string:frequency>')
@api.route('/<string:metric>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/<string:metric>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<string:metric>/<string:frequency>/to/<isodate:todate>')
@api.route('/<string:metric>/by/<string:geolevel>')
@api.route('/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<string:metric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@yaml_response
def distribution(metric=None, geolevel='world', ondate=None, frequency=None, fromdate=None, todate=None):

    validateParams(
        frequency=frequency,
        metric=metric,
        geolevel=geolevel,
    )

    timeDomain = TimeAggregator.Create(
        operator = common.metrics[metric].timeaggregation,
        first=api.firstDate,
        last=api.source.getLastDay(metric),
        on=ondate,
        since=fromdate,
        to=todate,
        periodicity=frequency,
    )

    filters = locationFiltersFromQuery()

    return getAggregated(
        source=api.source,
        metric=metric,
        timeDomain=timeDomain,
        location_filter=filters,
        geolevel=geolevel,
        mutable=False,
    )




"""
@api {get} /v0.2/map/:metric/by/:geolevel/on/:ondate Absolute Metrics Map

@apiVersion 0.2.17
@apiGroup Maps
@apiName Static Map
@apiDescription Returns a map that represents the geographical distribution at a given date.

Use the geolevel choose the map detail (ccaa, state).
Use the filters in the query string to choose the language.
If no language is specified, the language is chosen using the request headers.

@apiExample Current contracts by CCAA
    /v0.2/map/contracts/by/ccaa
@apiExample Members by state on 2018-02-01
    /v0.2/map/members/by/state/on/2018-02-01
@apiExample Members by ccaa in Galician
    /v0.2/map/members/by/ccaa?lang=gl

@apiUse PathMetric
@apiParam {String="ccaa","state"} geolevel Geographical detail level
@apiUse PathOnDate
@apiUse QueryLang

@apiSuccess {svg} Response Map that represents the geographical distribution at a given date

"""

"""
@api {get} /v0.2/map/:metric/per/:relativemetric/by/:geolevel/on/:ondate Relative Metrics Map

@apiVersion 0.2.7
@apiGroup Maps
@apiName RelativeMap
@apiDescription Returns a map that represents the relative geographical distribution at a given date.

Use the geolevel choose the map detail (ccaa, state).
Use the relativemetric to specify the metric to relativize the values by.
Use the filters in the query string to choose the language.
If no language is specified, the language is chosen using the request headers.

@apiExample Current contracts per population by CCAA
    /v0.2/map/contracts/per/population/by/ccaa
@apiExample Current members per population by state
    /v0.2/map/members/per/population/by/state
@apiExample Members per population by CCAA on 2018-02-01
    /v0.2/map/members/per/population/by/ccaa/on/2018-02-01
@apiExample Members per population by ccaa in Galician
    /v0.2/map/members/per/population/by/ccaa?lang=gl

@apiUse PathMetric
@apiUse PathRelativeMetric
@apiUse PathMapGeolevel
@apiUse PathOnDate
@apiUse QueryLang

@apiSuccess {svg} Response Map that represents the relative geographical distribution at a given date

"""

"""
@api {get} /v0.2/map/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate Absolute Metrics Map Animation

@apiVersion 0.2.17
@apiGroup Maps
@apiName MapSeries
@apiDescription Returns a map animation that represents the temporal evolution of the geographical distribution.

Use the geolevel choose the map detail (ccaa, state).
Use the filters in the query string to choose the language.
If no language is specified, the language is chosen using the request headers.

@apiExample Evolution of all contracts by CCAA every year
    /v0.2/map/contracts/by/ccaa/yearly
@apiExample Monthly evolution of members by state on 2018
    /v0.2/map/members/by/state/monthly/from/2018-01-01/to/2019-01-01
@apiExample Monthly evolution of members by CCAA from 2018-01-01
    /v0.2/map/members/by/ccaa/monthly/from/2018-01-01
@apiExample Members by ccaa every year in Galician
    /v0.2/map/members/by/ccaa/yearly?lang=gl


@apiUse PathMetric
@apiUse PathMapGeolevel
@apiUse PathFromToDate
@apiUse QueryLang

@apiSuccess {svg} Response Map animation that represents the temporal evolution of the geographical distribution
    HTTP/1.1 200 OK
"""
"""
@api {get} /v0.2/map/:metric/per/:relativemetric/by/:geolevel/:frequency/from/:fromdate/to/:todate Relative Metrics Map Animation

@apiVersion 0.2.17
@apiGroup Maps
@apiName RelativeMapSeries
@apiDescription Returns a map animation that represents the temporal evolution of the relative geographical distribution.

Use the geolevel choose the map detail (ccaa, state).
Use the relativemetric to specify the metric to relativize the values by.
Use the filters in the query string to choose the language.
If no language is specified, the language is chosen using the request headers.

@apiExample Evolution of all contracts per population by CCAA every year
    /v0.2/map/contracts/per/population/by/ccaa/yearly
@apiExample Monthly evolution of members per population by state on 2018
    /v0.2/map/members/per/population/by/state/monthly/from/2018-01-01/to/2019-01-01
@apiExample Monthly evolution of members per population by CCAA from 2018-01-01
    /v0.2/map/members/per/population/by/ccaa/monthly/from/2018-01-01
@apiExample Members per population by ccaa every year in Galician
    /v0.2/map/members/per/population/by/ccaa/yearly?lang=gl


@apiUse PathMetric
@apiUse PathMapGeolevel
@apiUse PathRelativeMetric
@apiUse PathFromToDate
@apiUse QueryLang

@apiSuccess {svg} Response Map animation that represents the temporal evolution of the geographical distribution
    HTTP/1.1 200 OK

"""

@api.route('/map/<string:metric>')
@api.route('/map/<string:metric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
def map(metric=None, ondate=None, geolevel='ccaa', frequency=None, fromdate=None, todate=None, relativemetric=None):

    validateMapParams(
        frequency=frequency,
        geolevel=geolevel,
        metric=metric,
        relativemetric=relativemetric,
    )

    timeDomain = TimeAggregator.Create(
        operator = common.metrics[metric].timeaggregation,
        first=api.firstDate,
        last=api.source.getLastDay(metric),
        on=ondate,
        since=fromdate,
        to=todate,
        periodicity=frequency,
    )

    locationCodes = api.relativeMetricSource.getCodesByGeolevel(geolevel=geolevel)
    relativeMValues = api.relativeMetricSource.getValuesByCode(
        metric=relativemetric,
        geolevel=geolevel,
    ) if relativemetric else dict()

    result = renderMap(
        source=api.source,
        metric=metric,
        timeDomain=timeDomain,
        geolevel=geolevel,
        template=api.mapTemplateSource.getTemplate(
            geolevel=geolevel,
            lang=str(get_locale()),
        ),
        legendTemplate=api.mapTemplateSource.getLegend(),
        locationsCodes=locationCodes,
        relativeMetricValues=relativeMValues,
    )
    response = make_response(result)
    response.mimetype = 'image/svg+xml'
    return response

api.source = None
api.mapTemplateSource = None
api.relativeMetricSource = None
api.localGroups = None

"""
@apiDefine PathMetric

@apiParam {String="contracts","members", "newcontracts", "canceledcontracts", "newmembers", "canceledmember"} metric Quantity to aggregate

"""

"""
@apiDefine PathRelativeMetric

@apiParam {String="population"} relativemetric Metric to relativize the values by

"""

"""
@apiDefine PathGeolevel

@apiParam {Enum=country,ccaa,state,city} [geolevel=world] Geographical detail level.
Use the geolevel to get more geographical detail (country, ccaa, state, city).
For just global numbers, remove the whole `/by/:geolevel` portion of the path.

"""

"""
@apiDefine PathGeolevelAndAlias

@apiParam {Enum="country","ccaa","state","city","localgroup"} geolevel Geographical detail level, including aliased geolevel alias, like localgroup.

"""

"""
@apiDefine PathOnDate

@apiParam {Date} [ondate]  Single date, in ISO format (YYYY-MM-DD).
To obtain the last available data, remove the whole `/on/:onDate` portion of the path.

"""

"""
@apiDefine PathMapGeolevel

@apiParam {String="ccaa","state"} geolevel Geographical detail level

"""
"""
@apiDefine QueryGeolevel

@apiParam (Query Parameters) {String[]} [country] ISO codes of the countries to be included
@apiParam (Query Parameters) {String[]} [ccaa] INE codes of the CCAAs to be included
@apiParam (Query Parameters) {String[]} [state] INE codes of the states to be included
@apiParam (Query Parameters) {String[]} [city] INE codes of cities to be included

"""

"""
@apiDefine QueryGeolevelAndAlias

@apiParam (Query Parameters) {String[]} [country] ISO codes of the countries to be included
@apiParam (Query Parameters) {String[]} [ccaa] INE codes of the CCAAs to be included
@apiParam (Query Parameters) {String[]} [state] INE codes of the states to be included
@apiParam (Query Parameters) {String[]} [city] INE codes of cities to be included
@apiParam (Query Parameters) {String[]} [localgroup] Code of the Local Group to be included. It represents an alias of one or more filters.

"""

"""
@apiDefine QueryLang

@apiParam (Query Parameters) {String="en", "es", "ca", "gl", "eu"} [lang=browser defined or en] Forced response language
If no language is forced, the one in the browser (Accepted-Language header) is taken.
If the languange is not one of the suppoerted, english is taken by default.

"""

"""
@apiDefine PathFromToDate

@apiParam {String="yearly","monthly"} frequency  Indicate a date series (only first day of the month, year...)
@apiParam {Date} [fromdate=2012-01-01]  Earlier date to show, in iso format
@apiParam {Date} [todate=2020-02-01]  Later date to show, in iso format

"""

"""
@apiDefine ResponseNumbers

@apiSuccessResponse 200
@apiSuccess {Date[]}   dates Date sequence for all data
@apiSuccess {int[]}    countries.values Values aggregated at this level for each date
@apiSuccess {Object[]} countries Map indexed by country code
@apiSuccess {String}   countries.name User visible translated text for CCAA
@apiSuccess {int[]}    countries.values Values aggregated at this level for each date
@apiSuccess {Object[]} countries.ccaas Map indexed by CCAA code
@apiSuccess {String}   countries.ccaas.name User visible translated text for CCAA
@apiSuccess {int[]}    countries.ccaas.values Values aggregated at this level for each date
@apiSuccess {Object[]} countries.ccaas.states Map indexed by state code
@apiSuccess {String}   countries.ccaas.states.name User visible translated text for state
@apiSuccess {int[]}    countries.ccaas.states.values Values aggregated at this level for each date
@apiSuccess {Object[]} countries.ccaas.states.cities Map indexed by city code
@apiSuccess {String}   countries.ccaas.states.cities.name User visible translated text for city
@apiSuccess {int[]}    countries.ccaas.states.cities.values Values aggregated at this level for each date

"""



# vim: et ts=4 sw=4
