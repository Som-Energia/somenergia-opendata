# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app
from yamlns import namespace as ns
from .common import (
        yaml_response,
        dateSequenceMonths,
        dateSequenceWeeks,
        dateSequenceYears,
        requestDates,
    )
from .distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    locationFilter,
    )
from .missingDateError import MissingDateError

api = Blueprint(name=__name__, import_name=__name__)
api.firstDate = '2010-01-01'

def validateInputDates(ondate = None, since = None, todate = None):
    return not (not ondate is None and (not since is None or not todate is None))



def extractQueryParam(location_filter_req, queryName, objectName):
    queryParam = request.args.getlist(queryName)
    if len(queryParam) != 0:
        location_filter_req[objectName] = queryParam


"""
@api {get} /v0.2/:field[/by/:geolevel]/on/:ondate|/frequency/:frequency[/from/:fromdate][/to/:todate]?queryFilter=:locationFilters

@apiVersion 0.2.0
@apiName Distribution
@apiGroup Distribution
@apiDescription Returns the geographical distribution and temporal evolution of a quantity.
@apiParam {String="contracts","members"} field Field to get.
@apiParam {String} [ondate]  Date in iso format.
@apiParam {String} [fromdate=2012-01-01]  Date in iso format. 
@apiParam {String} [todate=2018-08-01]  Date in iso format. 
@apiParam {String="countries","ccaas","states","cities"} [geolevel=world]  Aggregate level response.
@apiParam {String="yearly","monthly"} [frequency]  Frequency response.
@apiParam {String="contry","ccaa","state","city"} [queryFilter] Query Geographical filter.

@apiSampleRequest /v0.2/contracts/by/ccaas/yearly/from/2010-01-01/to/2013-01-01?country=ES
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

#@api.route('/<field:field>') # TODO: Activate it when dates are free
@api.route('/<field:field>/on/<isodate:ondate>')
@api.route('/<field:field>/<frequency:frequency>')
@api.route('/<field:field>/<frequency:frequency>/from/<isodate:fromdate>')
@api.route('/<field:field>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<field:field>/<frequency:frequency>/to/<isodate:todate>')
@api.route('/<field:field>/by/<geolevel:geolevel>')
@api.route('/<field:field>/by/<geolevel:geolevel>/on/<isodate:ondate>')
@api.route('/<field:field>/by/<geolevel:geolevel>/<frequency:frequency>')
@api.route('/<field:field>/by/<geolevel:geolevel>/<frequency:frequency>/from/<isodate:fromdate>')
@api.route('/<field:field>/by/<geolevel:geolevel>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@api.route('/<field:field>/by/<geolevel:geolevel>/<frequency:frequency>/to/<isodate:todate>')
@yaml_response
def distribution(field=None, geolevel='world', ondate=None, frequency=None, fromdate=None, todate=None):

    content = api.source

    request_dates = requestDates(first=api.firstDate, on=ondate, since=fromdate, to=todate, periodicity=frequency)
    location_filter_req = ns()

    relation_locationLevel_id = [
            ['country', 'codi_pais'],
            ['ccaa', 'codi_ccaa'],
            ['state', 'codi_provincia'],
            ['city', 'codi_ine']
          ]

    for locationLevel_id in relation_locationLevel_id:
        extractQueryParam(location_filter_req, *locationLevel_id)

    filtered_objects = content.get(field, request_dates, location_filter_req)
    if len(filtered_objects) > 0: return aggregate(filtered_objects, geolevel)
    else: return ns()


@api.route('/version')
@yaml_response
def version():
    """
    @api {get} /v0.2/version
    @apiVersion 0.2.0
    @apiName Version
    @apiGroup Version
    @apiDescription Response version API

    @apiSampleRequest /v0.2/version
    @apiSuccessExample {yaml} Success-Response:
        HTTP/1.1 200OK
        version: 0.2.0
        compat: 0.2.0
    """
    return ns(
        version = '0.2.0',
        compat = '0.2.0',
        )


api.source = None

# vim: et ts=4 sw=4
