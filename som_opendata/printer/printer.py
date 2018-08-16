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


@printer_module.route('/<field:field>')
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
