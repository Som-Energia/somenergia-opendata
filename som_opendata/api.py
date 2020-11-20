# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, make_response, send_file, render_template
from yamlns import namespace as ns
from .common import (
        yaml_response,
        dateSequenceMonths,
        dateSequenceWeeks,
        dateSequenceYears,
        requestDates,
        validateParams,
    )
from . import common
from .distribution import getAggregated
from .errors import MissingDateError
from . import __version__
from .map import renderMap
from .map_utils import validateImplementation
from flask_babel import lazy_gettext as _l
from flask_babel import _, Babel, get_locale


api = Blueprint(name=__name__, import_name=__name__, template_folder='../')
api.firstDate = '2010-01-01'


@api.route('/version')
@yaml_response
def version():
    """
    @api {get} /v0.2/version
    @apiVersion 0.2.2
    @apiName Version
    @apiGroup Version
    @apiDescription Response version API

    @apiSampleRequest /v0.2/version
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        version: 0.2.2
        compat: 0.2.1
    """
    return ns(
        version = __version__,
        compat = '0.2.1',
        )

@api.route('/introspection/metrics')
@yaml_response
def introspectionMetrics():
    """
    @api {get} /v0.2/introspection/metrics
    @apiVersion 0.2.2
    @apiName Metrics
    @apiGroup Introspection
    @apiDescription Returns the metrics that can be queried

    @apiSampleRequest /v0.2/introspection/metrics
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        metrics:
        - id: members
          text: 'Members'
        - id: contracts
          text: 'Contracts'
    """
    return ns(metrics=[
        ns(
            id = key,
            text = value,
        )
        for key,value in common.metrics.items()
    ])


@api.route('/introspection/geolevels')
@yaml_response
def introspectionGeoLevel():
    """
    @api {get} /v0.2/introspection/metrics
    @apiVersion 0.2.2
    @apiName Metrics
    @apiGroup Introspection
    @apiDescription Returns the metrics that can be queried

    @apiSampleRequest /v0.2/introspection/geolevels
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        geolevels:
        - id: world
          text: 'World'
        - id: country
          text: 'Country'
          parent: world
        - id: ccaa
          text: 'CCAA'
          parent: country
        - id: state
          text: 'State'
          parent: ccaa 
        - id: city
          text: 'City'
          parent: state
        - id: localgroup
          text: 'Local Group'
          parent: world
          aggregation: False
    """
    return ns(
        geolevels = [
        ns(**data, id=key)
        for key, data in common.geolevels.items()
    ])

@api.route('/introspection/geolevels/<geolevel>')
@yaml_response
def introspectionGeoLevelOptions(geolevel):
    """
    @api {get} /v0.2/introspection/metrics
    @apiVersion 0.2.2
    @apiName Metrics
    @apiGroup Introspection
    @apiDescription Returns the metrics that can be queried

    @apiSampleRequest /v0.2/introspection/geolevels
    @apiSuccessExample {yaml} Success-Response:
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
    """
    if geolevel == 'localgroup':
        return ns(
            options=ns(api.localGroups.getLocalGroups())
        )
    location_filter = extractFilters()
    return ns(options=api.source.geolevelOptions(geolevel, **location_filter))


def validateInputDates(ondate = None, since = None, todate = None):
    return not (not ondate is None and (not since is None or not todate is None))

def extractQueryParam(location_filter_req, alias_filters, geolevel):
    filterValues = request.args.getlist(geolevel)
    filterValues += alias_filters.get(geolevel, [])
    if len(filterValues) != 0:
        location_filter_req[geolevel] = tuple(filterValues)

def extractAlias():
    localgroups = request.args.getlist('localgroup')
    return api.localGroups.aliasFilters(localgroups) if localgroups else ns()

# TODO: Untested
def extractFilters():
    result = ns()
    alias_filters = extractAlias()
    for plural, level, codefield, namefield in common.aggregation_levels:
        extractQueryParam(result, alias_filters, level)
    return result


"""
@apiDefine CommonDistribution

@apiParam {String="country","ccaa","state","city"} [geolevel=world] Geographical detail level
@apiParam {String} [country] ISO codes of the countries to be included
@apiParam {String} [ccaa] INE codes of the CCAA's to be included
@apiParam {String} [state] INE codes of the states to be included
@apiParam {String} [city] INE codes of cities to be included
@apiParam {String} [localgroup] Code of the Local Group to be included. It represents an alias of one or more filters.
"""

"""
@api {get} /v0.2/:metric/by/:geolevel/on/:ondate

@apiVersion 0.2.2
@apiGroup Distribution
@apiName Distribution
@apiDescription Returns the geographical distribution of a quantity at a given date.

Use the geolevel to get more geographical detail (country, ccaa, state, city).

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
@apiUse CommonDistribution
@apiParam {Date} [ondate=today]  Single date, in iso format.

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
@api {get} /v0.2/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate

@apiVersion 0.2.2
@apiGroup DistributionSeries
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


@apiParam {String="contracts","members"} metric Quantity to aggregate.
@apiUse CommonDistribution
@apiParam {String="yearly","monthly"} frequency  Indicate a date series (only first day of the month, year...)
@apiParam {Date} [fromdate=2012-01-01]  Earlier date to show, in iso format. 
@apiParam {Date} [todate=2018-08-01]  Later date to show, in iso format. 

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

    relation_paramField_param = [
            ['metric', metric],
            ['frequency', frequency],
            ['geolevel', geolevel]
          ]

    for paramField, param in relation_paramField_param:
        validateParams(paramField, param)

    content = api.source

    request_dates = requestDates(
        first=api.firstDate,
        last=api.source.getLastDay(metric),
        on=ondate,
        since=fromdate,
        to=todate,
        periodicity=frequency,
    )
    location_filter = extractFilters()

    return getAggregated(content, metric, request_dates, location_filter, geolevel, mutable=False)




"""
@apiDefine MapDistribution


