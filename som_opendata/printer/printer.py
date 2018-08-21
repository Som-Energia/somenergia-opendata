# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app
from yamlns import namespace as ns
from ..common import (
        yaml_response,
        dateSequenceMonths,
        dateSequenceWeeks,
        dateSequenceYears,
        requestDates,
    )
from ..distribution import (
    parse_tsv,
    tuples2objects,
    aggregate,
    locationFilter,
    pickDates,
    )
from ..missingDateError import MissingDateError

printer_module = Blueprint(name='printer_module', import_name=__name__)
printer_module.firstDate = '2010-01-01'

def validateInputDates(ondate = None, since = None, todate = None):
    return not (not ondate is None and (not since is None or not todate is None))



def extractQueryParam(location_filter_req, queryName, objectName):
    queryParam = request.args.getlist(queryName)
    if len(queryParam) != 0:
        location_filter_req[objectName] = queryParam


"""
@api {get} /printer/:field[/by/:aggregateLevel]/on/:ondate|/frequency/:frequency[/from/:fromdate][/to/:todate]?queryFilter=:locationFilters

@apiVersion 1.0.1
@apiName OpenData
@apiGroup Printer
@apiDescription Retorna un yaml amb la distribució desitjada repartida en espai - temps
@apiParam {String="contracts","members"} field  Firstname of the User.
@apiParam {String} [ondate]  Date in iso format.
@apiParam {String} [fromdate=2012-01-01]  Date in iso format. 
@apiParam {String} [todate=2018-08-01]  Date in iso format. 
@apiParam {String="countries","ccaas","states","cities"} [aggregateLevel=world]  Aggregate level response.
@apiParam {String="yearly","monthly"} [frequency]  Frequency response.
@apiParam {String="contry","ccaa","state","city"} [queryFilter] Query Geographical filter.


@apiSampleRequest http://192.168.1.5:5001/printer/contracts/by/ccaas/yearly/from/2010-01-01/to/2013-01-01?country=ES
@apiSuccessExample {yaml} Success-Response:
    HTTP/1.1 200OK
    {
        dates:
        - 2010-01-01
        - 2011-01-01
        - 2012-01-01
        - 2013-01-01
        data:
        - 0
        - 0
        - 277
        - 3197
        countries:
          ES:
            name: España
            data:
            - 0
            - 0
            - 277
            - 3197
            ccaas:
              '01':
                name: Andalucia
                data:
                - 0
                - 0
                - 0
                - 48
              '02':
                name: Aragón
                data:
                - 0
                - 0
                - 0
                - 124
              '03':
                name: Asturias, Principado de
                data:
                - 0
                - 0
                - 0
                - 13
              '04':
                name: Baleares, Islas
                data:
                - 0
                - 0
                - 1
                - 235
              '05':
                name: Canarias
                data:
                - 0
                - 0
                - 0
                - 0
              '06':
                name: Cantabria
                data:
                - 0
                - 0
                - 0
                - 12
              08:
                name: Castilla - La Mancha
                data:
                - 0
                - 0
                - 0
                - 28
              '07':
                name: Castilla y León
                data:
                - 0
                - 0
                - 0
                - 24
              09:
                name: Cataluña
                data:
                - 0
                - 0
                - 256
                - 2054
              '10':
                name: Comunidad Valenciana
                data:
                - 0
                - 0
                - 11
                - 224
              '11':
                name: Extremadura
                data:
                - 0
                - 0
                - 0
                - 14
              '12':
                name: Galicia
                data:
                - 0
                - 0
                - 0
                - 24
              '13':
                name: Madrid, Comunidad de
                data:
                - 0
                - 0
                - 3
                - 145
              '14':
                name: Murcia, Región de
                data:
                - 0
                - 0
                - 0
                - 11
              '15':
                name: Navarra, Comunidad Foral de
                data:
                - 0
                - 0
                - 6
                - 151
              '16':
                name: País Vasco
                data:
                - 0
                - 0
                - 0
                - 53
              '17':
                name: Rioja, La
                data:
                - 0
                - 0
                - 0
                - 37
    }
"""

@printer_module.route('/<field:field>/on/<isodate:ondate>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>/on/<isodate:ondate>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>/<frequency:frequency>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@printer_module.route('/<field:field>/by/<aggregateLevel:al>/<frequency:frequency>/to/<isodate:todate>')
@printer_module.route('/<field:field>/<frequency:frequency>')
@printer_module.route('/<field:field>/<frequency:frequency>/from/<isodate:fromdate>')
@printer_module.route('/<field:field>/<frequency:frequency>/from/<isodate:fromdate>/to/<isodate:todate>')
@printer_module.route('/<field:field>/<frequency:frequency>/to/<isodate:todate>')
@yaml_response
def printer(field=None, al='world', ondate=None, frequency=None, fromdate=None, todate=None):

    content = current_app.csvSource

    request_dates = requestDates(first=printer_module.firstDate, on=ondate, since=fromdate, to=todate, periodicity=frequency)
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
    if len(filtered_objects) > 0: return aggregate(filtered_objects, al)
    else: return ns()


printer_module.source = None
