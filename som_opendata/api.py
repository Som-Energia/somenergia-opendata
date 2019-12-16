# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, make_response
from yamlns import namespace as ns
from .common import (
        yaml_response,
        dateSequenceMonths,
        dateSequenceWeeks,
        dateSequenceYears,
        requestDates,
        validateParams,
    )
from .distribution import aggregate
from .errors import MissingDateError
from . import __version__
from .map import renderMap

api = Blueprint(name=__name__, import_name=__name__)
api.firstDate = '2010-01-01'

def validateInputDates(ondate = None, since = None, todate = None):
    return not (not ondate is None and (not since is None or not todate is None))



def extractQueryParam(location_filter_req, queryName, objectName):
    queryParam = request.args.getlist(queryName)
    if len(queryParam) != 0:
        location_filter_req[objectName] = queryParam

"""
@apiDefine CommonDistribution

@apiParam {String="country","ccaa","state","city"} [geolevel=world] Geographical detail level
@apiParam {String} [country] ISO codes of the countries to be included
@apiParam {String} [ccaa] INE codes of the CCAA's to be included
@apiParam {String} [state] INE codes of the states to be included
@apiParam {String} [city] INE codes of cities to be included
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

    request_dates = requestDates(first=api.firstDate, last=api.source.getLastDay(metric), on=ondate, since=fromdate, to=todate, periodicity=frequency)
    location_filter_req = ns()

    relation_locationLevel_id = [
            ['country', 'codi_pais'],
            ['ccaa', 'codi_ccaa'],
            ['state', 'codi_provincia'],
            ['city', 'codi_ine']
          ]

    for locationLevel_id in relation_locationLevel_id:
        extractQueryParam(location_filter_req, *locationLevel_id)

    filtered_objects = content.get(metric, request_dates, location_filter_req)
    if len(filtered_objects) > 0: return aggregate(filtered_objects, geolevel)
    else: return ns()


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



@api.route('/wipmap/<string:metric>')
@api.route('/wipmap/<string:metric>/on/<isodate:ondate>')
@api.route('/wipmap/<string:metric>/by/<string:geolevel>')
@api.route('/wipmap/<string:metric>/by/<string:geolevel>/on/<isodate:ondate>')
def map(metric=None, ondate=None, geolevel='ccaa'):
    request_dates = requestDates(first=api.firstDate, last=api.source.getLastDay(metric), on=ondate, since=None, to=None, periodicity=None)
    result = renderMap(source=api.source, metric=metric, date=request_dates, geolevel=geolevel)
    response = make_response(result)
    response.mimetype = 'image/svg+xml'
    return response

api.source = None

# vim: et ts=4 sw=4