"""

"""
@api {get} /v0.2/map/:metric/by/:geolevel/on/:ondate

@apiVersion 0.2.7
@apiGroup Map
@apiName Map
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

@apiParam {String="contracts","members"} metric Quantity to aggregate
@apiParam {String="ccaa","state"} geolevel Geographical detail level
@apiParam {Date} [ondate=today]  Single date, in iso format
@apiParam {String="en", "es", "ca", "gl", "eu"} [lang=en] Response language

@apiSuccess {svg} Response Map that represents the geographical distribution at a given date

"""

"""
@api {get} /v0.2/map/:metric/per/:relativemetric/by/:geolevel/on/:ondate

@apiVersion 0.2.7
@apiGroup RelativeMap
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

@apiParam {String="contracts","members"} metric Quantity to aggregate
@apiParam {String="population"} relativemetric Metric to relativize the values by
@apiParam {String="ccaa","state"} geolevel Geographical detail level
@apiParam {Date} [ondate=today]  Single date, in iso format
@apiParam {String="en", "es", "ca", "gl", "eu"} [lang=en] Response language

@apiSuccess {svg} Response Map that represents the relative geographical distribution at a given date

"""

"""
@api {get} /v0.2/map/:metric/by/:geolevel/:frequency/from/:fromdate/to/:todate

@apiVersion 0.2.2
@apiGroup MapSeries
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


@apiParam {String="contracts","members"} metric Quantity to aggregate
@apiParam {String="ccaa","state"} geolevel Geographical detail level
@apiParam {String="yearly","monthly"} frequency  Indicate a date series (only first day of the month, year...)
@apiParam {Date} [fromdate=2012-01-01]  Earlier date to show, in iso format
@apiParam {Date} [todate=2020-02-01]  Later date to show, in iso format
@apiParam {String="en", "es", "ca", "gl", "eu"} [lang=en] Response language

@apiSuccess {GIF} Response Map animation that represents the temporal evolution of the geographical distribution

"""
"""
@api {get} /v0.2/map/:metric/per/:relativemetric/by/:geolevel/:frequency/from/:fromdate/to/:todate

@apiVersion 0.2.2
@apiGroup RelativeMapSeries
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


@apiParam {String="contracts","members"} metric Quantity to aggregate
@apiParam {String="ccaa","state"} geolevel Geographical detail level
@apiParam {String="yearly","monthly"} frequency  Indicate a date series (only first day of the month, year...)
@apiParam {Date} [fromdate=2012-01-01]  Earlier date to show, in iso format
@apiParam {Date} [todate=2020-02-01]  Later date to show, in iso format
@apiParam {String="en", "es", "ca", "gl", "eu"} [lang=en] Response language

@apiSuccess {GIF} Response Map animation that represents the temporal evolution of the geographical distribution

"""

@api.route('/map/<string:metric>')
@api.route('/map/<string:metric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/on/<isodate:ondate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/from/<isodate:fromdate>')
@api.route('/map/<string:metric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
@api.route('/map/<string:metric>/per/<string:relativemetric>/by/<string:geolevel>/<string:frequency>/to/<isodate:todate>')
def map(metric=None, ondate=None, geolevel='ccaa', frequency=None, fromdate=None, todate=None, relativemetric=None):

    relation_paramField_param = [
        ['metric', metric],
        ['geolevel', geolevel],
        ['frequency', frequency],
      ]
    for paramField, param in relation_paramField_param:
        validateParams(paramField, param)

    relation_paramField_param += [['relativemetric',relativemetric]]
    validateImplementation(relation_paramField_param)
    request_dates = requestDates(first=api.firstDate, last=api.source.getLastDay(metric), on=ondate, since=fromdate, to=todate, periodicity=frequency)

    locationCodes = api.relativeMetricSource.getCodesByGeolevel(geolevel=geolevel)
    relativeMValues = api.relativeMetricSource.getValuesByCode(metric=relativemetric, geolevel=geolevel) if relativemetric else dict()
    result = renderMap(
        source=api.source,
        metric=metric,
        dates=request_dates,
        geolevel=geolevel,
        template=api.mapTemplateSource.getTemplate(geolevel=geolevel, lang=str(get_locale())),
        legendTemplate=api.mapTemplateSource.getLegend(),
        locationsCodes=locationCodes,
        relativeMetricValues=relativeMValues,
    )
    response = make_response(result)

    if len(request_dates) > 1:
        response.mimetype = 'image/gif'
        return response

    response.mimetype = 'image/svg+xml'
    return response


api.source = None
api.mapTemplateSource = None
api.relativeMetricSource = None
api.localGroups = None

# vim: et ts=4 sw=4
